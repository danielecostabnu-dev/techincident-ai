from typing import TypedDict
from langgraph.graph import StateGraph, END


class IncidentState(TypedDict):
    incidente: str
    criticidade: str
    risco: str
    diagnostico: str


def analisar_incidente(state: IncidentState):
    print("1. Analisando incidente...")
    return state


def avaliar_criticidade(state: IncidentState):
    print("2. Avaliando criticidade...")
    state["criticidade"] = "Em análise"
    return state


def avaliar_risco(state: IncidentState):
    print("3. Avaliando risco...")
    state["risco"] = "Em análise"
    return state


def consolidar_analise(state: IncidentState):
    print("4. Consolidando análise...")
    return state


def gerar_diagnostico(state: IncidentState):
    print("5. Gerando diagnóstico...")
    state["diagnostico"] = (
        f"Incidente: {state['incidente']} | "
        f"Criticidade: {state['criticidade']} | "
        f"Risco: {state['risco']}"
    )
    return state


workflow = StateGraph(IncidentState)

workflow.add_node("analisar_incidente", analisar_incidente)
workflow.add_node("avaliar_criticidade", avaliar_criticidade)
workflow.add_node("avaliar_risco", avaliar_risco)
workflow.add_node("consolidar_analise", consolidar_analise)
workflow.add_node("gerar_diagnostico", gerar_diagnostico)

workflow.set_entry_point("analisar_incidente")

workflow.add_edge("analisar_incidente", "avaliar_criticidade")
workflow.add_edge("avaliar_criticidade", "avaliar_risco")
workflow.add_edge("avaliar_risco", "consolidar_analise")
workflow.add_edge("consolidar_analise", "gerar_diagnostico")
workflow.add_edge("gerar_diagnostico", END)

app = workflow.compile()
if __name__ == "__main__":
    estado_inicial = {
        "incidente": "Erro 500 na API de usuários com timeout após 30 segundos.",
        "criticidade": "",
        "risco": "",
        "diagnostico": "",
    }

    resultado = app.invoke(estado_inicial)

    print("\nResultado final:")
    print(resultado["diagnostico"])