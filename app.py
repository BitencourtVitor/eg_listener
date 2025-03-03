import streamlit as st
import pandas as pd
import time
import json

st.set_page_config(page_title="Effective Gain", page_icon="🔑")

st.title('Effective Gain')
st.write('Ferramenta para Gestão de Adimplência do Cartão de Todos')

mostrar = False

with open('./clientes.json', 'r') as f:
    data = json.load(f)
clientes = pd.DataFrame(data)

url = './data.xlsx'
df = pd.read_excel(url, sheet_name='Export', engine='openpyxl')

regional = st.selectbox('Regional', df['Regional'].dropna().unique())

col1, col2 = st.columns([3, 1], vertical_alignment='bottom')

with col1:
    franquia_email = st.text_input('E-mail da Franquia')
with col2:
    if st.button('Consultar'):
        if franquia_email:
            franquia = clientes[clientes['email'].str.lower() == franquia_email.lower()]
            if not franquia.empty:
                franquia_nome = franquia.iloc[0]['franquia']
                df = df[(df['Franquia'].str.contains(franquia_nome, case=False, na=False)) & (df['Regional'] == regional)]
                mostrar = True
            else:
                st.toast('Franquia não encontrada para o e-mail informado.')
                time.sleep(2)
        else:
            st.toast('Informe um e-mail válido para a franquia.')
            time.sleep(2)

colunas_desejadas = ['Matrícula', 'Nome', 'Celular', 'Email', 'Descrição', 'Régua', 'VAM Inadimplente']
df['Nome'] = df['Nome'].str.title()
df['Nome'] = df['Nome'].str.replace(r'\b\w', lambda x: x.group().upper(), regex=True)
df['Email'] = df['Email'].str.lower()
df['Celular'] = df['Celular'].apply(lambda x: f"({str(int(x))[:2]}) {str(int(x))[2:7]}-{str(int(x))[7:]}" if pd.notna(x) else x)
df['VAM Inadimplente'] = df['VAM Inadimplente'].apply(lambda x: f'R$ {x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))
df = df[colunas_desejadas]
df = df[df['Matrícula'].notna()]

if mostrar:
    with st.container(border=True):
        col1, col2 = st.columns([3, 1], vertical_alignment='center')
        with col1:
            st.subheader('Clientes Inadimplentes Atualmente')
        with col2:
            st.metric(label='Total', value=df.shape[0])
        st.dataframe(df, hide_index=True)