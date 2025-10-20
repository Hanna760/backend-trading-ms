

# 🧠 backend-Andina Trading

Proyecto base con FastAPI para levantar una API localmente.

## 🚀 Instalación

### Opción 1: Con Docker (Recomendado)

1. Clona el repositorio y entra al directorio del proyecto:

```bash
git clone <URL-del-repo>
cd backend-at
```

2. Copia el archivo de configuración de entorno:

```bash
cp docker.env .env
```

3. Levanta la aplicación con Docker Compose:

```bash
docker-compose up -d
```

Esto levantará:
- **MySQL Database** en el puerto `3306`
- **FastAPI Application** en el puerto `8000`

4. Para ver los logs:

```bash
docker-compose logs -f
```

5. Para detener la aplicación:

```bash
docker-compose down
```

6. Para reconstruir la aplicación después de cambios:

```bash
docker-compose up --build -d
```

### Opción 2: Instalación Local

1. Clona el repositorio y entra al directorio del proyecto:

```bash
git clone <URL-del-repo>
cd backend-at
```

1.1 Si es linux se debe de activar el entorno del proyecto:

```bash
source venv/bin/activate
```

1.2 Si es windows se ejecuta con conda

2. Crea y activa el entorno virtual:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instala las dependencias necesarias:

```bash
pip install fastapi uvicorn autopep8 python-multipart
```

## ▶️ Ejecución del servidor

### Con Docker
```bash
docker-compose up -d
```

### Localmente
Con el entorno virtual activado, ejecuta:

```bash
uvicorn main:app --reload
```

Esto levantará el servidor en `http://127.0.0.1:8000`.

## 🧪 Endpoints de prueba

- Documentación interactiva: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Documentación alternativa: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 📧 Sistema de Notificaciones por Correo

El sistema incluye notificaciones automáticas por correo electrónico cuando se crean órdenes de compra o venta.

### Configuración

1. Configura las variables de entorno para el correo en tu archivo `.env`:

```bash
# Configuración de correo (ejemplo para Gmail)
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_contraseña_de_aplicacion
MAIL_FROM=tu_email@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
```

2. Para Gmail, necesitas usar una "Contraseña de aplicación" en lugar de tu contraseña normal.

### Funcionalidad

- ✅ Envío automático de correos de confirmación al crear órdenes
- ✅ Soporte para múltiples proveedores de correo (Gmail, Outlook, Yahoo, SendGrid)
- ✅ Manejo de errores sin afectar la funcionalidad principal
- ✅ Plantillas HTML profesionales para los correos

### Pruebas

#### Prueba Local
```bash
python test_email_system.py
```

#### Prueba con Docker
```bash
# En Windows (PowerShell)
.\test_docker_email.sh

# En Linux/Mac
./test_docker_email.sh
```

### Configuración para Docker

1. **Edita el archivo `docker.env`** con tus credenciales reales:
   ```bash
   MAIL_USERNAME=tu_email@gmail.com
   MAIL_PASSWORD=tu_contraseña_de_aplicacion
   MAIL_FROM=tu_email@gmail.com
   ```

2. **Levanta los servicios**:
   ```bash
   docker-compose up -d
   ```

3. **Verifica que funcione**:
   ```bash
   docker-compose logs app
   ```

Para más detalles sobre la configuración, consulta [EMAIL_CONFIG.md](EMAIL_CONFIG.md).

## 🐳 Configuración de Docker

### Variables de Entorno

El archivo `docker.env` contiene las siguientes variables configurables:

- `MYSQL_ROOT_PASSWORD`: Contraseña del usuario root de MySQL (default: 1234)
- `MYSQL_DATABASE`: Nombre de la base de datos (default: andina_trading)
- `MYSQL_USER`: Usuario de la aplicación (default: app_user)
- `MYSQL_PASSWORD`: Contraseña del usuario de la aplicación (default: app_password)

### Servicios Docker

- **mysql**: Base de datos MySQL 8.0 con inicialización automática
- **app**: Aplicación FastAPI con hot-reload habilitado

### Comandos Útiles

```bash
# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f app
docker-compose logs -f mysql

# Ejecutar comandos en el contenedor de la app
docker-compose exec app bash

# Reiniciar un servicio específico
docker-compose restart app

# Eliminar volúmenes (CUIDADO: Esto borrará los datos de la base de datos)
docker-compose down -v
```
```
