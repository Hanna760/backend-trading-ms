# 🐳 Configuración de Docker para Sistema de Correos

## Requisitos Previos

- Docker y Docker Compose instalados
- Credenciales de correo electrónico válidas

## Configuración Paso a Paso

### 1. Configurar Variables de Entorno

Edita el archivo `docker.env` con tus credenciales reales:

```bash
# Email Configuration
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_contraseña_de_aplicacion
MAIL_FROM=tu_email@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
```

**Importante para Gmail:**
- Usa una "Contraseña de aplicación" en lugar de tu contraseña normal
- Activa la verificación en 2 pasos en tu cuenta de Google
- Genera la contraseña de aplicación en: Seguridad → Contraseñas de aplicaciones

### 2. Construir y Levantar los Servicios

```bash
# Construir las imágenes
docker-compose build

# Levantar los servicios
docker-compose up -d
```

### 3. Verificar que Todo Funcione

```bash
# Ver logs de la aplicación
docker-compose logs app

# Ver logs de la base de datos
docker-compose logs mysql

# Probar el sistema de correos
docker-compose exec app python test_email_system.py
```

### 4. Probar Manualmente

1. Ve a http://localhost:8000/docs
2. Autentícate con un usuario existente
3. Crea una orden de compra o venta
4. Verifica que llegue el correo de confirmación

## Comandos Útiles

```bash
# Ver estado de los servicios
docker-compose ps

# Reiniciar solo la aplicación
docker-compose restart app

# Detener todos los servicios
docker-compose down

# Detener y eliminar volúmenes (CUIDADO: borra datos)
docker-compose down -v

# Reconstruir después de cambios en el código
docker-compose up --build -d

# Ejecutar comandos dentro del contenedor
docker-compose exec app bash
```

## Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'fastapi_mail'"

```bash
# Reconstruir la imagen
docker-compose build --no-cache
docker-compose up -d
```

### Error de conexión SMTP

1. Verifica las credenciales en `docker.env`
2. Para Gmail, asegúrate de usar contraseña de aplicación
3. Verifica que el puerto 587 esté abierto

### Error de base de datos

```bash
# Verificar que MySQL esté corriendo
docker-compose logs mysql

# Reiniciar MySQL
docker-compose restart mysql
```

## Estructura de Archivos

```
├── docker-compose.yml      # Configuración de servicios
├── Dockerfile             # Imagen de la aplicación
├── docker.env            # Variables de entorno
├── requirements.txt      # Dependencias Python
├── test_docker_email.sh  # Script de prueba
└── test_email_system.py  # Prueba del sistema de correos
```

## Variables de Entorno Disponibles

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `MAIL_USERNAME` | Usuario del correo | `tu_email@gmail.com` |
| `MAIL_PASSWORD` | Contraseña de aplicación | `abcd1234efgh5678` |
| `MAIL_FROM` | Email remitente | `tu_email@gmail.com` |
| `MAIL_PORT` | Puerto SMTP | `587` |
| `MAIL_SERVER` | Servidor SMTP | `smtp.gmail.com` |

## Logs y Monitoreo

```bash
# Ver logs en tiempo real
docker-compose logs -f app

# Ver logs de errores
docker-compose logs app | grep ERROR

# Verificar salud del servicio
docker-compose ps
```

El sistema está completamente configurado para funcionar con Docker. Solo necesitas configurar tus credenciales de correo en `docker.env` y levantar los servicios.
