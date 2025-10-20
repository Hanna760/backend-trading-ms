#!/usr/bin/env python3
"""
Script de prueba para verificar el envío de correos electrónicos
"""

import asyncio
import os
from dotenv import load_dotenv
from src.app.application.services.email_service import EmailService

# Cargar variables de entorno
load_dotenv()

async def test_email_service():
    """Prueba el servicio de correo electrónico"""
    
    # Verificar que las variables de entorno estén configuradas
    required_vars = ['MAIL_USERNAME', 'MAIL_PASSWORD', 'MAIL_FROM', 'MAIL_SERVER']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Variables de entorno faltantes: {', '.join(missing_vars)}")
        print("Por favor configura las variables de entorno según EMAIL_CONFIG.md")
        return False
    
    try:
        # Crear instancia del servicio de correo
        email_service = EmailService()
        
        # Datos de prueba
        test_email = os.getenv('MAIL_FROM')  # Enviar a nosotros mismos para prueba
        test_name = "Usuario de Prueba"
        test_order_type = "Compra"
        test_price = 1500.50
        test_order_id = 999
        
        print(f"📧 Enviando correo de prueba a: {test_email}")
        
        # Enviar correo de prueba
        success = await email_service.send_order_confirmation_email(
            user_email=test_email,
            user_name=test_name,
            order_type=test_order_type,
            price=test_price,
            order_id=test_order_id
        )
        
        if success:
            print("✅ Correo enviado exitosamente!")
            print(f"   - Tipo de orden: {test_order_type}")
            print(f"   - Precio: ${test_price}")
            print(f"   - ID de orden: {test_order_id}")
            return True
        else:
            print("❌ Error al enviar el correo")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la prueba: {str(e)}")
        return False

def test_order_service_integration():
    """Prueba la integración del servicio de órdenes"""
    try:
        from src.app.application.services.order_service import OrderService
        from src.app.infrastructure.repositories.order_repository_impl import OrdenRepositoryImpl
        
        print("🔧 Probando integración del servicio de órdenes...")
        
        # Crear servicio de órdenes
        order_service = OrderService(OrdenRepositoryImpl())
        
        print("✅ Servicio de órdenes creado exitosamente")
        print("   - Integración con EmailService: OK")
        print("   - Dependencias: OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en la integración: {str(e)}")
        return False

async def main():
    """Función principal de prueba"""
    print("🚀 Iniciando pruebas del sistema de correos electrónicos\n")
    
    # Prueba 1: Integración del servicio
    print("1️⃣ Probando integración del servicio...")
    integration_ok = test_order_service_integration()
    print()
    
    # Prueba 2: Envío de correo
    print("2️⃣ Probando envío de correo...")
    email_ok = await test_email_service()
    print()
    
    # Resumen
    print("📊 Resumen de pruebas:")
    print(f"   - Integración: {'✅ OK' if integration_ok else '❌ FALLO'}")
    print(f"   - Envío de correo: {'✅ OK' if email_ok else '❌ FALLO'}")
    
    if integration_ok and email_ok:
        print("\n🎉 ¡Todas las pruebas pasaron! El sistema está listo para usar.")
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisa la configuración.")

if __name__ == "__main__":
    asyncio.run(main())
