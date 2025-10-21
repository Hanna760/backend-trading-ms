from fastapi import APIRouter, Depends, HTTPException
from src.app.domain.entities.portfolio import Portfolio
from src.app.domain.entities.user import User
from src.app.application.services.portfolio_service import PortfolioService
from src.app.infrastructure.dependencies.auth_dependencies import get_current_user

router = APIRouter()

def get_portfolio_service():
    return PortfolioService()

@router.get("/test/{user_id}", response_model=Portfolio)
async def get_user_portfolio_test(
    user_id: int,
    portfolio_service: PortfolioService = Depends(get_portfolio_service)
):
    """
    Endpoint de prueba para obtener el portafolio sin autenticación.
    Solo para testing - NO usar en producción.
    """
    try:
        portfolio = portfolio_service.get_user_portfolio(user_id)
        return portfolio
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el portafolio: {str(e)}")

@router.get("/portfolio", response_model=Portfolio)
async def get_user_portfolio(
    current_user: User = Depends(get_current_user),
    portfolio_service: PortfolioService = Depends(get_portfolio_service)
):
    """
    Obtiene el portafolio completo del usuario autenticado.
    
    Retorna:
    - Saldo disponible (base $25,000 menos gastos en compras)
    - Valor total del portafolio
    - Ganancia/pérdida total
    - Lista de acciones con sus detalles
    """
    try:
        portfolio = portfolio_service.get_user_portfolio(current_user.id)
        return portfolio
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el portafolio: {str(e)}")
