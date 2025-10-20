#!/bin/bash

# Script para probar el sistema de correos en Docker

echo "🚀 Probando el sistema de correos en Docker..."

# Verificar que Docker esté corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker no está corriendo. Por favor inicia Docker primero."
    exit 1
fi

# Verificar que el archivo docker.env existe
if [ ! -f "docker.env" ]; then
    echo "❌ Archivo docker.env no encontrado."
    echo "Por favor crea el archivo docker.env con la configuración de correo."
    exit 1
fi

echo "📧 Verificando configuración de correo en docker.env..."

# Verificar variables de correo
if grep -q "your_email@gmail.com" docker.env; then
    echo "⚠️  ADVERTENCIA: Aún tienes valores de ejemplo en docker.env"
    echo "   Por favor configura tus credenciales reales de correo en docker.env"
    echo ""
    echo "   Variables que necesitas cambiar:"
    echo "   - MAIL_USERNAME"
    echo "   - MAIL_PASSWORD"
    echo "   - MAIL_FROM"
    echo ""
    read -p "¿Quieres continuar con los valores de ejemplo? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Configuración cancelada. Edita docker.env y vuelve a ejecutar este script."
        exit 1
    fi
fi

echo "🔨 Construyendo la imagen de Docker..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "❌ Error construyendo la imagen de Docker"
    exit 1
fi

echo "🚀 Iniciando los servicios..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ Error iniciando los servicios"
    exit 1
fi

echo "⏳ Esperando que los servicios estén listos..."
sleep 10

echo "🧪 Probando el sistema de correos..."

# Ejecutar el script de prueba dentro del contenedor
docker-compose exec app python test_email_system.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ ¡Prueba exitosa! El sistema de correos está funcionando."
    echo ""
    echo "📋 Para probar manualmente:"
    echo "   1. Ve a http://localhost:8000/docs"
    echo "   2. Autentícate con un usuario"
    echo "   3. Crea una orden de compra o venta"
    echo "   4. Verifica que llegue el correo de confirmación"
    echo ""
    echo "🛑 Para detener los servicios: docker-compose down"
else
    echo ""
    echo "❌ La prueba falló. Revisa los logs:"
    echo "   docker-compose logs app"
fi
