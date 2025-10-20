# Andina Trading Backend - Docker Setup

Este proyecto es un backend de FastAPI para el sistema de trading de Andina, completamente dockerizado.

## 🚀 Inicio Rápido

### Prerrequisitos
- Docker
- Docker Compose

### Ejecutar la aplicación

1. **Clonar el repositorio** (si no lo has hecho ya)
```bash
git clone <repository-url>
cd Auth-JWT-ms
```

2. **Levantar los servicios**
```bash
docker-compose up --build -d
```

3. **Verificar que los servicios estén corriendo**
```bash
docker ps
```

4. **Acceder a la documentación de la API**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📋 Servicios

### Base de Datos MySQL
- **Puerto**: 3306
- **Usuario**: root
- **Contraseña**: 1234
- **Base de datos**: andina_trading

### Aplicación FastAPI
- **Puerto**: 8000
- **URL**: http://localhost:8000

## 🛠️ Comandos Útiles

### Ver logs de la aplicación
```bash
docker logs andina_trading_app
```

### Ver logs de la base de datos
```bash
docker logs andina_trading_mysql
```

### Detener los servicios
```bash
docker-compose down
```

### Detener y eliminar volúmenes (⚠️ Esto eliminará los datos)
```bash
docker-compose down -v
```

### Reconstruir la aplicación
```bash
docker-compose up --build -d
```

## 📁 Estructura del Proyecto

```
├── src/
│   └── app/
│       ├── application/     # Lógica de aplicación
│       ├── domain/         # Entidades y repositorios
│       └── infrastructure/ # Implementaciones concretas
├── database/
│   └── script.sql         # Script de inicialización de BD
├── Dockerfile            # Configuración del contenedor de la app
├── docker-compose.yml    # Orquestación de servicios
├── docker.env           # Variables de entorno
└── requirements.txt     # Dependencias de Python
```

## 🔧 Configuración

### Variables de Entorno
Las variables de entorno están configuradas en `docker.env`:

- `MYSQL_HOST`: mysql
- `MYSQL_PORT`: 3306
- `MYSQL_USER`: root
- `MYSQL_PASSWORD`: 1234
- `MYSQL_DATABASE`: andina_trading

### Base de Datos
La base de datos se inicializa automáticamente con el script `database/script.sql` que incluye:
- Creación de tablas
- Datos de prueba
- Usuarios por defecto

## 🧪 Testing

### Probar la API
```bash
# Verificar que la API responde
curl http://localhost:8000/docs

# Probar un endpoint específico
curl http://localhost:8000/openapi.json
```

### Usuarios de Prueba
- **Usuario**: admin
- **Contraseña**: 1234 (hasheada en la BD)

## 🐛 Troubleshooting

### Problema: MySQL no inicia
```bash
# Verificar logs
docker logs andina_trading_mysql

# Reiniciar solo MySQL
docker-compose restart mysql
```

### Problema: Aplicación no responde
```bash
# Verificar logs
docker logs andina_trading_app

# Verificar conectividad de red
docker network ls
```

### Problema: Puerto ocupado
Si el puerto 8000 o 3306 están ocupados, modifica los puertos en `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Cambiar puerto externo
```

## 📝 Notas

- La aplicación se ejecuta en modo desarrollo con auto-reload
- Los datos de la base de datos persisten en un volumen Docker
- El contenedor de la aplicación se reconstruye automáticamente cuando hay cambios en el código
