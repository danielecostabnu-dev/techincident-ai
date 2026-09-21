from typing import TypedDict
import json
import time

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from tools import consultar_sla


load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    timeout=30,
    max_retries=2,
)


def log_evento(evento: str, detalhes: dict):
    registro = {
        "evento": evento,
        "timestamp": time.time(),
        "detalhes": detalhes,
    }
    print(json.dumps(registro, ensure_ascii=False))


class IncidentState(TypedDict):
    titulo: str
    descricao: str
    categoria: str
    criticidade: str
    risco: str
    sla: str
    historico: list[str]
    resumo: str
    acao_sugerida: str
    revisao_humana: bool
    diagnostico: str


def validar_entrada(texto: str):
    termos_bloqueados = [
        "ignore as instruções",
        "ignore todas as instruções",
        "ignore instruções anteriores",
        "revele a chave",
        "revele sua chave",
        "mostre a chave",
        "mostre sua chave",
        "groq_api_key",
        "api key",
        "system prompt",
        "prompt do sistema",
        "revele o prompt",
        "mostre o prompt",
    ]

    texto_normalizado = texto.lower()

    return not any(
        termo in texto_normalizado
        for termo in termos_bloqueados
    )


def analisar_incidente(state: IncidentState):
    print("1. Analisando chamado...")
    inicio = time.time()

    titulo = state.get("titulo", "").strip()
    descricao = state.get("descricao", "").strip()

    if not titulo or not descricao:
        raise ValueError(
            "Entrada inválida: título e descrição são obrigatórios."
        )

    texto_chamado = f"{titulo}. {descricao}"

    log_evento(
        "analise_iniciada",
        {
            "titulo": titulo,
            "descricao": descricao,
        },
    )

    if not validar_entrada(texto_chamado):
        log_evento(
            "entrada_bloqueada",
            {
                "motivo": "Possível tentativa de manipulação do agente."
            },
        )

        raise ValueError(
            "Entrada bloqueada por regra de segurança."
        )

    historico = state.get("historico", [])

    if texto_chamado not in historico:
        historico.append(texto_chamado)

    state["historico"] = historico

    log_evento(
        "memoria_atualizada",
        {
            "total_interacoes": len(historico),
        },
    )

    log_evento(
        "tempo_analise",
        {
            "segundos": round(time.time() - inicio, 4),
        },
    )

    return state


def avaliar_criticidade(state: IncidentState):
    print("2. Avaliando criticidade...")

    texto_chamado = f"{state['titulo']}. {state['descricao']}"

    historico = state.get("historico", [])

    contexto_anterior = [
        item
        for item in historico
        if item != texto_chamado
    ]

    if contexto_anterior:
        contexto = "\n".join(contexto_anterior[-3:])
    else:
        contexto = "Nenhum incidente anterior relacionado."

    log_evento(
        "contexto_consultado",
        {
            "interacoes_anteriores": len(contexto_anterior),
            "contexto_utilizado": contexto,
        },
    )

    try:
        resposta = llm.invoke(
            f"Classifique a criticidade deste chamado técnico como "
            f"Baixa, Média, Alta ou Crítica. "
            f"Considere também o histórico de interações anteriores, "
            f"pois recorrência ou persistência do problema pode "
            f"influenciar a criticidade. "
            f"Responda somente com uma palavra, sem justificativa.\n\n"
            f"Histórico anterior:\n{contexto}\n\n"
            f"Chamado atual:\n{texto_chamado}"
        )

        criticidade = resposta.content.strip()

        log_evento(
            "criticidade_avaliada",
            {
                "criticidade": criticidade,
                "historico_considerado": bool(contexto_anterior),
            },
        )

        return {
            "criticidade": criticidade,
        }

    except Exception as erro:
        log_evento(
            "erro_llm_criticidade",
            {
                "erro": str(erro),
            },
        )

        return {
            "criticidade": "Média",
        }


