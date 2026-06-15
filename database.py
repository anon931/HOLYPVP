from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from src.config import config
from src.domain.entities import EvidenceStatus, SanctionType
from datetime import datetime

Base = declarative_base()

class EvidenceModel(Base):
    """Modelo de base de datos para las evidencias."""
    __tablename__ = "evidences"
    
    id = Column(String, primary_key=True)
    player_name = Column(String, nullable=False)
    staff_name = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    type = Column(SQLEnum(SanctionType), nullable=False)
    evidence_url = Column(String)
    status = Column(SQLEnum(EvidenceStatus), default=EvidenceStatus.PENDING)
    discord_message_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.now)

class Database:
    """Gestor de conexión a la base de datos asíncrona."""
    def __init__(self):
        self.engine = create_async_engine(config.DATABASE_URL, echo=False)
        self.async_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def create_tables(self):
        """Crea las tablas si no existen."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_session(self) -> AsyncSession:
        return self.async_session()

db = Database()
