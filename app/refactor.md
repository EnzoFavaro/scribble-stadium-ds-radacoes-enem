# refactor.md

## Objetivo

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


---

## 10. Prompts para o GPT te ajudar no refactor

Use os prompts abaixo para pedir ajuda ao GPT durante o processo de refatoração:

- **Para remover endpoints antigos:**  
  "Analise todo o código da pasta `app/` e seus subdiretórios. Liste detalhadamente todos os endpoints atualmente implementados, indicando o arquivo e a função correspondente. Em seguida, gere um plano de modificação e o código necessário para remover completamente todos os endpoints, modelos, rotas e dependências que não sejam essenciais para um único endpoint POST `/ocr` que recebe uma imagem e retorna o texto transcrito usando a engine Tesseract (mantendo suporte a engine customizada, se houver). Certifique-se de atualizar ou remover arquivos, imports, dependências e testes conforme necessário, deixando o projeto enxuto, funcional e pronto para uso apenas como microserviço de OCR. Forneça instruções claras para aplicar as mudanças e garanta que o resultado final seja um código limpo, organizado e fácil de manter."

- **Para criar o novo endpoint:**  
  "Implemente um endpoint FastAPI `/ocr` em `main.py` (ou arquivo principal), que recebe uma imagem via multipart/form-data e retorna o texto transcrito usando a engine Tesseract. O endpoint deve ser seguro, eficiente e seguir boas práticas de desenvolvimento Python. Forneça o código completo e explique como integrá-lo ao projeto."

- **Para adaptar a função de OCR:**  
  "Adapte ou crie uma função em `utils/img_processing/tesseract_api.py` que receba bytes de uma imagem (por exemplo, de um UploadFile do FastAPI) e retorne o texto transcrito usando Tesseract. Certifique-se de que a função seja robusta, trate erros comuns e permita a escolha de uma engine customizada, se necessário. Forneça exemplos de uso."

- **Para adicionar suporte a engine customizada:**  
  "Adicione ao endpoint `/ocr` um parâmetro opcional que permita ao usuário escolher uma engine customizada do Tesseract (por exemplo, passando o nome do modelo treinado). Explique como modificar tanto o endpoint quanto a função de OCR para suportar essa funcionalidade, garantindo flexibilidade e segurança."

- **Para limpar dependências:**  
  "Analise o arquivo de dependências do projeto (`requirements.txt` ou `Pipfile`) e liste todas as bibliotecas que podem ser removidas após a refatoração para um microserviço de OCR. Explique como atualizar o arquivo de dependências e garantir que apenas o necessário para FastAPI, Tesseract e manipulação de imagens permaneça."

- **Para organizar o projeto:**  
  "Sugira e explique a estrutura final de pastas e arquivos para o microserviço de OCR, considerando boas práticas de organização de projetos Python e FastAPI. Indique onde cada componente (endpoint, função de OCR, testes, etc.) deve ficar e justifique suas escolhas."

---