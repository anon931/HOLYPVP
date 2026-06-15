import logging
import sys
import os
from datetime import datetime
import aiofiles
import asyncio

class AsyncLogger:
    """
    Sistema de logging segmentado y asíncrono.
    Maneja múltiples archivos de log sin bloquear el event loop.
    """
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Formato profesional
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Handler para consola
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    async def _write_to_file(self, category: str, message: str):
        """Escribe el mensaje de log en el archivo correspondiente de forma asíncrona."""
        log_dir = f"data/logs/{category}"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
            
        file_path = f"{log_dir}/{datetime.now().strftime('%Y-%m-%d')}.log"
        
        async with aiofiles.open(file_path, mode='a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            await f.write(f"{timestamp} | {message}\n")
        
        # También escribir en el log general
        async with aiofiles.open("data/logs/console.log", mode='a', encoding='utf-8') as f:
            await f.write(f"{timestamp} | {category.upper()} | {message}\n")

    async def info(self, category: str, message: str):
        self.logger.info(f"[{category}] {message}")
        await self._write_to_file(category, f"INFO: {message}")

    async def error(self, category: str, message: str):
        self.logger.error(f"[{category}] {message}")
        await self._write_to_file(category, f"ERROR: {message}")

    async def debug(self, category: str, message: str):
        self.logger.debug(f"[{category}] {message}")
        await self._write_to_file(category, f"DEBUG: {message}")

    async def warning(self, category: str, message: str):
        self.logger.warning(f"[{category}] {message}")
        await self._write_to_file(category, f"WARNING: {message}")

# Instancia global para el bot
bot_logger = AsyncLogger("HolyPvP")
