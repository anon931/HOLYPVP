import discord
from discord.ext import commands
from src.config import config
from src.infrastructure.logger import bot_logger
from src.infrastructure.api import start_api
import os
import traceback
import asyncio

class HolyPvPBot(commands.Bot):
    """
    Núcleo del bot de HolyPvP.
    Hereda de commands.Bot y personaliza la carga de Cogs y manejo de eventos.
    """
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )
        self.config = config
        self.api_server = None

    async def setup_hook(self):
        """Carga inicial de extensiones y sincronización de comandos."""
        await bot_logger.info("dclogs", "Iniciando proceso de carga de Cogs...")
        
        # Cargar Cogs de Comandos
        for filename in os.listdir('./src/cogs/commands'):
            if filename.endswith('.py') and not filename.startswith('__'):
                try:
                    await self.load_extension(f'src.cogs.commands.{filename[:-3]}')
                    await bot_logger.info("dclogs", f"Comando cargado: {filename}")
                except Exception as e:
                    await bot_logger.error("debuglogs", f"Error cargando comando {filename}: {traceback.format_exc()}")

        # Cargar Cogs de Eventos
        for filename in os.listdir('./src/cogs/events'):
            if filename.endswith('.py') and not filename.startswith('__'):
                try:
                    await self.load_extension(f'src.cogs.events.{filename[:-3]}')
                    await bot_logger.info("dclogs", f"Evento cargado: {filename}")
                except Exception as e:
                    await bot_logger.error("debuglogs", f"Error cargando evento {filename}: {traceback.format_exc()}")

        # Sincronizar comandos de aplicación
        try:
            synced = await self.tree.sync()
            await bot_logger.info("dclogs", f"Sincronizados {len(synced)} comandos de aplicación.")
        except Exception as e:
            await bot_logger.error("debuglogs", f"Error sincronizando comandos: {e}")

        # Iniciar API de sincronización en segundo plano
        self.api_server = start_api(self)
        asyncio.create_task(self.api_server.serve())
        await bot_logger.info("dclogs", f"API de sincronización iniciada en puerto {config.API_PORT}")

    async def on_ready(self):
        """Evento ejecutado cuando el bot está listo."""
        await bot_logger.info("dclogs", f"Bot conectado como {self.user} (ID: {self.user.id})")
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, 
                name="HolyPvP Community"
            ),
            status=discord.Status.online
        )

    async def on_error(self, event_method, *args, **kwargs):
        """Manejo global de errores de eventos."""
        await bot_logger.error("debuglogs", f"Error en evento {event_method}: {traceback.format_exc()}")

    async def close(self):
        """Cierre limpio del bot y la API."""
        if self.api_server:
            self.api_server.should_exit = True
        await super().close()
