from datetime import datetime
import logging
from pythonjsonlogger import json
import os


def getLogger(loggerName : str) -> logging.Logger:
    logger = logging.getLogger(loggerName)

    diretorio= os.path.join('logs', loggerName)
    os.makedirs(diretorio, exist_ok=True)

    if logger.handlers:
        return logger

    formatter = json.JsonFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', json_ensure_ascii=False)
    handler = logging.FileHandler(os.path.join(diretorio, datetime.now().strftime("%d-%m-%Y") + '.jsonl'), encoding="utf-8")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger

def ragLog(nivel: str, mensagem : str, fields: dict = None):
    try:
        logger = getLogger("RAG")
        nivel = nivel.strip().upper()
        extra = {
            "extra": fields
        } if fields else None

        if nivel == "WARNING":
            logger.warning(mensagem, extra=extra)
        elif nivel == "INFO":
            print(nivel)
            logger.info(mensagem, extra=extra)
        elif nivel == "DEBUG":
            logger.debug(mensagem, extra=extra)
        elif nivel == "ERROR":
            logger.error(mensagem, extra=extra)
        elif nivel == "CRITICAL":
            logger.critical(mensagem, extra=extra)
        else:
            print(f"{nivel} não é um levelname válido")
    except Exception as e:
        print(e)
        return str(e)

#ragLog('critical  ', "teste 1")
