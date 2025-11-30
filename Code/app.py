import os
from flask import Flask, jsonify, request

# --- LlamaIndex para RAG ---
from llama_index.vector_stores.elasticsearch import ElasticsearchStore as LE
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding

# --- LangChain / LangGraph ---
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.postgres import PostgresSaver

# --- PostgreSQL Memory ---
from psycopg_pool import ConnectionPool

# 📊 LangSmith (Trazabilidad)
os.environ["LANGSMITH_ENDPOINT"] = ""
os.environ["LANGSMITH_API_KEY"] = ""
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = ""
os.environ["OPENAI_API_KEY"] = ""

# ---------------------------------------------------------
# 1) INICIALIZAR SERVIDOR FLASK PARA CLOUD RUN
# ---------------------------------------------------------
app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "OK", "message": "Servicio orientador vocacional activo"})

# ---------------------------------------------------------
# 2) DEFINICIÓN DE TU TOOL REAL DE RAG — USA TU ELASTICSEARCH
# ---------------------------------------------------------
@tool
def orientador_vocacional(query: str) -> str:
    """Consulta información vocacional almacenada en Elasticsearch."""

    vector_store = LE(
        es_url="http://xxxxx:9200",
        es_user="",
        es_password="",
        index_name="",
    )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        storage_context=storage_context,
        embed_model=OpenAIEmbedding()
    )

    retriever = index.as_retriever(search_kwargs={"k": 4})
    results = retriever.retrieve(query)

    output = "\n\n".join([
        f"[{i+1}] {node.node.text}\nFuente: {node.node.metadata.get('source', 'N/A')}"
        for i, node in enumerate(results)
    ])
    return output

# ---------------------------------------------------------
# 3) RUTA PRINCIPAL DEL AGENTE /agent
# ---------------------------------------------------------
@app.route("/agent", methods=["GET"])
def ejecutar_agente():
    # ------------- Parámetros GET -------------
    thread_id = request.args.get("id")
    msg = request.args.get("msg")

    if not msg:
        return jsonify({"error": "Debes enviar el parámetro 'msg'"}), 400
    if not thread_id:
        thread_id = "vocacional_default"

    # ------------- Conninfo PostgreSQL -------------
    usuario = ""
    password = "."   
    host = ""
    puerto = 5432
    basedatos = ""

    DB_URI = (
        f"postgresql://{usuario}:{password}@{host}:{puerto}/{basedatos}"
        "?sslmode=disable"
    )

    connection_kwargs = {"autocommit": True, "prepare_threshold": 0}

    # ---------------------------------------------------------
    # 4) CONECTAR MEMORIA — PostgreSQL con PostgresSaver
    # ---------------------------------------------------------
    with ConnectionPool(conninfo=DB_URI, max_size=20, kwargs=connection_kwargs) as pool:
        checkpointer = PostgresSaver(pool)

        # ---------------------------------------------------------
        # 5) MODELO
        # ---------------------------------------------------------
        model = ChatOpenAI(model="gpt-4.1")

        # ---------------------------------------------------------
        # 6) SYSTEM PROMPT (el tuyo)
        # ---------------------------------------------------------
        system_prompt = """Eres un asistente de orientación vocacional.
        Usa exclusivamente tu herramienta RAG para responder. 
        Si no tienes información, dilo de manera clara y educada.
        """

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{messages}")
        ])

        # ---------------------------------------------------------
        # 7) Crear agente ReAct + memoria + RAG
        # ---------------------------------------------------------
        tools = [orientador_vocacional]

        agent = create_react_agent(
            model,
            tools,
            prompt=prompt,
            checkpointer=checkpointer
        )

        # ---------------------------------------------------------
        # 8) Ejecutar el agente
        # ---------------------------------------------------------
        config = {"configurable": {"thread_id": thread_id}}
        response = agent.invoke(
            {"messages": [HumanMessage(content=msg)]},
            config=config
        )

        final_text = response["messages"][-1].content
        return jsonify({"respuesta": final_text})

# ---------------------------------------------------------
# 9) Cloud Run requiere puerto 8080
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
