# Projeto de Análise de Algodão 🌾

## Objetivo

Explorar os dados históricos de plantio e variáveis climáticas para responder:

1. Quais são os melhores períodos para o plantio do algodão?
2. Quais são as melhores regiões para o plantio?
3. Relações entre variáveis climáticas e área plantada.

## Estrutura do Projeto

- **`data/`**: Dados brutos e processados.
- **`src/`**: Código-fonte para limpeza, análise e visualização.
- **`app.py`**: Aplicação Streamlit interativa.

## Instruções para Uso

### Localmente

1. Clone o repositório:

   ```bash
   git clone <repo-url>
   cd project/
   ```

2. Crie um ambiente virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Execute:

   ```bash
   streamlit run src/app.py
   ```

### Com Docker

1. Build e execute o container:

   ```bash
   docker build -t algodao-analise .
   docker run -p 8501:8501 algodao-analise
   ```
