from tools import consultar_sla


def test_consultar_sla_alta():
    resultado = consultar_sla("Alta")

    assert resultado["sucesso"] is True
    assert resultado["sla"] == "4 horas"
    assert resultado["horas"] == 4
    assert resultado["fonte"] == "Política interna de SLA do TechIncident AI"


def test_consultar_sla_com_acento():
    resultado = consultar_sla("Crítica")

    assert resultado["sucesso"] is True
    assert resultado["sla"] == "1 hora"
    assert resultado["horas"] == 1


def test_consultar_sla_invalido():
    resultado = consultar_sla("Urgente")

    assert resultado["sucesso"] is False
    assert "Criticidade inválida" in resultado["erro"]


def test_consultar_sla_vazio():
    resultado = consultar_sla("")

    assert resultado["sucesso"] is False
    assert resultado["erro"] == "Criticidade não informada."


def test_consultar_sla_tipo_invalido():
    resultado = consultar_sla(None)

    assert resultado["sucesso"] is False
    assert resultado["erro"] == "Criticidade deve ser informada como texto."
