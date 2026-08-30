def consultar_sla(criticidade: str):
    slas = {
        "baixa": "24 horas",
        "média": "8 horas",
        "media": "8 horas",
        "alta": "4 horas",
        "crítica": "1 hora",
        "critica": "1 hora",
    }

    chave = criticidade.strip().lower()

    if chave not in slas:
        return {
            "sucesso": False,
            "erro": "Criticidade inválida",
        }

    return {
        "sucesso": True,
        "criticidade": criticidade,
        "sla": slas[chave],
    }