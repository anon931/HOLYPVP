from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from src.config import config
from src.services.evidence_service import EvidenceService
import uvicorn
import asyncio

app = FastAPI(title="HolyPvP In-Game Sync API")

class EvidencePayload(BaseModel):
    id: str
    player_name: str
    staff_name: str
    reason: str
    type: str # warn, kick, ban, mute
    evidence_url: str

class StatusUpdatePayload(BaseModel):
    id: str
    status: str # accepted, denied

# Dependencia para verificar API KEY
async def verify_token(x_api_key: str = Header(...)):
    if x_api_key != config.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key

# Referencia al bot (se inyectará al iniciar)
bot_instance = None

@app.post("/evidences/new", dependencies=[Depends(verify_token)])
async def create_evidence(payload: EvidencePayload):
    if not bot_instance:
        raise HTTPException(status_code=503, detail="Bot not ready")
    
    service = EvidenceService(bot_instance)
    # Ejecutar en el event loop del bot
    asyncio.run_coroutine_threadsafe(
        service.post_evidence(payload.dict()), 
        bot_instance.loop
    )
    return {"status": "success", "message": "Evidence received"}

@app.post("/evidences/update", dependencies=[Depends(verify_token)])
async def update_status(payload: StatusUpdatePayload):
    if not bot_instance:
        raise HTTPException(status_code=503, detail="Bot not ready")
    
    service = EvidenceService(bot_instance)
    asyncio.run_coroutine_threadsafe(
        service.update_evidence_status(payload.id, payload.status),
        bot_instance.loop
    )
    return {"status": "success", "message": "Status update received"}

def start_api(bot):
    global bot_instance
    bot_instance = bot
    config_uvicorn = uvicorn.Config(app, host="0.0.0.0", port=config.API_PORT, log_level="info")
    server = uvicorn.Server(config_uvicorn)
    return server
