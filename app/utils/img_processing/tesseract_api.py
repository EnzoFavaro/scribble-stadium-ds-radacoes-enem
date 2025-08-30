# Suporte a múltiplos motores OCR
def ocr_with_engine(image_bytes, engine="tesseract"):
    """
    Função unificada para OCR usando Tesseract, EasyOCR, PaddleOCR ou TrOCR.
    Parâmetros:
        image_bytes: bytes da imagem
        engine: 'tesseract', 'easyocr', 'paddleocr', 'trocr'
    Retorna:
        dict com pelo menos a chave 'text'
    """
    import io
    from PIL import Image
    import numpy as np
    result = {"text": "", "engine": engine}
    if engine == "tesseract":
        ocr_engine = TesseractAPI(lang="storysquad")
        low_confidence, content_flagged, text = ocr_engine.transcribe(image_bytes)
        result.update({
            "text": text,
            "low_confidence": low_confidence,
            "content_flagged": content_flagged
        })
        return result
    elif engine == "easyocr":
        try:
            import easyocr
        except ImportError:
            raise RuntimeError("EasyOCR não está instalado. Instale com 'pip install easyocr'.")
        reader = easyocr.Reader(['pt', 'en'])
        # EasyOCR espera caminho ou numpy array
        img = np.array(Image.open(io.BytesIO(image_bytes)))
        out = reader.readtext(img, detail=0, paragraph=True)
        result["text"] = "\n".join(out)
        return result
    elif engine == "paddleocr":
        try:
            from paddleocr import PaddleOCR
        except ImportError:
            raise RuntimeError("PaddleOCR não está instalado. Instale com 'pip install paddleocr'.")
        ocr = PaddleOCR(use_angle_cls=True, lang='pt')
        img = np.array(Image.open(io.BytesIO(image_bytes)).convert("RGB"))
        out = ocr.ocr(img)
        lines = []
        for block in out:
            for line in block:
                lines.append(line[1][0])
        result["text"] = "\n".join(lines)
        return result
    elif engine == "trocr":
        try:
            from transformers import TrOCRProcessor, VisionEncoderDecoderModel
            import torch
        except ImportError:
            raise RuntimeError("Transformers e torch não estão instalados. Instale com 'pip install transformers torch'.")
        processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
        model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        pixel_values = processor(images=img, return_tensors="pt").pixel_values
        generated_ids = model.generate(pixel_values)
        text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        result["text"] = text
        return result
    else:
        raise ValueError(f"Engine '{engine}' não suportada. Use 'tesseract', 'easyocr', 'paddleocr' ou 'trocr'.")
# Adicionando imports necessários para ocr_image
from PIL import Image
import io
import pytesseract
from os.path import dirname

import numpy as np
from cv2 import COLOR_BGR2RGB, IMREAD_COLOR, cvtColor, imdecode
from dotenv import load_dotenv
from pytesseract import image_to_data, image_to_string

# Windows users: uncomment and add local Tesseract path, example below
# This should not be necessary if running through Docker (or for Mac users)
from pytesseract import pytesseract
pytesseract.tesseract_cmd = "C:/Users/22.00774-0/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"

# Get name of directory where this file is located
DIR = dirname(__file__)



class TesseractAPI:
    """
    Interface to Tesseract OCR engine
    Takes single image page and returns transcribed text
    """

    def __init__(self, lang="storysquad"):
    #def __init__(self, lang="por"):
        """
        Arguments:
        Tesseract model (default is 'storysquad')

        Actions:
        Prepares TesseractAPI to handle requests from the endpoints
        """

        # Nenhum serviço cloud é utilizado, apenas modelo local
        self.lang = lang

    def img_preprocess(self, image):
        """
        Arguments:
        Single full-page image

        Actions:
        1. Convert image data bytestring to image object
        2. Convert order of image colors from BGR to RGB

        Returns:
        Full-page processed image
        """

        nparr = np.fromstring(image, np.uint8)
        image_array = imdecode(nparr, IMREAD_COLOR)

        processed_img = cvtColor(image_array, COLOR_BGR2RGB)

        return processed_img

    def extract_data(self, image):
        """
        Arguments:
        Single full-page image

        Actions:
        Extract data on image with Tesseract OCR

        Returns:
        Dictionary with data for:
        1. Content moderation by word: data_dict['text']
        2. Confidence scoring (values are per word): data_dict['conf']
        """

        data_dict = image_to_data(
            image, lang=self.lang, config='', output_type="dict"
        )
        return data_dict

    def extract_text(self, image):
        """
        Arguments:
        Single full-page image

        Actions:
        Extract text from image with Tesseract OCR

        Returns:
        Transcribed text (string)
        """

        text = image_to_string(image, lang=self.lang, config='')
        return text

    # Removido: moderação de conteúdo baseada em lista de palavras, pois não pode depender de recursos externos
    def word_moderation(self, data_dict):
        return False

    def confidence_flag(self, data_dict):
        """
        Arguments:
        Data dictionary generated by Tesseract from extract_data method

        Actions:
        Calculate mean confidence for entire page

        Returns:
        Low confidence flag (T/F)
        """

        confidence_list = list(map(int, data_dict["conf"]))
        page_confidence = sum(confidence_list) / len(confidence_list) / 100

        return page_confidence < 0.85

    def transcribe(self, image):
        """
        Arguments:
        Single full-page image

        Actions:
        1. Preprocesses image
        2. Extract text
        3. Get confidence

        Returns:
        1. Transcribed text (string)
        2. Bad content flag (sempre False)
        3. Low confidence flag (T/F)
        """

        features = self.img_preprocess(image)
        text = self.extract_text(features)
        data_dict = self.extract_data(features)
        content_flagged = False
        low_confidence = self.confidence_flag(data_dict)

        return low_confidence, content_flagged, text
    
    def ocr_image(image_bytes, engine="tesseract"):
        image = Image.open(io.BytesIO(image_bytes))
        if engine == "tesseract":
            return pytesseract.image_to_string(image)
        # Adicione suporte para engine customizada aqui, se necessário
        raise NotImplementedError("Only Tesseract engine is supported.")
