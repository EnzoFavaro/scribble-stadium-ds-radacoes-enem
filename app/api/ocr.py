

from fastapi import APIRouter, File, UploadFile, HTTPException, status, Depends
from app.utils.img_processing.tesseract_api import TesseractAPI

router = APIRouter()

def get_ocr_engine():
    return TesseractAPI(lang="storysquad")

@router.post("/ocr")
async def ocr_endpoint(
    file: UploadFile = File(...),
    ocr_engine: TesseractAPI = Depends(get_ocr_engine)
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arquivo enviado deve ser uma imagem."
        )
    try:
        image_bytes = await file.read()
        low_confidence, content_flagged, text = ocr_engine.transcribe(image_bytes)
        return {
            "text": text,
            "low_confidence": low_confidence,
            "content_flagged": content_flagged
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar imagem."
        )
