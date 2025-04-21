
import streamlit as st
import pandas as pd
import plotly.express as px

# Carregando os dados
df = pd.read_csv("pizzaria_streamlit.csv", parse_dates=['order_date'])

st.set_page_config(page_title="Dashboard Pizzaria", layout="wide")
st.title("🍕 Dashboard da Pizzaria")

# Filtros
with st.sidebar:
    st.header("Filtros")
    categoria = st.multiselect("Categoria da Pizza", options=df['pizza_category'].unique(), default=df['pizza_category'].unique())
    tamanho = st.multiselect("Tamanho da Pizza", options=df['pizza_size'].unique(), default=df['pizza_size'].unique())
    dias = st.multiselect("Dia da Semana", options=df['dia_semana'].unique(), default=df['dia_semana'].unique())
    datas = st.date_input("Intervalo de Datas", [df['order_date'].min(), df['order_date'].max()])

# Aplicar filtros
mask = (
    df['pizza_category'].isin(categoria) &
    df['pizza_size'].isin(tamanho) &
    df['dia_semana'].isin(dias) &
    (df['order_date'] >= pd.to_datetime(datas[0])) &
    (df['order_date'] <= pd.to_datetime(datas[1]))
)
df_filtrado = df[mask]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total de Pedidos", f"{df_filtrado['order_id'].nunique():,}")
col2.metric("Receita Total", f"R$ {df_filtrado['valor_total'].sum():,.2f}")
col3.metric("Pizza Mais Vendida", df_filtrado.groupby('pizza_name')['quantity'].sum().idxmax())

# Gráficos
col1, col2 = st.columns(2)

mais_vendidas = df_filtrado.groupby('pizza_name')['quantity'].sum().sort_values(ascending=False).head(10).reset_index()
fig1 = px.bar(mais_vendidas, x='quantity', y='pizza_name', orientation='h', title='Top 10 Pizzas Mais Vendidas')
col1.plotly_chart(fig1, use_container_width=True)

mais_lucrativas = df_filtrado.groupby('pizza_name')['valor_total'].sum().sort_values(ascending=False).head(10).reset_index()
fig2 = px.bar(mais_lucrativas, x='valor_total', y='pizza_name', orientation='h', title='Top 10 Pizzas Mais Lucrativas')
col2.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)
por_tamanho = df_filtrado.groupby('pizza_size')['quantity'].sum().reset_index()
fig3 = px.bar(por_tamanho, x='pizza_size', y='quantity', title='Vendas por Tamanho')
col3.plotly_chart(fig3, use_container_width=True)

por_categoria = df_filtrado.groupby('pizza_category')['quantity'].sum().reset_index()
fig4 = px.pie(por_categoria, values='quantity', names='pizza_category', title='Distribuição por Categoria')
col4.plotly_chart(fig4, use_container_width=True)

# Pedidos por dia e hora
col5, col6 = st.columns(2)
pedidos_dia = df_filtrado.groupby('dia_semana')['order_id'].nunique().reset_index()
fig5 = px.bar(pedidos_dia, x='dia_semana', y='order_id', title='Pedidos por Dia da Semana')
col5.plotly_chart(fig5, use_container_width=True)

pedidos_hora = df_filtrado.groupby('hour')['order_id'].nunique().reset_index()
fig6 = px.area(pedidos_hora, x='hour', y='order_id', title='Pedidos por Hora do Dia')
col6.plotly_chart(fig6, use_container_width=True)
