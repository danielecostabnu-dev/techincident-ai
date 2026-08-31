from tools import consultar_sla

def test_consultar_sla_alta():
    resultado = consultar_sla("Alta")

    assert resultado["sucesso"] is True
    assert resultado["sla"] == "4 horas"

def test_consultar_sla_invalido():
    resultado = consultar_sla("Urgente")

    assert resultado["sucesso"] is False
    assert resultado["erro"] == "Criticidade inválida"