# TechIncident AI

## Descrição da solução

O TechIncident AI é uma aplicação de inteligência artificial voltada à análise inicial de incidentes técnicos de software.

O projeto é uma evolução do mini-projeto Agente de Resumos Técnicos, ampliando o fluxo anterior para realizar análise, classificação e diagnóstico de incidentes técnicos.

## Problema

Equipes de desenvolvimento, QA e suporte técnico recebem erros, logs e relatos de incidentes que precisam ser analisados para identificar possíveis causas e ações recomendadas.

O TechIncident AI tem como objetivo apoiar essa análise, processando as informações do incidente e produzindo um diagnóstico inicial estruturado.

## Público-alvo

- Desenvolvedores;
- Profissionais de QA;
- Equipes de suporte técnico.

## Entrada

A aplicação recebe uma descrição textual de um incidente técnico, que pode conter mensagens de erro, logs ou informações sobre o comportamento apresentado pelo sistema.

## Saída

A aplicação deverá produzir uma saída estruturada contendo informações como:

- categoria do incidente;
- criticidade;
- resumo;
- possíveis causas;
- ação recomendada;
- indicação de necessidade de aprovação humana.

## Limites da solução

O TechIncident AI atua como ferramenta de apoio à análise de incidentes.

A aplicação não deverá executar automaticamente ações destrutivas ou irreversíveis, revelar credenciais ou permitir que conteúdos fornecidos na entrada substituam suas regras de segurança.

## Cenários de uso

### Cenário 1 — Fluxo principal

O usuário informa um incidente técnico, como um erro de API acompanhado de timeout.

A aplicação deverá validar a entrada, classificar o incidente, recuperar informações relevantes, analisar o problema e produzir um diagnóstico estruturado.

### Cenário 2 — Entrada adversarial

O usuário fornece uma descrição de incidente contendo uma tentativa de prompt injection, solicitando que o agente ignore suas regras ou revele informações sensíveis.

A aplicação deverá identificar a entrada não confiável, impedir ações não autorizadas e não revelar credenciais ou informações sensíveis.