from typing import Optional
from src.app.domain.entities.portfolio import Portfolio, PortfolioItem
from src.app.domain.entities.order import Order
from src.app.domain.entities.action import Accion
from src.app.infrastructure.repositories.order_repository_impl import OrdenRepositoryImpl
from src.app.infrastructure.repositories.action_repository_impl import AccionRepositoryImpl
from src.app.infrastructure.database.db_connection_factory import DatabaseConectionFactory
from datetime import datetime


class PortfolioService:
    """Servicio para calcular y gestionar el portafolio de usuarios"""
    
    def __init__(self):
        self.order_repository = OrdenRepositoryImpl()
        self.action_repository = AccionRepositoryImpl()
        self.base_balance = 25000.0  # Saldo base para todos los usuarios
    
    def get_user_portfolio(self, user_id: int) -> Portfolio:
        """
        Calcula el portafolio completo del usuario basado en sus órdenes
        """
        # Obtener todas las órdenes aprobadas del usuario
        orders = self._get_user_approved_orders(user_id)
        
        # Calcular el saldo disponible
        available_balance = self._calculate_available_balance(orders)
        
        # Calcular las acciones en el portafolio
        portfolio_items = self._calculate_portfolio_items(orders)
        
        # Calcular valores totales
        total_portfolio_value = sum(item.valor_actual for item in portfolio_items)
        total_gain_loss = sum(item.ganancia_perdida for item in portfolio_items)
        total_percentage_change = (total_gain_loss / (total_portfolio_value - total_gain_loss)) * 100 if total_portfolio_value > total_gain_loss else 0
        
        return Portfolio(
            usuario_id=user_id,
            saldo_disponible=available_balance,
            valor_total_portafolio=total_portfolio_value,
            ganancia_perdida_total=total_gain_loss,
            porcentaje_cambio_total=total_percentage_change,
            acciones=portfolio_items,
            fecha_actualizacion=datetime.now()
        )
    
    def _get_user_approved_orders(self, user_id: int) -> list:
        """Obtiene todas las órdenes aprobadas del usuario"""
        connection = DatabaseConectionFactory.get_connection()
        try:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT o.*, a.nombre as accion_nombre, a.valor as accion_valor_actual
                    FROM Orden o
                    LEFT JOIN Accion a ON o.accion_id = a.id
                    WHERE o.usuario_id = %s 
                    AND o.estado = 'approved' 
                    AND o.deleted_at IS NULL
                    ORDER BY o.fecha_hora ASC
                """, (user_id,))
                return cursor.fetchall()
        finally:
            DatabaseConectionFactory.release_connection(connection)
    
    def _calculate_available_balance(self, orders: list) -> float:
        """Calcula el saldo disponible del usuario"""
        total_spent = 0.0
        
        for order in orders:
            tipo_orden = order['tipo_orden'].lower()
            precio = float(order['precio'])
            comision = float(order['comision'] or 0)
            
            if tipo_orden in ['compra', 'buy', 'buy-aapl']:
                # En compras: gastamos precio + comisión
                total_spent += precio + comision
            elif tipo_orden in ['venta', 'sell', 'sell-aapl']:
                # En ventas: recibimos precio - comisión
                total_spent -= precio - comision
        
        return self.base_balance - total_spent
    
    def _calculate_portfolio_items(self, orders: list) -> list:
        """Calcula las acciones en el portafolio basado en las órdenes"""
        action_orders = self._group_orders_by_action(orders)
        return self._create_portfolio_items(action_orders)
    
    def _group_orders_by_action(self, orders: list) -> dict:
        """Agrupa las órdenes por acción"""
        action_orders = {}
        
        for order in orders:
            accion_id = order.get('accion_id')
            if not accion_id:
                continue
                
            if accion_id not in action_orders:
                action_orders[accion_id] = {
                    'nombre': order['accion_nombre'],
                    'compras': [],
                    'ventas': [],
                    'valor_actual': order['accion_valor_actual'] or 0
                }
            
            tipo_orden = order['tipo_orden'].lower()
            if tipo_orden in ['compra', 'buy', 'buy-aapl']:
                action_orders[accion_id]['compras'].append(order)
            elif tipo_orden in ['venta', 'sell', 'sell-aapl']:
                action_orders[accion_id]['ventas'].append(order)
        
        return action_orders
    
    def _create_portfolio_items(self, action_orders: dict) -> list:
        """Crea los items del portafolio"""
        portfolio_items = []
        
        for accion_id, data in action_orders.items():
            item = self._calculate_action_item(accion_id, data)
            if item:
                portfolio_items.append(item)
        
        return portfolio_items
    
    def _calculate_action_item(self, accion_id: int, data: dict) -> Optional[PortfolioItem]:
        """Calcula un item individual del portafolio"""
        total_compras = len(data['compras'])
        total_ventas = len(data['ventas'])
        cantidad_neta = total_compras - total_ventas
        
        if cantidad_neta <= 0:
            return None
        
        total_inversion = sum(float(compra['precio']) + float(compra['comision'] or 0) for compra in data['compras'])
        precio_promedio = total_inversion / total_compras if total_compras > 0 else 0
        
        valor_actual = cantidad_neta * float(data['valor_actual'])
        ganancia_perdida = valor_actual - (cantidad_neta * precio_promedio)
        porcentaje_cambio = (ganancia_perdida / (cantidad_neta * precio_promedio)) * 100 if cantidad_neta * precio_promedio > 0 else 0
        
        return PortfolioItem(
            accion_id=accion_id,
            nombre_accion=data['nombre'],
            cantidad=cantidad_neta,
            precio_promedio=precio_promedio,
            valor_actual=valor_actual,
            ganancia_perdida=ganancia_perdida,
            porcentaje_cambio=porcentaje_cambio
        )