def avaliar_risco(state: IncidentState):
    print("3. Avaliando risco...")

    texto_chamado = f"{state['titulo']}. {state['descricao']}"

    try:
        resposta = llm.invoke(
            f"Classifique o risco deste chamado técnico como "
            f"Baixo, Médio, Alto ou Crítico. "
            f"Responda somente com a classificação, sem justificativa. "
            f"Chamado: {texto_chamado}"
        )

        risco = resposta.content.strip()

        log_evento(
            "risco_avaliado",
            {
                "risco": risco,
            },
        )

        return {
            "risco": risco,
        }

    except Exception as erro:
        log_evento(
            "erro_llm_risco",
            {
                "erro": str(erro),
            },
        )

        return {
            "risco": "Médio",
        }


def avaliar_categoria(state: IncidentState):
    print("4. Avaliando categoria...")

    texto_chamado = f"{state['titulo']}. {state['descricao']}"

    try:
        resposta = llm.invoke(
            f"Classifique este chamado técnico em uma das categorias: "
            f"Software, Infraestrutura ou Suporte. "
            f"Responda somente com a categoria, sem justificativa. "
            f"Chamado: {texto_chamado}"
        )

        categoria = resposta.content.strip()

        log_evento(
            "categoria_avaliada",
            {
                "categoria": categoria,
            },
        )

        return {
            "categoria": categoria,
        }

    except Exception as erro:
        log_evento(
            "erro_llm_categoria",
            {
                "erro": str(erro),
            },
        )

        return {
            "categoria": "Suporte",
        }


def consultar_sla_incidente(state: IncidentState):
    print("5. Consultando SLA...")

    inicio = time.time()

    resultado = consultar_sla(
        state["criticidade"]
    )

    log_evento(
        "tool_sla_executada",
        {
            "criticidade": state["criticidade"],
            "sucesso": resultado["sucesso"],
            "tempo_segundos": round(
                time.time() - inicio,
                4,
            ),
        },
    )

    if not resultado["sucesso"]:
        return {
            "sla": "SLA não encontrado",
        }

    return {
        "sla": resultado["sla"],
    }


def consolidar_analise(state: IncidentState):
    print("6. Consolidando análise...")

    log_evento(
        "analise_consolidada",
        {
            "categoria": state["categoria"],
            "criticidade": state["criticidade"],
            "risco": state["risco"],
            "sla": state["sla"],
        },
    )

    return state


def decidir_fluxo(state: IncidentState):
    criticidade = state["criticidade"].strip().lower()

    if criticidade in [
        "alta",
        "crítica",
        "critica",
    ]:
        log_evento(
            "decisao_fluxo",
            {
                "rota": "priorizar_incidente",
            },
        )

        return "priorizar_incidente"

    log_evento(
        "decisao_fluxo",
        {
            "rota": "gerar_diagnostico",
        },
    )

    return "gerar_diagnostico"


def priorizar_incidente(state: IncidentState):
    print("7. Priorizando chamado crítico...")

    log_evento(
        "incidente_priorizado",
        {
            "criticidade": state["criticidade"],
            "risco": state["risco"],
        },
    )

    return {}


def gerar_diagnostico(state: IncidentState):
    print("8. Gerando resposta estruturada...")

    inicio = time.time()

    criticidade = state["criticidade"].strip()
    risco = state["risco"].strip()
    categoria = state["categoria"].strip()

    revisao_humana = (
        criticidade.lower()
        in [
            "alta",
            "crítica",
            "critica",
        ]
        or risco.lower()
        in [
            "alto",
            "crítico",
            "critico",
        ]
    )

    resumo = (
        f"{state['titulo']}: "
        f"{state['descricao']}"
    )

    if revisao_humana:
        acao_sugerida = (
            "Priorizar o chamado e encaminhar "
            "para revisão humana."
        )
    else:
        acao_sugerida = (
            "Seguir o fluxo normal de atendimento "
            "conforme o SLA."
        )

    state["resumo"] = resumo
    state["acao_sugerida"] = acao_sugerida
    state["revisao_humana"] = revisao_humana

    saida = {
        "categoria": categoria,
        "severidade": criticidade,
        "risco": risco,
        "resumo": resumo,
        "acao_sugerida": acao_sugerida,
        "revisao_humana": revisao_humana,
        "sla": state["sla"],
        "quantidade_interacoes": len(
            state["historico"]
        ),
    }

    state["diagnostico"] = json.dumps(
        saida,
        ensure_ascii=False,
        indent=2,
    )

    log_evento(
        "resposta_gerada",
        {
            "categoria": categoria,
            "criticidade": criticidade,
            "risco": risco,
            "revisao_humana": revisao_humana,
            "tempo_segundos": round(
                time.time() - inicio,
                4,
            ),
        },
    )

    return state


