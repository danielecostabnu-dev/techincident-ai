from typing import TypedDict


class SLAResult(TypedDict, total=False):
    sucesso: bool
    criticidade: str
    sla: str
    horas: int
    fonte: str
    erro: str


POLITICA_SLA = {
    "baixa": {
        "sla": "24 horas",
        "horas": 24,
    },
    "media": {
        "sla": "8 horas",
        "horas": 8,
    },
    "alta": {
        "sla": "4 horas",
        "horas": 4,
    },
    "critica": {
        "sla": "1 hora",
        "horas": 1,
    },
}


def normalizar_criticidade(criticidade: str) -> str:
    if not isinstance(criticidade, str):
        return ""

    chave = criticidade.strip().lower()

    substituicoes = {
        "média": "media",
        "crítica": "critica",
    }

    return substituicoes.get(chave, chave)


def consultar_sla(criticidade: str) -> SLAResult:
    """
    Consulta a política interna de SLA de acordo com a criticidade
    classificada pelo agente.

    Entrada:
        criticidade: Baixa, Média, Alta ou Crítica.

    Saída:
        dicionário estruturado contendo sucesso, SLA, horas e fonte.
        Em caso de parâmetro inválido, retorna erro controlado.
    """

    if not isinstance(criticidade, str):
        return {
            "sucesso": False,
            "erro": "Criticidade deve ser informada como texto.",
        }

    if not criticidade.strip():
        return {
            "sucesso": False,
            "erro": "Criticidade não informada.",
        }

    chave = normalizar_criticidade(criticidade)

    if chave not in POLITICA_SLA:
        return {
            "sucesso": False,
            "erro": (
                "Criticidade inválida. "
                "Valores aceitos: Baixa, Média, Alta ou Crítica."
            ),
        }

    politica = POLITICA_SLA[chave]

    return {
        "sucesso": True,
        "criticidade": criticidade.strip(),
        "sla": politica["sla"],
        "horas": politica["horas"],
        "fonte": "Política interna de SLA do TechIncident AI",
    }
