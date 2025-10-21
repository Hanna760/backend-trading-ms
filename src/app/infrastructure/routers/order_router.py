# src/app/infrastructure/api/routes/order_routes.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, Body
from fastapi.security import OAuth2PasswordBearer

from src.app.application.services.generic_service import GenericService
from src.app.application.services.order_service import OrderService
from src.app.domain.entities.order import Order
from src.app.infrastructure.repositories.order_repository_impl import OrdenRepositoryImpl
from src.app.domain.entities.user import User
from src.app.infrastructure.dependencies.auth_dependencies import get_current_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


# Dependency para instanciar el servicio de Orden con notificaciones por correo
def get_order_service() -> OrderService:
    repository = OrdenRepositoryImpl()
    return OrderService(repository)


# Obtener todas las órdenes
@router.get("/", response_model=List[Order], summary="Get All Orders")
def get_all_orders(
    service: OrderService = Depends(get_order_service),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener TODAS las órdenes del sistema
    Requiere autenticación Bearer token
    Retorna array completo de órdenes ordenadas por fecha (más recientes primero)
    """
    return service.get_all()


# Obtener órdenes pendientes
@router.get("/pending", response_model=List[Order], summary="Get Pending Orders")
def get_pending_orders(
    service: OrderService = Depends(get_order_service),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener órdenes pendientes de aprobación
    Requiere autenticación Bearer token
    Filtro: estado = 'pending'
    """
    return service.get_pending_orders()


# Obtener orden por ID
@router.get("/{orden_id}", response_model=Order, summary="Get Orden by ID")
def get_orden_by_id(
    orden_id: int = Path(..., description="The ID of the orden to retrieve"),
    service: OrderService = Depends(get_order_service),
    current_user: User = Depends(get_current_user)
):
    orden = service.get_by_id(orden_id)
    if not orden:
        raise HTTPException(status_code=404, detail="Orden not found")
    return orden


# Crear una nueva orden
@router.post("/", response_model=Order, status_code=201, summary="Create New Orden")
def create_orden(
    orden: Order = Body(..., description="Orden to create"),
    service: OrderService = Depends(get_order_service),
    current_user: User = Depends(get_current_user)
):
    return service.create(orden)


# Actualizar una orden existente
@router.put("/{orden_id}", response_model=Order, summary="Update Orden by ID")
def update_orden(
    orden_id: int,
    orden: Order = Body(...),
    service: OrderService = Depends(get_order_service),
    current_user: User = Depends(get_current_user)
):
    updated_orden = service.update(orden_id, orden)
    if not updated_orden:
        raise HTTPException(status_code=404, detail="Orden not found")
    return updated_orden


# Aprobar una orden específica
@router.put("/{order_id}/approve", response_model=dict, summary="Approve Order")
def approve_order(
    order_id: int = Path(..., description="The ID of the order to approve"),
    service: OrderService = Depends(get_order_service),
    current_user: User = Depends(get_current_user)
):
    """
    Aprobar una orden específica
    Requiere autenticación Bearer token
    Cambia estado a 'approved'
    Retorna mensaje de éxito
    """
    try:
        service.approve_order(order_id)
        return {"message": "Orden aprobada exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Denegar una orden específica
@router.put("/{order_id}/deny", response_model=dict, summary="Deny Order")
def deny_order(
    order_id: int = Path(..., description="The ID of the order to deny"),
    service: OrderService = Depends(get_order_service),
    current_user: User = Depends(get_current_user)
):
    """
    Denegar una orden específica
    Requiere autenticación Bearer token
    Cambia estado a 'denied'
    Retorna mensaje de éxito
    """
    try:
        service.deny_order(order_id)
        return {"message": "Orden denegada exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Eliminar una orden (soft delete)
@router.delete("/{orden_id}", response_model=dict, summary="Delete Orden by ID")
def delete_orden(
    orden_id: int,
    service: OrderService = Depends(get_order_service),
    current_user: User = Depends(get_current_user)
):
    success = service.delete(orden_id)
    if not success:
        raise HTTPException(status_code=404, detail="Orden not found or already deleted")
    return {"detail": "Orden deleted successfully"}
