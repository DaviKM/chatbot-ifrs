from os import getenv
from fastapi import APIRouter, Query, HTTPException, Request
from typing import Optional
from util.log import writeLog
from datetime import datetime


router = APIRouter(prefix="/webhook", tags=["Webhook"])

WHATSAPP_TOKEN = getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = getenv("PHONE_NUMBER_ID")
VERIFY_TOKEN = getenv("VERIFY_TOKEN")
GRAPH_API_URL = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"

@router.get('')
def verify_webhook(
    hub_mode: Optional[str] = Query(None, alias="hub.mode"),
    hub_verify_token: Optional[str] = Query(None, alias="hub.verify_token"),
    hub_challenge: Optional[str] = Query(None, alias="hub.challenge"),
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        writeLog("webhook", "INFO", "Webhook verificado com sucesso", {"data": datetime.now()})
        return hub_challenge
    writeLog("webhook", "ERROR", "Falha ao verificar webhook", {"data": datetime.now()})
    raise HTTPException(status_code=403, detail="Falha ao verificar webhook")

@router.post('')
def receive_message(request: Request):
    body = request.json()
    from_number = body["entry"][0]["messages"][0]["from"]
    content = body["entry"][0]["messages"][0]["text"]["body"]
    type = body["entry"][0]["messages"][0]["type"]
    print(f"Mensagem recebida: {content}")
    if type == "text":
        from src.service.rag_service import query
        resposta = query(content, from_number)
        print(f"Resposta gerada: {resposta}")
        send_message(from_number, resposta)
    
    return {"status": "success"}

def send_message(to_number: str, message: str):
    import requests
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        writeLog("webhook", "ERROR", "Token do WhatsApp ou ID do número de telefone não configurado", {"data": datetime.now()})
        return

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message},
    }

    try:
        response = requests.post(GRAPH_API_URL, headers=headers, json=data)
        response.raise_for_status()
        writeLog("webhook", "INFO", "Mensagem enviada com sucesso", {"to": to_number, "message": message, "data": datetime.now()})
    except requests.exceptions.RequestException as e:
        writeLog("webhook", "ERROR", "Falha ao enviar mensagem", {"to": to_number, "message": message, "error": str(e), "data": datetime.now()})
    