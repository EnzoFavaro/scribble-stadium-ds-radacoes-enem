---
applyTo: '**'
---
Provide project context and coding guidelines that AI should follow when generating code, answering questions, or reviewing changes.## Objetivo

Refatorar a API para que ela tenha apenas um endpoint POST `/ocr`, que recebe uma imagem (upload) e retorna o texto transcrito usando a engine Tesseract (mantendo a possibilidade de usar uma engine customizada treinada).

---

## 1. Análise da Estrutura Atual

- **Endpoints**: Diversos endpoints para submissão de textos, ilustrações, visualizações, clustering, etc.
- **Dependências**: Uso de FastAPI, Pydantic, Tesseract, Google Vision API, e outros módulos auxiliares.
- **Organização**: Código modularizado em `api/`, `utils/`, e `tests/`.
- **OCR**: Implementações de OCR em `utils/img_processing/tesseract_api.py` e possivelmente integração com Google Vision em `google_api.py`.

---

## 2. Componentes a Serem Mantidos

- **FastAPI**: Para servir o endpoint.
- **Tesseract API**: Toda a lógica de OCR baseada em Tesseract, incluindo suporte a engine customizada.
- **Validação básica**: Apenas para o upload da imagem.

---

## 3. Componentes a Serem Removidos

- Todos os endpoints e modelos relacionados a:
  - Submissão de textos e ilustrações
  - Visualizações (histogramas, nuvens de palavras, etc)
  - Clustering e moderação
  - Banco de dados e autenticação
- Toda lógica de banco de dados, autenticação, e integração com Google Vision (exceto se desejar manter como fallback).

---

## 4. Novo Fluxo da API

1. **POST `/ocr`**
   - Recebe um arquivo de imagem (formato: multipart/form-data).
   - (Opcional) Parâmetro para escolher engine customizada.
   - Processa a imagem usando Tesseract.
   - Retorna JSON com o texto extraído.

---

## 5. Passos de Refatoração

### 5.1. Limpeza de Código

- Remover todos os arquivos e funções não relacionados ao OCR.
- Manter apenas o necessário para rodar FastAPI e Tesseract.

### 5.2. Novo Endpoint

- Criar um endpoint `/ocr` em `main.py` (ou novo arquivo).
- Usar FastAPI `UploadFile` para receber a imagem.
- Chamar função de OCR do Tesseract (de `utils/img_processing/tesseract_api.py`).
- Retornar o texto extraído em JSON.

### 5.3. Ajuste de Dependências

- Remover dependências não utilizadas no `requirements.txt` ou `Pipfile`.

### 5.4. Testes

- Criar testes unitários para o endpoint `/ocr` e para a função de OCR.

---

## 6. Exemplo de Novo Endpoint

```python
# main.py
from fastapi import FastAPI, File, UploadFile
from utils.img_processing.tesseract_api import ocr_image  # ajuste conforme a função real

app = FastAPI()

@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    text = ocr_image(contents)  # ajuste conforme assinatura real
    return {"text": text}
```

---

## 7. Organização Sugerida

```
app/
  main.py
  utils/
    img_processing/
      tesseract_api.py
tests/
  test_ocr.py
```

---

## 8. Observações

- Se quiser manter a opção de engine customizada, adicione um parâmetro opcional no endpoint.
- Documente o endpoint na raiz do projeto.
- Remova arquivos e pastas obsoletos para simplificar manutenção.

---

## 9. Checklist

- [ ] Remover endpoints/modelos desnecessários
- [ ] Manter apenas lógica de OCR
- [ ] Criar endpoint `/ocr`
- [ ] Ajustar dependências
- [ ] Testar a API

