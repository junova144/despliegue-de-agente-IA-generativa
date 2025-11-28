# 🚀 **Agente de IA Generativa con RAG + Memoria + Cloud Run**

### *Despliegue real en producción usando Flask, LangGraph, LlamaIndex, Elasticsearch y PostgreSQL*

Este repositorio demuestra **cómo se construye y despliega en
producción** un **agente de IA generativa profesional**, utilizando:

-   **RAG corporativo** (Elasticsearch + LlamaIndex)
-   **Memoria persistente** por usuario (PostgreSQL + LangGraph
    Checkpoints)
-   **IA generativa con OpenAI (GPT-4.1)**
-   **API escalable en Cloud Run (serverless)**
-   **Trazabilidad con LangSmith**

------------------------------------------------------------------------

# 🧠 Visión de negocio

En escenarios reales, un agente productivo requiere:

✔ Conocimiento privado (RAG)✔ Memoria por usuario (PostgreSQL)✔
Escalabilidad (Cloud Run)✔ Observabilidad (LangSmith)✔ API REST segura

Este template implementa exactamente lo que se usa en producción.

------------------------------------------------------------------------

# 📁 Estructura

    .
    ├── app.py
    ├── requirements.txt
    ├── Dockerfile
    └── README.md

------------------------------------------------------------------------

# 🔧 Configuración del entorno

## 1) LangSmith

Variables:

    LANGSMITH_ENDPOINT=https://api.smith.langchain.com
    LANGSMITH_API_KEY=tu_key
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_PROJECT=orientador_v

## 2) OpenAI API

    OPENAI_API_KEY=tu_key

## 3) PostgreSQL (memoria del agente)

Deploy en una VM o Cloud SQL.

El agente usa: - psycopg_pool - LangGraph PostgresSaver

## 4) Elasticsearch (RAG)

Puedes usar: - Elasticsearch en VM - Elastic Cloud

El RAG consulta tus documentos indexados.

------------------------------------------------------------------------

# 🧩 Explicación de archivos

## 🟦 app.py --- Lógica del agente

Incluye:

### ✔ Servidor Flask

Endpoints: - `/` -\> healthcheck - `/agent` -\> ejecución del agente

### ✔ Herramienta RAG con LlamaIndex

``` python
vector_store = LE(
    es_url="tu url",
    es_user="tu user",
    es_password="tu key",
    index_name="tu index",
)
```

### ✔ Agente ReAct con memoria

``` python
agent = create_react_agent(
    model,
    tools,
    prompt=prompt,
    checkpointer=checkpointer
)
```

### ✔ Memoria por thread_id

Cada usuario puede tener un historial persistente.

------------------------------------------------------------------------

## 🟩 requirements.txt

Lista todas las dependencias:

    Flask==2.0.1
    gunicorn==20.1.0
    psycopg[binary,pool]==3.2.6
    werkzeug==2.0.3
    elasticsearch
    langchain
    langchain-core
    langchain-community
    langchain-openai
    langchain-elasticsearch
    langgraph
    langgraph-checkpoint-postgres
    llama_index
    llama-index-vector-stores-elasticsearch

------------------------------------------------------------------------

## 🟥 Dockerfile

Contenedor listo para Cloud Run:

``` dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip     && pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "1"]
```

------------------------------------------------------------------------

# 🚀 Deploy en Cloud Run

## 1) Construir imagen y subirla a GCR

    gcloud builds submit --tag gcr.io/pe-westeros-dev-datalake/talleria:latest

## 2) Desplegar

    gcloud run deploy apicloudia   --image=gcr.io/pe-westeros-dev-datalake/talleria:latest   --platform=managed   --region=us-west4   --allow-unauthenticated

------------------------------------------------------------------------

# 🔗 Ejemplo de uso

    https://apicloudia-256134804304.us-west4.run.app/agent?msg=de%20que-trata-el-elemento&id=123

------------------------------------------------------------------------

# 💼 Nota final

Este es el estándar mínimo para agentes productivos:

-   RAG real
-   Memoria persistente
-   Contenedor dockerizado
-   API escalable
-   Trazabilidad completa

Listo para despliegues empresariales y adaptaciones futuras.
