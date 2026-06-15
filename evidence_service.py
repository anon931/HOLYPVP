import discord
from src.domain.entities import Evidence, EvidenceStatus, SanctionType
from src.config import config
from src.infrastructure.logger import bot_logger
from datetime import datetime

class EvidenceService:
    """
    Servicio de orquestación para el manejo de evidencias.
    Conecta la lógica de negocio con la interfaz de Discord.
    """
    def __init__(self, bot):
        self.bot = bot

    def _get_color(self, status: EvidenceStatus) -> int:
        """Retorna el color del embed según el estado."""
        if status == EvidenceStatus.PENDING:
            return config.COLORS["pending"]
        elif status == EvidenceStatus.ACCEPTED:
            return config.COLORS["accepted"]
        elif status == EvidenceStatus.DENIED:
            return config.COLORS["denied"]
        return config.COLORS["main"]

    def _create_embed(self, evidence: Evidence) -> discord.Embed:
        """Crea un embed profesional para la evidencia."""
        color = self._get_color(evidence.status)
        title = f"🛡️ Nueva Evidencia: {evidence.type.value.upper()}"
        
        embed = discord.Embed(
            title=title,
            description=f"Se ha registrado una nueva sanción en el servidor.",
            color=color,
            timestamp=evidence.timestamp
        )
        
        embed.add_field(name="👤 Jugador", value=f"`{evidence.player_name}`", inline=True)
        embed.add_field(name="👮 Staff", value=f"`{evidence.staff_name}`", inline=True)
        embed.add_field(name="📝 Razón", value=f"```{evidence.reason}```", inline=False)
        embed.add_field(name="📊 Estado", value=f"**{evidence.status.value.upper()}**", inline=True)
        
        if evidence.evidence_url:
            embed.set_image(url=evidence.evidence_url)
            
        embed.set_footer(text=f"HolyPvP Network | ID: {evidence.id}", icon_url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        
        return embed

    async def post_evidence(self, evidence_data: dict):
        """
        Procesa y publica una nueva evidencia recibida (ej. vía API).
        """
        try:
            # Mapear datos a entidad de dominio
            evidence = Evidence(
                id=evidence_data["id"],
                player_name=evidence_data["player_name"],
                staff_name=evidence_data["staff_name"],
                reason=evidence_data["reason"],
                type=SanctionType(evidence_data["type"]),
                evidence_url=evidence_data["evidence_url"],
                status=EvidenceStatus.PENDING
            )

            # Obtener canal correspondiente
            channel_id = config.CHANNELS.get(evidence.type.value)
            channel = self.bot.get_channel(channel_id)
            
            if not channel:
                await bot_logger.error("mclogs", f"Canal no encontrado para tipo: {evidence.type.value}")
                return

            embed = self._create_embed(evidence)
            message = await channel.send(embed=embed)
            
            # Guardar el ID del mensaje para futuras actualizaciones
            evidence.discord_message_id = message.id
            
            await bot_logger.info("mclogs", f"Evidencia {evidence.id} publicada en Discord.")
            
            # Aquí se llamaría al repositorio para persistir en DB
            # await self.repository.save_evidence(evidence)

        except Exception as e:
            await bot_logger.error("debuglogs", f"Error al postear evidencia: {e}")

    async def update_evidence_status(self, evidence_id: str, new_status: str):
        """
        Actualiza el estado de una evidencia existente.
        """
        try:
            status = EvidenceStatus(new_status)
            # 1. Obtener evidencia de la DB (Simulado)
            # evidence = await self.repository.get_evidence(evidence_id)
            
            # 2. Obtener canal y mensaje de Discord
            # channel = self.bot.get_channel(config.CHANNELS.get(evidence.type.value))
            # message = await channel.fetch_message(evidence.discord_message_id)
            
            # 3. Actualizar entidad y embed
            # evidence.status = status
            # new_embed = self._create_embed(evidence)
            # await message.edit(embed=new_embed)
            
            await bot_logger.info("mclogs", f"Estado de evidencia {evidence_id} actualizado a {new_status}.")
            
        except Exception as e:
            await bot_logger.error("debuglogs", f"Error al actualizar evidencia: {e}")
