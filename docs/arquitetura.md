# Arquitetura - TechIncident AI

## Visão geral

O TechIncident AI será uma aplicação para análise inicial de incidentes técnicos de software.

A solução utilizará LangGraph para organizar o processamento em etapas, permitindo combinar decisões determinísticas com recursos de inteligência artificial.

## Fluxo principal

O fluxo planejado será:

1. Receber o incidente informado pelo usuário.
2. Validar a entrada.
3. Verificar possíveis riscos de segurança.
4. Classificar o incidente.
5. Recuperar contexto relevante.
6. Analisar o incidente.
7. Avaliar criticidade e risco.
8. Gerar um diagnóstico estruturado.

## Fluxo do LangGraph

```text
START
  |
  v
Validar entrada
  |
  v
Verificar segurança
  |
  +----------------------+
  |                      |
Entrada segura       Entrada suspeita
  |                      |
  v                      v
Classificar           Bloquear
  |
  v
Recuperar contexto
  |
  v
Analisar incidente
  |
  +-------------------------+
  |                         |
  v                         v
Avaliar criticidade     Avaliar risco
  |                         |
  +------------+------------+
               |
               v
       Consolidar análise
               |
               v
      Gerar diagnóstico
               |
               v
              END