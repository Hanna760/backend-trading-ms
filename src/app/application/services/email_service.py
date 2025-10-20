from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
            MAIL_FROM=os.getenv("MAIL_FROM"),
            MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
            MAIL_SERVER=os.getenv("MAIL_SERVER"),
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )
        self.fastmail = FastMail(self.conf)

    async def send_order_confirmation_email(self, user_email: str, user_name: str, order_type: str, price: float, order_id: int):
        """
        Envía un correo de confirmación cuando se crea una orden
        """
        try:
            # Determinar el tipo de orden en español
            tipo_orden_texto = "Compra" if order_type.lower() == "compra" else "Venta"
            
            subject = f"Confirmación de {tipo_orden_texto} - Orden #{order_id}"
            
            # Crear el contenido del correo
            html_content = f"""
            <html>
            <body>
                <h2>Confirmación de {tipo_orden_texto}</h2>
                <p>Estimado/a {user_name},</p>
                <p>Le confirmamos que se ha creado exitosamente su orden de <strong>{tipo_orden_texto}</strong>.</p>
                
                <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3>Detalles de la Orden:</h3>
                    <ul>
                        <li><strong>Número de Orden:</strong> #{order_id}</li>
                        <li><strong>Tipo:</strong> {tipo_orden_texto}</li>
                        <li><strong>Precio:</strong> ${price:,.2f}</li>
                    </ul>
                </div>
                
                <p>Gracias por utilizar nuestros servicios.</p>
                <p>Saludos cordiales,<br>Equipo de Andina Trading</p>
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
            return True
            
        except Exception as e:
            print(f"Error enviando correo: {str(e)}")
            return False

    async def send_email(self, to_email: str, subject: str, html_content: str):
        """
        Método genérico para enviar correos
        """
        try:
            message = MessageSchema(
                subject=subject,
                recipients=[to_email],
                body=html_content,
                subtype="html"
            )
            
            await self.fastmail.send_message(message)
            return True
            
        except Exception as e:
            print(f"Error enviando correo: {str(e)}")
            return False
