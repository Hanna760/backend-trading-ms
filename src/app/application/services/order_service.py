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
                import asyncio
                try:
                    # Ejecutar el envío de correo de forma asíncrona
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        # Si ya hay un loop corriendo, crear una tarea
                        task = asyncio.create_task(
                            self.email_service.send_order_confirmation_email(
                                user_email=user.email,
                                user_name=user.full_name or user.username,
                                order_type=order.tipo_orden,
                                price=order.precio,
                                order_id=created_order.id
                            )
                        )
                    else:
                        # Si no hay loop corriendo, ejecutar directamente
                        loop.run_until_complete(
                            self.email_service.send_order_confirmation_email(
                                user_email=user.email,
                                user_name=user.full_name or user.username,
                                order_type=order.tipo_orden,
                                price=order.precio,
                                order_id=created_order.id
                            )
                        )
                except Exception as e:
                    logger.error(f"Error enviando correo de confirmación: {str(e)}")
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
