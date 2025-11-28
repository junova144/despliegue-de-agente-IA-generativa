# 🚀 **Despliegue de Agente IA Generativa en Productivo**

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

En escenarios reales, un agente para ser lanzado en productivo requiere:

✔ Conocimiento privado (RAG)✔ Memoria por usuario (PostgreSQL)✔
Escalabilidad (Cloud Run)✔ Observabilidad (LangSmith)✔ API REST segura

Este template implementa un modelo de como lanzar un agente en ambiente productivo.

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

## ✅ **1. Configuración de Librerías Necesarias**

Estas importaciones permiten construir el agente, servirlo vía API y
conectarlo a los servicios:

-   **Flask** → crea un **servidor web** para exponer el agente como
    endpoint.
-   **LangGraph / LangChain** → librerías que permiten construir agentes
    inteligentes.
-   **LlamaIndex** → para hacer **RAG**, conectarse a Elasticsearch y
    recuperar contexto.
-   **PostgreSQL (psycopg)** → usado para **memoria persistente** del
    agente.
-   **ElasticSearch** → almacena y busca embeddings de texto.

Cada una es fundamental para que el agente responda con memoria,
contexto y razonamiento.

------------------------------------------------------------------------

## ✅ **2. Configuración de las Credenciales**

Aquí se cargan variables como:

-   `OPENAI_API_KEY`
-   `POSTGRES_HOST`, `USER`, `PASSWORD`
-   `ELASTIC_URL`, `ELASTIC_USER`, `ELASTIC_PASSWORD`

**¿Para qué sirven?**

  Variable        Propósito
  --------------- -----------------------------------------------
  OpenAI key      Permite llamar al modelo del agente
  PostgreSQL      Guarda la memoria del agente (chat histórico)
  Elasticsearch   Permite hacer RAG (búsqueda semántica)
  Flask PORT      Cloud Run asigna un puerto dinámico

**Por qué es importante**\
Esto hace que **el agente pueda razonar (modelo), recordar (Postgres) y
buscar información (Elastic)**.

------------------------------------------------------------------------

## ✅ **3. Servidor Flask --- API del Agente**

El servidor expone dos endpoints:

### \### 🟢 `/` --- Healthcheck

Sirve para que Cloud Run confirme que el servicio está vivo.

### 🟢 `/agent` --- Endpoint Principal

Recibe:

``` json
{
  "message": "tu consulta",
  "thread_id": "user123"
}
```

Y retorna la respuesta del agente.

**Para qué sirve Flask aquí:**\
👉 Convierte tu agente en una **API HTTP real**, que puede ser consumida
por un frontend, bot, app móvil o integración empresarial.\
👉 Es la forma correcta de desplegar agentes en **producción**.

------------------------------------------------------------------------

## ✅ **4. Herramienta RAG con LlamaIndex**

El código configura el vector store:

``` python
vector_store = LE(
    es_url="URL",
    es_user="USER",
    es_password="KEY",
    index_name="INDEX",
)
```

**Qué hace esta herramienta:**

-   Conecta con Elasticsearch.
-   Busca documentos relevantes usando embeddings.
-   Retorna contexto para que el agente pueda responder mejor.

**En producción**\
Esto permite hacer **respuestas basadas en tu propia base de
conocimiento corporativa**.

------------------------------------------------------------------------

## ✅ **5. Agente ReAct con Memoria**

El agente se crea así:

``` python
agent = create_react_agent(
    model,
    tools,
    prompt=prompt,
    checkpointer=checkpointer
)
```

### ✔ ¿Qué es un agente ReAct?

Un agente que puede:

-   **Razonar**
-   **Planear**
-   **Tomar acciones (usar herramientas)**
-   **Responder**

Es el tipo usado en producción por empresas.

### ✔ ¿Qué hace cada componente?

  Componente       Rol
  ---------------- ----------------------------------------
  `model`          El cerebro (GPT o similar)
  `tools`          RAG, consultas, acciones
  `prompt`         Define su personalidad e instrucciones
  `checkpointer`   Guarda la memoria por thread

------------------------------------------------------------------------

## ✅ **6. Memoria por `thread_id`**

El agente guarda el historial de cada usuario en PostgreSQL.\
Ejemplo:

-   Usuario A → `thread_id=A123`
-   Usuario B → `thread_id=B555`

Cada uno mantiene su propio contexto.

**¿Por qué es clave en producción?**

-   Soporta miles de usuarios.
-   Memoria persistente.
-   Conversaciones separadas.

------------------------------------------------------------------------

## 🏁 Conclusión

Este `app.py` no es solo un archivo:\
Es una arquitectura completa **lista para producción** con:

✔ API Flask\
✔ RAG con Elasticsearch\
✔ Memoria con PostgreSQL\
✔ Agente ReAct empresarial\
✔ Despliegue en Cloud Run

----------------------------------------------------------------------

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
