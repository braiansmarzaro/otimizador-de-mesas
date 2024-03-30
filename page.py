import streamlit as st
import pandas as pd
from solution import Solver

st.sidebar.header("Insira um arquivo csv com os nomes dos participantes")
uploaded_file = st.sidebar.file_uploader("Upload CSV", help="Insira um arquivo csv onde a primeira coluna tem o nome do estudante e as colunas seguintes são suas preferências. O csv deve conter o título das colunas",type="csv")

st.header("Organizador de mesas para estudantes e empresários")

if uploaded_file is not None:
    solver = Solver(uploaded_file)
    solver.define_problem()
    
    st.subheader("Dados de entrada")
    st.dataframe(solver.df)

# Create a button to solve
if st.button("Solve"):
    st.subheader('Resultados')
    solver.solve()
    for e,s in solver.resultados():
        st.write(f'A(o) estudante {s} se sentará com a(o) empresária(o) {e}.')
    
    insatisfeitos = solver.resultados_negativos()
    st.write(f"A quantidade de estudantes insatisfeitos na solução ótima é {insatisfeitos}.")
