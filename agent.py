from typing import TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
from tools import consultar_sla
load_dotenv()
llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)


class IncidentState(TypedDict):    
    incidente: str
    criticidade: str
    risco: str
    sla: str
    historico: list[str]
    diagnostico: str


def analisar_incidente(state: IncidentState):
    print("1. Analisando incidente...")
    state["historico"].append(state["incidente"])
    return state


def avaliar_criticidade(state: IncidentState):
    print("2. Avaliando criticidade...")
    resposta = llm.invoke(
    f"Classifique a criticidade deste incidente como Baixa, Média, Alta ou Crítica. "
    f"Responda somente com uma palavra, sem justificativa: {state['incidente']}"
)
    return {"criticidade": resposta.content}


def avaliar_risco(state: IncidentState):
    print("3. Avaliando risco...")
    resposta = llm.invoke(
        f"Classifique o risco deste incidente como Baixo, Médio, Alto ou Crítico. "
        f"Responda somente com a classificação: {state['incidente']}"
    )
    return {"risco": resposta.content}

def consultar_sla_incidente(state: IncidentState):
    print("4. Consultando SLA...")
    resultado = consultar_sla(state["criticidade"])

    if not resultado["sucesso"]:
        return {"sla": "SLA não encontrado"}

    return {"sla": resultado["sla"]}


def decidir_fluxo(state: IncidentState):
    if state["criticidade"].strip().lower() in ["alta", "crítica", "critica"]:
        return "priorizar_incidente"

    return "gerar_diagnostico"


def consolidar_analise(state: IncidentState):
    print("5. Consolidando análise...")
    return state

def priorizar_incidente(state: IncidentState):
    print("6. Priorizando incidente crítico...")
    return {}


def gerar_diagnostico(state: IncidentState):
    print("7. Gerando diagnóstico...")
    state["diagnostico"] = (
        f"Incidente: {state['incidente']} | "
        f"Criticidade: {state['criticidade']} | "
        f"Risco: {state['risco']}"
        f" | SLA: {state['sla']}"
          )
    return state

memory = MemorySaver()

workflow = StateGraph(IncidentState)

workflow.add_node("analisar_incidente", analisar_incidente)
workflow.add_node("avaliar_criticidade", avaliar_criticidade)
workflow.add_node("avaliar_risco", avaliar_risco)
workflow.add_node("consultar_sla", consultar_sla_incidente)
workflow.add_node("consolidar_analise", consolidar_analise)
workflow.add_node("priorizar_incidente", priorizar_incidente)
workflow.add_node("gerar_diagnostico", gerar_diagnostico)

workflow.set_entry_point("analisar_incidente")

workflow.add_edge("analisar_incidente", "avaliar_criticidade")
workflow.add_edge("analisar_incidente", "avaliar_risco")

workflow.add_edge("avaliar_criticidade", "consultar_sla")
workflow.add_edge(["consultar_sla", "avaliar_risco"], "consolidar_analise")

workflow.add_conditional_edges(
    "consolidar_analise",
    decidir_fluxo,
    {
       "priorizar_incidente": "priorizar_incidente",
        "gerar_diagnostico": "gerar_diagnostico",
    },
)
workflow.add_edge("priorizar_incidente", "gerar_diagnostico")
workflow.add_edge("gerar_diagnostico", END)

app = workflow.compile(checkpointer=memory)
if __name__ == "__main__":
    estado_inicial = {
        "incidente": "Erro 500 na API de usuários com timeout após 30 segundos.",
        "criticidade": "",
        "risco": "",
        "sla": "",
        "historico": [],
        "diagnostico": "",
    }

    config = {"configurable": {"thread_id": "incidente-001"}}

    resultado = app.invoke(estado_inicial, config=config)

    print("\nResultado final:")
    print(resultado["diagnostico"])
    print("Histórico:", resultado["historico"])
