from src.app.domain.repositories.crud_repository import CrudRepository
from src.app.domain.entities.order import Order
from src.app.domain.entities.user import User
from src.app.application.services.email_service import EmailService
from src.app.application.services.user_service import UserService
from src.app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class OrderService:
    def __init__(self, order_repository: CrudRepository[Order]):
        self.order_repository = order_repository
        self.email_service = EmailService()
        self.user_service = UserService(UserRepositoryImpl())

    def get_all(self) -> list[Order]:
        return self.order_repository.get_all()

    def get_by_id(self, order_id: int) -> Order:
        return self.order_repository.get_by_id(order_id)

    def create(self, order: Order) -> Order:
        """
        Crea una nueva orden y envía notificación por correo
        """
        try:
            # Crear la orden
            created_order = self.order_repository.create(order)
            
            # Obtener información del usuario
            user = self.user_service.get_by_id(order.usuario_id)
            
            if user and user.email:
                # Enviar correo de confirmación de forma asíncrona
                self._send_confirmation_email_async(created_order, user)
            else:
                logger.warning(f"No se pudo enviar correo de confirmación para la orden {created_order.id}: usuario sin email")
            
            return created_order
            
        except Exception as e:
            logger.error(f"Error creando orden: {str(e)}")
            raise e

    def update(self, order_id: int, order: Order) -> Order:
        return self.order_repository.update(order_id, order)

    def delete(self, order_id: int) -> bool:
        return self.order_repository.delete(order_id)

    def get_pending_orders(self) -> list[Order]:
        return self.order_repository.get_pending_orders()

    def approve_order(self, order_id: int) -> Order:
        """
        Aprueba una orden específica
        """
        updated_order = self.order_repository.update_order_status(order_id, "approved")
        if not updated_order:
            raise ValueError(f"Order with id {order_id} not found")
        
        # Enviar correo de notificación de aprobación
        self._send_status_email_async(updated_order, "approved")
        
        return updated_order

    def deny_order(self, order_id: int) -> Order:
        """
        Deniega una orden específica
        """
        updated_order = self.order_repository.update_order_status(order_id, "denied")
        if not updated_order:
            raise ValueError(f"Order with id {order_id} not found")
        
        # Enviar correo de notificación de denegación
        self._send_status_email_async(updated_order, "denied")
        
        return updated_order

    def _send_status_email_async(self, order: Order, status: str):
        """
        Envía correo de cambio de estado de forma asíncrona
        """
        try:
            # Obtener información del usuario
            user = self.user_service.get_by_id(order.usuario_id)
            
            if user and user.email:
                import asyncio
                import threading
                
                def run_email_task():
                    try:
                        # Crear un nuevo loop de eventos para el hilo
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        
                        # Ejecutar el envío de correo
                        loop.run_until_complete(
                            self.email_service.send_order_status_email(
                                user_email=user.email,
                                user_name=user.full_name or user.username,
                                order_id=order.id,
                                status=status,
                                order_type=order.tipo_orden,
                                price=order.precio
                            )
                        )
                        loop.close()
                    except Exception as e:
                        logger.error(f"Error enviando correo de estado en hilo separado: {str(e)}")
                
                # Ejecutar en un hilo separado para no bloquear
                email_thread = threading.Thread(target=run_email_task)
                email_thread.daemon = True
                email_thread.start()
                
            else:
                logger.warning(f"No se pudo enviar correo de estado para la orden {order.id}: usuario sin email")
                
        except Exception as e:
            logger.error(f"Error configurando envío de correo de estado: {str(e)}")

    def _send_confirmation_email_async(self, order: Order, user: User):
        """
        Envía correo de confirmación de forma asíncrona
        """
        try:
            import asyncio
            import threading
            
            def run_email_task():
                try:
                    # Crear un nuevo loop de eventos para el hilo
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    # Ejecutar el envío de correo
                    loop.run_until_complete(
                        self.email_service.send_order_confirmation_email(
                            user_email=user.email,
                            user_name=user.full_name or user.username,
                            order_type=order.tipo_orden,
                            price=order.precio,
                            order_id=order.id
                        )
                    )
                    loop.close()
                except Exception as e:
                    logger.error(f"Error enviando correo de confirmación en hilo separado: {str(e)}")
            
            # Ejecutar en un hilo separado para no bloquear
            email_thread = threading.Thread(target=run_email_task)
            email_thread.daemon = True
            email_thread.start()
            
        except Exception as e:
            logger.error(f"Error configurando envío de correo de confirmación: {str(e)}")
