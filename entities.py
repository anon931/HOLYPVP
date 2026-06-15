from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

class SanctionType(Enum):
    WARN = "warn"
    KICK = "kick"
    BAN = "ban"
    MUTE = "mute"

class EvidenceStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DENIED = "denied"

@dataclass
class Evidence:
    """
    Entidad de Dominio que representa una evidencia de sanción.
    Independiente de Discord y de la Base de Datos.
    """
    id: str
    player_name: str
    staff_name: str
    reason: str
    type: SanctionType
    evidence_url: str
    timestamp: datetime = field(default_factory=datetime.now)
    status: EvidenceStatus = EvidenceStatus.PENDING
    discord_message_id: Optional[int] = None

@dataclass
class Strike:
    """
    Representa un strike aplicado a una facción o jugador.
    """
    id: int
    target: str
    issuer: str
    reason: str
    points: int
    timestamp: datetime = field(default_factory=datetime.now)
