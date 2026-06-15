import os

def create_project():
    # Estructura de carpetas
    folders = [
        "src/domain",
        "src/infrastructure",
        "src/services",
        "src/cogs/commands",
        "src/cogs/events",
        "src/utils",
        "src/cfg",
        "data/bkp",
        "data/logs/dclogs",
        "data/logs/mclogs",
        "data/logs/cmdlogs",
        "data/logs/debuglogs"
    ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"Created folder: {folder}")

    # Archivos y su contenido
    files = {
        ".env": """# HolyPvP Bot Configuration
DISCORD_TOKEN=your_discord_bot_token_here
GUILD_ID=your_guild_id_here

# API Configuration for In-Game Sync
API_PORT=8080
API_KEY=your_secure_api_key_here

# Database Configuration
DATABASE_URL=sqlite+aiosqlite:///data/holypvp.db

# Logging Configuration
LOG_LEVEL=INFO
""",
        "requirements.txt": """discord.py
pydantic
pydantic-settings
python-dotenv
fastapi
uvicorn
sqlalchemy
aiosqlite
aiofiles
python-decouple
""",
        "src/config.py": """import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Config(BaseSettings):
    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "")
    GUILD_ID: int = int(os.getenv("GUILD_ID", 0))
    API_PORT: int = int(os.getenv("API_PORT", 8080))
    API_KEY: str = os.getenv("API_KEY", "secret_key")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data/holypvp.db")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    CHANNELS: dict = {"warn": 0, "kick": 0, "ban": 0, "mute": 0}
    COLORS: dict = {"pending": 0x808080, "accepted": 0x00FF00, "denied": 0xFF0000, "main": 0x2F3136}

config = Config()
""",
        "src/domain/entities.py": """from dataclasses import dataclass, field
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
    id: str
    player_name: str
    staff_name: str
    reason: str
    type: SanctionType
    evidence_url: str
    timestamp: datetime = field(default_factory=datetime.now)
    status: EvidenceStatus = EvidenceStatus.PENDING
    discord_message_id: Optional[int] = None
""",
        "src/infrastructure/logger.py": """import logging
import sys
import os
from datetime import datetime
import aiofiles

class AsyncLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    async def _write_to_file(self, category: str, message: str):
        log_dir = f"data/logs/{category}"
        os.makedirs(log_dir, exist_ok=True)
        file_path = f"{log_dir}/{datetime.now().strftime('%Y-%m-%d')}.log"
        async with aiofiles.open(file_path, mode='a', encoding='utf-8') as f:
            await f.write(f"{datetime.now()} | {message}\\n")

    async def info(self, category: str, message: str):
        self.logger.info(f"[{category}] {message}")
        await self._write_to_file(category, f"INFO: {message}")

    async def error(self, category: str, message: str):
        self.logger.error(f"[{category}] {message}")
        await self._write_to_file(category, f"ERROR: {message}")

bot_logger = AsyncLogger("HolyPvP")
""",
        "src/services/evidence_service.py": """import discord
from src.domain.entities import Evidence, EvidenceStatus, SanctionType
from src.config import config
from src.infrastructure.logger import bot_logger

class EvidenceService:
    def __init__(self, bot):
        self.bot = bot

    def _get_color(self, status: EvidenceStatus) -> int:
        colors = {EvidenceStatus.PENDING: config.COLORS["pending"], 
                  EvidenceStatus.ACCEPTED: config.COLORS["accepted"], 
                  EvidenceStatus.DENIED: config.COLORS["denied"]}
        return colors.get(status, config.COLORS["main"])

    async def post_evidence(self, data: dict):
        try:
            evidence = Evidence(id=data["id"], player_name=data["player_name"], 
                                staff_name=data["staff_name"], reason=data["reason"], 
                                type=SanctionType(data["type"]), evidence_url=data["evidence_url"])
            channel = self.bot.get_channel(config.CHANNELS.get(evidence.type.value))
            if channel:
                embed = discord.Embed(title=f"🛡️ Nueva Evidencia: {evidence.type.value.upper()}", 
                                      color=self._get_color(evidence.status))
                embed.add_field(name="👤 Jugador", value=f"`{evidence.player_name}`")
                embed.add_field(name="👮 Staff", value=f"`{evidence.staff_name}`")
                embed.set_image(url=evidence.evidence_url)
                await channel.send(embed=embed)
        except Exception as e:
            await bot_logger.error("debuglogs", f"Error: {e}")
""",
        "src/infrastructure/api.py": """from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from src.config import config
from src.services.evidence_service import EvidenceService
import uvicorn
import asyncio

app = FastAPI()
bot_instance = None

class EvidencePayload(BaseModel):
    id: str
    player_name: str
    staff_name: str
    reason: str
    type: str
    evidence_url: str

@app.post("/evidences/new")
async def create_evidence(payload: EvidencePayload):
    if not bot_instance: raise HTTPException(status_code=503)
    service = EvidenceService(bot_instance)
    asyncio.run_coroutine_threadsafe(service.post_evidence(payload.dict()), bot_instance.loop)
    return {"status": "success"}

def start_api(bot):
    global bot_instance
    bot_instance = bot
    config_uv = uvicorn.Config(app, host="0.0.0.0", port=config.API_PORT)
    return uvicorn.Server(config_uv)
""",
        "src/bot.py": """import discord
from discord.ext import commands
from src.config import config
from src.infrastructure.logger import bot_logger
from src.infrastructure.api import start_api
import os
import asyncio

class HolyPvPBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())
        self.api_server = None

    async def setup_hook(self):
        for root, dirs, files in os.walk("./src/cogs"):
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file).replace("./", "").replace("/", ".").replace(".py", "")
                    await self.load_extension(path)
        self.api_server = start_api(self)
        asyncio.create_task(self.api_server.serve())

    async def on_ready(self):
        await bot_logger.info("dclogs", f"Bot {self.user} listo.")
""",
        "main.py": """import asyncio
from src.bot import HolyPvPBot

async def main():
    bot = HolyPvPBot()
    async with bot:
        await bot.start("YOUR_TOKEN")

if __name__ == "__main__":
    asyncio.run(main())
""",
        "src/cogs/commands/ping.py": """import discord
from discord import app_commands
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot): self.bot = bot
    @app_commands.command(name="ping")
    async def ping(self, itx): await itx.response.send_message(f"Pong! {round(self.bot.latency*1000)}ms")

async def setup(bot): await bot.add_cog(Ping(bot))
"""
    }

    for path, content in files.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created file: {path}")

    print("\\n✅ HolyPvP Bot Project successfully built!")

if __name__ == "__main__":
    create_project()
"""}-->(content truncated)---
Page HTML was not saved to sandbox storage, use another tool if you want to perform DOM analysis
