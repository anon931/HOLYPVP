import discord
from discord import app_commands
from discord.ext import commands
from src.infrastructure.logger import bot_logger
from src.config import config
import time

class Ping(commands.Cog):
    """
    Comando de utilidad para verificar la latencia del bot.
    """
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Muestra la latencia actual del bot.")
    async def ping(self, interaction: discord.Interaction):
        """Maneja el comando slash /ping."""
        try:
            start_time = time.time()
            # Respuesta inicial
            embed = discord.Embed(
                title="🏓 Pong!",
                description="Calculando latencia...",
                color=config.COLORS["main"]
            )
            await interaction.response.send_message(embed=embed)
            
            end_time = time.time()
            api_latency = round(self.bot.latency * 1000)
            round_trip = round((end_time - start_time) * 1000)

            # Actualizar embed con resultados
            updated_embed = discord.Embed(
                title="🏓 Pong!",
                color=config.COLORS["accepted"]
            )
            updated_embed.add_field(name="📡 API Latency", value=f"`{api_latency}ms`", inline=True)
            updated_embed.add_field(name="🔄 Round Trip", value=f"`{round_trip}ms`", inline=True)
            updated_embed.set_footer(text="HolyPvP System | Optimización Senior")
            
            await interaction.edit_original_response(embed=updated_embed)
            await bot_logger.info("cmdlogs", f"Comando /ping ejecutado por {interaction.user}")

        except Exception as e:
            await bot_logger.error("debuglogs", f"Error en comando /ping: {e}")
            await interaction.followup.send("❌ Ha ocurrido un error al procesar el comando.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Ping(bot))
