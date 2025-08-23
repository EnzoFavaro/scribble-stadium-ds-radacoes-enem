from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.ocr import router as ocr_router
import uvicorn

app = FastAPI(title="OCR Microservice")
app.include_router(ocr_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app)