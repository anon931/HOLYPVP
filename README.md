# 🛡️ HolyPvP Discord Bot

Bot multipropósito de alto rendimiento diseñado para el servidor de Minecraft **HolyPvP**. Construido con una arquitectura modular de tres capas (Hexagonal) para máxima escalabilidad y seguridad.

## 🚀 Características Principales

- **Arquitectura Hexagonal**: Separación clara entre Dominio, Infraestructura y Servicios.
- **Sincronización In-Game**: API integrada (FastAPI) para recibir evidencias de sanciones en tiempo real desde Minecraft.
- **Sistema de Evidencias**: Gestión automatizada de Warns, Kicks, Bans y Mutes con actualización dinámica de estados (colores).
- **Logging Asíncrono**: Sistema de logs segmentado por categorías sin bloqueo del Event Loop.
- **Backups Automáticos**: Utilidad integrada para respaldos de base de datos y logs.
- **Comandos Modernos**: Uso exclusivo de Slash Commands y componentes interactivos.

## 📁 Estructura del Proyecto

```text
HOLYPVP/
├── main.py                 # Punto de entrada
├── src/
│   ├── bot.py              # Núcleo del bot
│   ├── config.py           # Configuración centralizada
│   ├── domain/             # Entidades y reglas de negocio
│   ├── infrastructure/     # API, DB, Logger (Adaptadores)
│   ├── services/           # Lógica de orquestación
│   ├── cogs/               # Comandos y Eventos de Discord
│   └── utils/              # Herramientas transversales
└── data/                   # DB, Logs y Backups
```

## 🛠️ Instalación

1. Clonar el repositorio.
2. Instalar dependencias: `pip install -r requirements.txt`
3. Configurar el archivo `.env` con tus credenciales.
4. Ejecutar: `python main.py`

## 🛡️ Seguridad y Auditoría

Este bot implementa chequeos estrictos de permisos y sanitización de entradas. El sistema de logs permite una trazabilidad completa de todas las acciones administrativas.

---
**Desarrollado para HolyPvP Network**
