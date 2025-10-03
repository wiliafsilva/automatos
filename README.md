# Autômatos - Noite de Aula na UNIT

Este repositório contém uma pequena aplicação Streamlit que demonstra um autômato (AFN/AFD) para modelar a sequência de eventos de uma aula com intervalo.

## Visão geral

O aplicativo (`app.py`) apresenta:
- Um alfabeto simbólico que representa estados e ações (ex.: `G`, `S`, `A1`, `I`, `A2`, `F`).
- Uma descrição informal da expressão regular aceita pela linguagem.
- Visualização do AFN (autômato não-determinístico) usando Graphviz.
- Conversão para AFD (autômato determinístico) e tabela de transição.
- Exemplos de sequências válidas e inválidas.
- Um campo para o usuário testar sua própria sequência e feedback imediato (aceita/recusada).

## Arquivos

- `app.py` — aplicação Streamlit principal (visualização + lógica de aceitação).
- `requirements.txt` — dependências Python para rodar a aplicação localmente.

## Dependências

- Python 3.8+ (foi testado com 3.11 no ambiente de desenvolvimento).
- Pacotes Python (veja `requirements.txt`):
  - `streamlit` — interface web rápida.
  - `graphviz` — geração de diagramas Graphviz.

Observação: para que a renderização dos gráficos funcione corretamente no Windows, pode ser necessário instalar o Graphviz (binários) e garantir que o executável `dot` esteja no PATH do sistema. Baixe em: https://graphviz.org/download/

## Como executar (Windows PowerShell)

1. Instale dependências:

```powershell
pip install -r requirements.txt
```

2. Execute a aplicação Streamlit:

```powershell
streamlit run app.py ou python -m streamlit run app.py
```

O navegador abrirá a interface. Se não abrir automaticamente, acesse http://localhost:8501.

## Explicação do `app.py` (seção por seção)

- Cabeçalho e título
  - Usa `streamlit` para criar uma página com título e seções claras.

- Alfabeto (Σ)
  - Define os símbolos usados pelo autômato e explica o que cada símbolo representa:
    - `G`: estudante em grupo
    - `S`: estudante sozinho esperando
    - `A1`: início da primeira aula
    - `I`: intervalo (10 minutos)
    - `A2`: aula após o intervalo
    - `F`: fim do período

- Expressão regular (descrição)
  - Descreve informalmente a forma geral das sequências aceitas: qualquer número (incluindo zero) de `G`/`S`, em seguida `A1 I A2 F`.

- Visualização AFN (Graphviz)
  - Cria um grafo direcionado com estados `q0` (espera), `q1` (aula 1), `q2` (intervalo), `q3` (aula 2) e `qf` (final).
  - Há um loop em `q0` com rótulo `G / S` permitindo repetição de ações de espera.

- Conversão AFN → AFD
  - Mostra um AFD resultante da conversão por subconjuntos; neste caso a estrutura permanece a mesma.

- Tabela de transição AFD
  - Tabela que mapeia cada estado e símbolo para o próximo estado determinístico.

- Exemplos
  - Sequências válidas: `S G G S A1 I A2 F`, `A1 I A2 F`, `G G G G A1 I A2 F`.
  - Sequências inválidas: exemplos com símbolos em ordem errada ou símbolos faltando.

- Teste de sequência (entrada do usuário)
  - `user_seq` recebe uma linha de entrada. A string é separada por espaços e validada por duas funções:
    - `aceita(sequencia)` — implementação simples que percorre a sequência e retorna `True` se termina em estado final `qf` sem erros.
    - `simulate_sequence(sequencia)` — versão que também acumula as arestas usadas e retorna índice do primeiro símbolo inválido, útil para debugar (não é diretamente usada na interface atual, mas está disponível no código).

Lógica principal de transição (resumida):

- Estado `q0`:
  - `G` ou `S` mantém em `q0` (loop).
  - `A1` → `q1`.
  - qualquer outro símbolo = rejeita.
- Estado `q1`:
  - `I` → `q2`.
  - caso contrário = rejeita.
- Estado `q2`:
  - `A2` → `q3`.
  - caso contrário = rejeita.
- Estado `q3`:
  - `F` → `qf` (aceita se terminar aqui).
  - caso contrário = rejeita.

## Exemplos para testar na caixa de entrada

- Aceitas:
  - `A1 I A2 F`
  - `G S G A1 I A2 F`

- Rejeitadas:
  - `G S A1 A2 F`  (faltou `I`)
  - `A1 I A2`      (faltou `F`)

## Observações e melhorias sugeridas


Se quiser, posso também:
- adicionar a integração de `simulate_sequence` à interface para mostrar o caminho percorrido no grafo;
- implementar testes unitários (pytest) para as funções de validação;
- gerar uma versão exportável (HTML) da interface.
