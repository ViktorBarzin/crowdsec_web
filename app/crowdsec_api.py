import httpx
from typing import List, Dict
import os

API_URL = os.environ["CS_API_URL"]  # e.g http://127.0.0.1:8080/v1
API_KEY = os.environ["CS_API_KEY"]  # cscli bouncers add <bouncer_name>
MACHINE_ID = os.environ["CS_MACHINE_ID"]
PASSWORD = os.environ["CS_MACHINE_PASSWORD"]


async def list_decisions() -> List[Dict]:
    """
    Get all current decisions from CrowdSec API.
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{API_URL}/decisions",
            headers={
                "X-Api-Key": API_KEY,
                "Content-Type": "application/json",
            },
        )
        resp.raise_for_status()
        decisions = resp.json() or []
    decisions = [d for d in decisions if d["origin"] != "CAPI"]
    return decisions


async def delete_decision(ip: str) -> None:
    """
    Delete a decision by IP.
    """
    async with httpx.AsyncClient() as client:
        login = await client.post(
            f"{API_URL}/watchers/login",
            json={
                "machine_id": MACHINE_ID,
                "password": PASSWORD,
            },
            headers={"Content-Type": "application/json"},
        )
        response = login.json()
        token = response["token"]
        resp = await client.delete(
            f"{API_URL}/decisions?ip={ip}", headers={"Authorization": f"Bearer {token}"}
        )
        resp.raise_for_status()
