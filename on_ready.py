import discord
from discord.ext import commands
from src.infrastructure.logger import bot_logger

class OnReady(commands.Cog):
    """
    Manejador del evento on_ready para lógica adicional al conectar.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Lógica ejecutada cuando el bot está listo."""
        # Nota: La lógica principal ya está en bot.py, esto es para extensiones adicionales.
        await bot_logger.info("dclogs", f"Extensión de Evento OnReady cargada correctamente.")

async def setup(bot):
    await bot.add_cog(OnReady(bot))
