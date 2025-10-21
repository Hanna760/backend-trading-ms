from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PortfolioItem(BaseModel):
    """Representa una acción en el portafolio del usuario"""
    accion_id: int
    nombre_accion: str
    cantidad: int
    precio_promedio: float
    valor_actual: float
    ganancia_perdida: float
    porcentaje_cambio: float


class Portfolio(BaseModel):
    """Representa el portafolio completo del usuario"""
    usuario_id: int
    saldo_disponible: float
    valor_total_portafolio: float
    ganancia_perdida_total: float
    porcentaje_cambio_total: float
    acciones: List[PortfolioItem]
    fecha_actualizacion: datetime
