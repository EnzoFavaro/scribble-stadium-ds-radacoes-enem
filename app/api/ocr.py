

from fastapi import APIRouter, File, UploadFile, HTTPException, status, Depends
from app.utils.img_processing.tesseract_api import TesseractAPI, ocr_with_engine
import logging

router = APIRouter()

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ocr-endpoint")



@router.post("/ocr")
async def ocr_endpoint(
    file: UploadFile = File(...),
    engine: str = "tesseract"
):
    logger.info(f"Recebendo arquivo: filename={file.filename}, content_type={file.content_type}, engine={engine}")
    if not file.content_type or not file.content_type.startswith("image/"):
        logger.warning("Arquivo enviado não é uma imagem.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arquivo enviado deve ser uma imagem."
        )
    try:
        image_bytes = await file.read()
        logger.info(f"Tamanho do arquivo recebido: {len(image_bytes)} bytes")
        result = ocr_with_engine(image_bytes, engine)
        logger.info(f"Transcrição realizada com sucesso usando engine {engine}.")
        return result
    except Exception as e:
        logger.error(f"Erro ao processar imagem: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar imagem."
        )
