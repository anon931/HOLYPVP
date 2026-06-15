import asyncio
from src.bot import HolyPvPBot
from src.config import config
from src.infrastructure.logger import bot_logger

async def main():
    """
    Punto de entrada principal para el bot de HolyPvP.
    Inicializa el bot y maneja la ejecución asíncrona.
    """
    # Asegurar que el directorio de logs existe
    import os
    os.makedirs("data/logs", exist_ok=True)
    
    bot = HolyPvPBot()
    
    try:
        await bot_logger.info("dclogs", "Iniciando HolyPvP Bot...")
        async with bot:
            await bot.start(config.DISCORD_TOKEN)
    except KeyboardInterrupt:
        await bot_logger.warning("dclogs", "Bot detenido manualmente.")
    except Exception as e:
        await bot_logger.error("debuglogs", f"Error crítico al iniciar el bot: {e}")
    finally:
        await bot_logger.info("dclogs", "Sistema apagado.")

if __name__ == "__main__":
    asyncio.run(main())
