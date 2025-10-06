import streamlit as st
import graphviz

st.title("🌙 Autômatos - Noite de Aula na UNIT")

# ------------------ ALFABETO ------------------
st.header("🔠 Alfabeto Σ (Símbolos da linguagem)")

st.markdown("""
| Símbolo | Significado                             |
|---------|-----------------------------------------|
| G       | Estudante em grupo no mini-shopping     |
| S       | Estudante sozinho esperando             |
| A1      | Aula antes do intervalo                 |
| I       | Intervalo (10 minutos)                  |
| A2      | Aula após o intervalo                   |
| F       | Fim do período (vai embora)             |
""")

# ------------------ EXPRESSÃO REGULAR ------------------
st.header("✍️ Expressão Regular da Linguagem")

st.markdown("""
A linguagem aceita todas as sequências da forma:


Ou seja:
- Zero ou mais ações de espera (sozinho ou em grupo)
- Depois **A1** (aula começa)
- Depois **I** (intervalo)
- Depois **A2** (aula recomeça)
- Depois **F** (fim do dia)
""")


# ------------------ AFN VISUAL ------------------
st.header("🌀 AFN (Não-determinístico)")

st.markdown("""
- O autômato aceita múltiplas ações de `G` ou `S` antes de `A1` (ciclo).
- É considerado AFN pois permite múltiplos caminhos para o mesmo símbolo (`G`, `S`).
""")

afn = graphviz.Digraph()
afn.attr(rankdir='LR')

# Estados
afn.node("q0", "q0 (espera)", shape="circle")
afn.node("q1", "q1 (aula 1)", shape="circle")
afn.node("q2", "q2 (intervalo)", shape="circle")
afn.node("q3", "q3 (aula 2)", shape="circle")
afn.node("qf", "qf (fim)", shape="doublecircle")

# Transições (com não-determinismo: G/S levam a q0 ou permanecem)
afn.edge("q0", "q0", label="G / S")
afn.edge("q0", "q1", label="A1")
afn.edge("q1", "q2", label="I")
afn.edge("q2", "q3", label="A2")
afn.edge("q3", "qf", label="F")

st.graphviz_chart(afn)

# ------------------ AFD CONVERTIDO ------------------
st.header("🔁 Conversão AFN → AFD")

st.markdown("""
Como o AFN acima já é determinístico em suas transições por símbolo, a conversão gera um AFD com a mesma estrutura.

🔹 Usamos o **algoritmo de subconjuntos**, mas neste caso, ele gera os mesmos estados.

📌 A diferença é que cada conjunto de estados se torna um novo estado único no AFD.
""")

afd = graphviz.Digraph()
afd.attr(rankdir='LR')

# Estados
afd.node("{q0}", "{q0}", shape="circle")
afd.node("{q1}", "{q1}", shape="circle")
afd.node("{q2}", "{q2}", shape="circle")
afd.node("{q3}", "{q3}", shape="circle")
afd.node("{qf}", "{qf}", shape="doublecircle")

# Transições determinísticas
afd.edge("{q0}", "{q0}", label="G / S")
afd.edge("{q0}", "{q1}", label="A1")
afd.edge("{q1}", "{q2}", label="I")
afd.edge("{q2}", "{q3}", label="A2")
afd.edge("{q3}", "{qf}", label="F")

st.graphviz_chart(afd)

# ------------------ TABELA DE TRANSIÇÃO AFD ------------------
st.subheader("📋 Tabela de Transições do AFD")

st.markdown("""
| Estado   | Símbolo | Próximo Estado |
|----------|---------|----------------|
| `{q0}`   | G / S   | `{q0}`         |
| `{q0}`   | A1      | `{q1}`         |
| `{q1}`   | I       | `{q2}`         |
| `{q2}`   | A2      | `{q3}`         |
| `{q3}`   | F       | `{qf}`         |
""")

# ------------------ EXEMPLOS ------------------
st.header("🎯 Exemplos de Sequências")

col1, col2 = st.columns(2)

with col1:
    st.subheader("✅ Válidas")
    st.code("S G G S A1 I A2 F")
    st.code("A1 I A2 F")
    st.code("G G G G A1 I A2 F")

with col2:
    st.subheader("❌ Inválidas")
    st.code("G S A1 A2 F  # faltou I")
    st.code("S G I A1 A2 F  # I fora de ordem")
    st.code("A1 I A2       # faltou F")
    st.code("A1 I I A2 F   # I repetido")
# ------------------ TESTE DE SEQUÊNCIA ------------------
st.header("✅ Teste sua própria sequência")

user_seq = st.text_input("Digite a sequência separada por espaços (ex: G S G A1 I A2 F):")
entrada = user_seq.strip().split()

def aceita(sequencia):
    # Estados: espera (G/S), A1, I, A2, F
    etapas = ['A1', 'I', 'A2', 'F']
    etapa_atual = 0  # começa na primeira etapa obrigatória
    for simbolo in sequencia:
        if simbolo in ['G', 'S']:
            continue  # G/S podem aparecer em qualquer momento antes de A1
        elif etapa_atual < len(etapas) and simbolo == etapas[etapa_atual]:
            etapa_atual += 1  # avançar para próxima etapa
        elif etapa_atual < len(etapas) and simbolo in etapas[etapa_atual+1:]:
            # Permite começar em qualquer etapa, mas nunca voltar
            proxima = etapas.index(simbolo)
            if proxima == etapa_atual or proxima == etapa_atual + 1:
                etapa_atual = proxima + 1
            else:
                return False
        else:
            return False
    return etapa_atual == len(etapas)

if user_seq:
    if aceita(entrada):
        st.success("✅ Sequência válida!")
    else:
        st.error("❌ Sequência inválida.")