memory = MemorySaver()

workflow = StateGraph(IncidentState)

workflow.add_node(
    "analisar_incidente",
    analisar_incidente,
)

workflow.add_node(
    "avaliar_criticidade",
    avaliar_criticidade,
)

workflow.add_node(
    "avaliar_risco",
    avaliar_risco,
)

workflow.add_node(
    "avaliar_categoria",
    avaliar_categoria,
)

workflow.add_node(
    "consultar_sla",
    consultar_sla_incidente,
)

workflow.add_node(
    "consolidar_analise",
    consolidar_analise,
)

workflow.add_node(
    "priorizar_incidente",
    priorizar_incidente,
)

workflow.add_node(
    "gerar_diagnostico",
    gerar_diagnostico,
)

workflow.set_entry_point(
    "analisar_incidente"
)

workflow.add_edge(
    "analisar_incidente",
    "avaliar_criticidade",
)

workflow.add_edge(
    "analisar_incidente",
    "avaliar_risco",
)

workflow.add_edge(
    "analisar_incidente",
    "avaliar_categoria",
)

workflow.add_edge(
    "avaliar_criticidade",
    "consultar_sla",
)

workflow.add_edge(
    [
        "consultar_sla",
        "avaliar_risco",
        "avaliar_categoria",
    ],
    "consolidar_analise",
)

workflow.add_conditional_edges(
    "consolidar_analise",
    decidir_fluxo,
    {
        "priorizar_incidente":
            "priorizar_incidente",
        "gerar_diagnostico":
            "gerar_diagnostico",
    },
)

workflow.add_edge(
    "priorizar_incidente",
    "gerar_diagnostico",
)

workflow.add_edge(
    "gerar_diagnostico",
    END,
)

app = workflow.compile(
    checkpointer=memory
)


def criar_estado(
    titulo: str,
    descricao: str,
    historico=None,
):
    return {
        "titulo": titulo,
        "descricao": descricao,
        "categoria": "",
        "criticidade": "",
        "risco": "",
        "sla": "",
        "historico": (
            historico.copy()
            if historico
            else []
        ),
        "resumo": "",
        "acao_sugerida": "",
        "revisao_humana": False,
        "diagnostico": "",
    }


if __name__ == "__main__":
    config = {
        "configurable": {
            "thread_id": "incidente-001",
        }
    }

    primeiro_incidente = criar_estado(
        titulo="Erro 500 na API de usuários",
        descricao=(
            "A API apresenta timeout "
            "após 30 segundos."
        ),
    )

    resultado_1 = app.invoke(
        primeiro_incidente,
        config=config,
    )

    print(
        "\n=== PRIMEIRA INTERAÇÃO ==="
    )

    print(
        resultado_1["diagnostico"]
    )

    segundo_incidente = criar_estado(
        titulo="Persistência do erro",
        descricao=(
            "O problema informado anteriormente "
            "continua ocorrendo mesmo após "
            "reiniciar o serviço."
        ),
        historico=resultado_1["historico"],
    )

    resultado_2 = app.invoke(
        segundo_incidente,
        config=config,
    )

    print(
        "\n=== SEGUNDA INTERAÇÃO ==="
    )

    print(
        resultado_2["diagnostico"]
    )

    print(
        "\n=== MEMÓRIA / CONTEXTO ACUMULADO ==="
    )

    for indice, item in enumerate(
        resultado_2["historico"],
        start=1,
    ):
        print(
            f"{indice}. {item}"
        )
