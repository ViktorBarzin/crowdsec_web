from fastapi import APIRouter, HTTPException
from app.crowdsec_api import list_decisions, delete_decision

router = APIRouter()


@router.get("/decisions")
async def get_decisions():
    try:
        decisions = await list_decisions()
        return {"decisions": decisions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/decisions/{ip}")
async def remove_decision(ip: str):
    try:
        await delete_decision(ip)
        return {"status": "deleted", "ip": ip}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
