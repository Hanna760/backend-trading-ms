# Configuración de Correo Electrónico

## Variables de Entorno Requeridas

Para que funcione el envío de correos electrónicos, necesitas configurar las siguientes variables de entorno:

```bash
# Configuración básica de correo
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_contraseña_de_aplicacion
MAIL_FROM=tu_email@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
```

## Configuración por Proveedor

### Gmail
```bash
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=contraseña_de_aplicacion_gmail
MAIL_FROM=tu_email@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
```

**Importante:** Para Gmail necesitas usar una "Contraseña de aplicación" en lugar de tu contraseña normal.

### Outlook/Hotmail
```bash
MAIL_USERNAME=tu_email@outlook.com
MAIL_PASSWORD=tu_contraseña
MAIL_FROM=tu_email@outlook.com
MAIL_PORT=587
MAIL_SERVER=smtp-mail.outlook.com
```

### Yahoo
```bash
MAIL_USERNAME=tu_email@yahoo.com
MAIL_PASSWORD=contraseña_de_aplicacion_yahoo
MAIL_FROM=tu_email@yahoo.com
MAIL_PORT=587
MAIL_SERVER=smtp.mail.yahoo.com
```

### SendGrid
```bash
MAIL_USERNAME=apikey
MAIL_PASSWORD=tu_api_key_de_sendgrid
MAIL_FROM=tu_email_verificado@sendgrid.com
MAIL_PORT=587
MAIL_SERVER=smtp.sendgrid.net
```

## Cómo Obtener Contraseñas de Aplicación

### Gmail
1. Ve a tu cuenta de Google
2. Seguridad → Verificación en 2 pasos (debe estar activada)
3. Contraseñas de aplicaciones
4. Selecciona "Correo" y "Otro"
5. Ingresa un nombre para la aplicación
6. Usa la contraseña generada como `MAIL_PASSWORD`

### Yahoo
1. Ve a la configuración de seguridad de Yahoo
2. Genera una contraseña de aplicación específica
3. Usa esa contraseña como `MAIL_PASSWORD`

## Funcionalidad

Cuando se crea una orden (compra o venta), el sistema automáticamente:

1. Crea la orden en la base de datos
2. Obtiene la información del usuario que creó la orden
3. Envía un correo de confirmación al email del usuario
4. El correo incluye:
   - Tipo de orden (Compra/Venta)
   - Número de orden
   - Precio
   - Mensaje personalizado

## Manejo de Errores

- Si el usuario no tiene email configurado, se registra un warning en los logs
- Si hay error en el envío del correo, se registra el error pero la orden se crea exitosamente
- Los errores de correo no afectan la funcionalidad principal de creación de órdenes
