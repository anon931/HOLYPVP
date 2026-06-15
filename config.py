import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Config(BaseSettings):
    """
    Gestor centralizado de configuración para HolyPvP Bot.
    Utiliza Pydantic para validación de datos y tipos.
    """
    # Discord
    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "")
    GUILD_ID: int = int(os.getenv("GUILD_ID", 0))
    
    # API para sincronización In-Game
    API_PORT: int = int(os.getenv("API_PORT", 8080))
    API_KEY: str = os.getenv("API_KEY", "secret_key")
    
    # Base de Datos
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data/holypvp.db")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Canales de Evidencias (IDs de ejemplo, deben configurarse)
    CHANNELS: dict = {
        "warn": 0,
        "kick": 0,
        "ban": 0,
        "mute": 0
    }

    # Colores de Embeds
    COLORS: dict = {
        "pending": 0x808080, # Gris
        "accepted": 0x00FF00, # Verde
        "denied": 0xFF0000,   # Rojo
        "main": 0x2F3136      # Color principal oscuro
    }

config = Config()
