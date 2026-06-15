import os
import tarfile
from datetime import datetime
from src.infrastructure.logger import bot_logger
import asyncio

class BackupManager:
    """
    Gestiona backups automáticos de la base de datos y logs.
    """
    @staticmethod
    async def create_backup():
        """Crea un archivo .tar.gz con la base de datos y logs."""
        try:
            date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            backup_dir = f"data/bkp/{datetime.now().strftime('%Y-%m-%d')}"
            os.makedirs(backup_dir, exist_ok=True)
            
            backup_path = f"{backup_dir}/backup_{date_str}.tar.gz"
            
            # Ejecutar tar en un hilo separado para no bloquear el event loop
            def perform_backup():
                with tarfile.open(backup_path, "w:gz") as tar:
                    if os.path.exists("data/holypvp.db"):
                        tar.add("data/holypvp.db", arcname="holypvp.db")
                    if os.path.exists("data/logs"):
                        tar.add("data/logs", arcname="logs")
            
            await asyncio.to_thread(perform_backup)
            await bot_logger.info("dclogs", f"Backup creado exitosamente: {backup_path}")
            return backup_path

        except Exception as e:
            await bot_logger.error("debuglogs", f"Error al crear backup: {e}")
            return None
