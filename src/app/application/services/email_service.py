from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import Optional
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Configurar logging
logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        # Obtener configuración de variables de entorno
        mail_username = os.getenv("MAIL_USERNAME")
        mail_password = os.getenv("MAIL_PASSWORD")
        mail_from = os.getenv("MAIL_FROM")
        mail_port = int(os.getenv("MAIL_PORT", 587))
        mail_server = os.getenv("MAIL_SERVER")
        
        # Log de configuración (sin mostrar contraseña)
        logger.info("Configurando EmailService:")
        logger.info(f"  - Servidor: {mail_server}")
        logger.info(f"  - Puerto: {mail_port}")
        logger.info(f"  - Usuario: {mail_username}")
        logger.info(f"  - Desde: {mail_from}")
        logger.info(f"  - Contraseña configurada: {'Sí' if mail_password else 'No'}")
        
        # Advertencia para Gmail
        if mail_server == "smtp.gmail.com" and mail_password:
            if len(mail_password.replace(" ", "")) != 16:
                logger.warning("⚠️  Para Gmail, asegúrate de usar una Contraseña de Aplicación de 16 caracteres")
                logger.warning("   Ve a: https://myaccount.google.com/apppasswords")
        
        # Validar configuración
        if not all([mail_username, mail_password, mail_from, mail_server]):
            logger.error("❌ Configuración de correo incompleta")
            raise ValueError("Configuración de correo incompleta. Verifica las variables de entorno.")
        
        self.conf = ConnectionConfig(
            MAIL_USERNAME=mail_username,
            MAIL_PASSWORD=mail_password,
            MAIL_FROM=mail_from,
            MAIL_PORT=mail_port,
            MAIL_SERVER=mail_server,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )
        self.fastmail = FastMail(self.conf)
        logger.info("✅ EmailService configurado correctamente")

    async def send_order_confirmation_email(self, user_email: str, user_name: str, order_type: str, price: float, order_id: int):
        """
        Envía un correo de confirmación cuando se crea una orden
        """
        try:
            logger.info(f"📧 Enviando correo de confirmación de orden #{order_id} a {user_email}")
            
            # Determinar el tipo de orden en español
            tipo_orden_texto = "Compra" if order_type.upper() in ["BUY", "COMPRA"] else "Venta"
            
            subject = f"Confirmación de {tipo_orden_texto} - Orden #{order_id}"
            
            # Crear el contenido del correo
            html_content = f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #2c3e50; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; background-color: #f8f9fa; }}
                    .order-details {{ background-color: #e9ecef; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                    .footer {{ text-align: center; padding: 20px; color: #6c757d; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🏢 Andina Trading</h1>
                        <h2>Confirmación de {tipo_orden_texto}</h2>
                    </div>
                    
                    <div class="content">
                        <p>Estimado/a <strong>{user_name}</strong>,</p>
                        <p>Le confirmamos que se ha creado exitosamente su orden de <strong>{tipo_orden_texto}</strong>.</p>
                        
                        <div class="order-details">
                            <h3>📋 Detalles de la Orden:</h3>
                            <ul>
                                <li><strong>Número de Orden:</strong> #{order_id}</li>
                                <li><strong>Tipo:</strong> {tipo_orden_texto}</li>
                                <li><strong>Precio:</strong> ${price:,.2f}</li>
                                <li><strong>Estado:</strong> Pendiente de aprobación</li>
                            </ul>
                        </div>
                        
                        <p>Su orden será revisada por nuestro equipo y recibirá una notificación una vez que sea procesada.</p>
                        <p>Gracias por utilizar nuestros servicios.</p>
                    </div>
                    
                    <div class="footer">
                        <p>Saludos cordiales,<br><strong>Equipo de Andina Trading</strong></p>
                        <p><small>Este es un correo automático, por favor no responder.</small></p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            message = MessageSchema(
                subject=subject,
                recipients=[user_email],
                body=html_content,
                subtype="html"
            )
            
            await self.fastmail.send_message(message)
            logger.info(f"✅ Correo enviado exitosamente a {user_email}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error enviando correo a {user_email}: {str(e)}")
            return False

    async def send_order_status_email(self, user_email: str, user_name: str, order_id: int, status: str, order_type: str, price: float):
        """
        Envía un correo cuando cambia el estado de una orden (aprobada/denegada)
        """
        try:
            logger.info(f"📧 Enviando correo de cambio de estado para orden #{order_id} a {user_email}")
            
            # Determinar el tipo de orden y estado en español
            tipo_orden_texto = "Compra" if order_type.upper() in ["BUY", "COMPRA"] else "Venta"
            estado_texto = "Aprobada" if status.lower() == "approved" else "Denegada"
            
            subject = f"Actualización de Orden #{order_id} - {estado_texto}"
            
            # Crear el contenido del correo
            html_content = f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: {'#28a745' if status.lower() == 'approved' else '#dc3545'}; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; background-color: #f8f9fa; }}
                    .order-details {{ background-color: #e9ecef; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                    .footer {{ text-align: center; padding: 20px; color: #6c757d; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🏢 Andina Trading</h1>
                        <h2>Orden #{order_id} - {estado_texto}</h2>
                    </div>
                    
                    <div class="content">
                        <p>Estimado/a <strong>{user_name}</strong>,</p>
                        <p>Le informamos que su orden de <strong>{tipo_orden_texto}</strong> ha sido <strong>{estado_texto.lower()}</strong>.</p>
                        
                        <div class="order-details">
                            <h3>📋 Detalles de la Orden:</h3>
                            <ul>
                                <li><strong>Número de Orden:</strong> #{order_id}</li>
                                <li><strong>Tipo:</strong> {tipo_orden_texto}</li>
                                <li><strong>Precio:</strong> ${price:,.2f}</li>
                                <li><strong>Estado:</strong> {estado_texto}</li>
                            </ul>
                        </div>
                        
                        {"<p>Su orden ha sido procesada exitosamente y está lista para ejecutarse.</p>" if status.lower() == "approved" else "<p>Su orden no pudo ser procesada en este momento. Por favor contacte con nuestro equipo para más información.</p>"}
                        
                        <p>Gracias por utilizar nuestros servicios.</p>
                    </div>
                    
                    <div class="footer">
                        <p>Saludos cordiales,<br><strong>Equipo de Andina Trading</strong></p>
                        <p><small>Este es un correo automático, por favor no responder.</small></p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            message = MessageSchema(
                subject=subject,
                recipients=[user_email],
                body=html_content,
                subtype="html"
            )
            
            await self.fastmail.send_message(message)
            logger.info(f"✅ Correo de estado enviado exitosamente a {user_email}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error enviando correo de estado a {user_email}: {str(e)}")
            return False

    async def send_email(self, to_email: str, subject: str, html_content: str):
        """
        Método genérico para enviar correos
        """
        try:
            logger.info(f"📧 Enviando correo genérico a {to_email}")
            
            message = MessageSchema(
                subject=subject,
                recipients=[to_email],
                body=html_content,
                subtype="html"
            )
            
            await self.fastmail.send_message(message)
            logger.info(f"✅ Correo genérico enviado exitosamente a {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error enviando correo genérico a {to_email}: {str(e)}")
            return False
