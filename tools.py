from typing import TypedDict


class SLAResult(TypedDict, total=False):
    sucesso: bool
    criticidade: str
    sla: str
    horas: int
    fonte: str
    erro: str


class RepositorioSLA:
    """
    Camada responsável pelo acesso às políticas de SLA.

    Nesta versão, os dados são mantidos em memória para fins
    acadêmicos. A abstração permite substituir futuramente essa
    fonte por banco de dados, API ou outro serviço externo sem
    alterar a ferramenta consultar_sla.
    """

    def __init__(self):
        self._politicas = {
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

    def buscar_por_criticidade(self, criticidade: str):
        return self._politicas.get(criticidade)


repositorio_sla = RepositorioSLA()


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
    Tool responsável por consultar o SLA de um incidente.

    A função atua como interface entre o agente e a camada
    responsável pelas políticas de SLA.
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

    politica = repositorio_sla.buscar_por_criticidade(chave)

    if politica is None:
        return {
            "sucesso": False,
            "erro": (
                "Criticidade inválida. "
                "Valores aceitos: Baixa, Média, Alta ou Crítica."
            ),
        }

    return {
        "sucesso": True,
        "criticidade": criticidade.strip(),
        "sla": politica["sla"],
        "horas": politica["horas"],
        "fonte": "Política interna de SLA do TechIncident AI",
    }