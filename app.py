import pandas as pd
import plotly.express as px
import streamlit as st

# Configuración de la página
st.set_page_config(page_title="QuimBío · Monitoreo L1", page_icon="🏭", layout="wide")

st.title("🏭 QuimBío Minería · Monitoreo Línea 1")
st.caption("Empresa ficticia – proyecto de portafolio de Loreto")

# Leer los datos
df = pd.read_csv("data/detenciones_L1_2026.csv")

# Filtro interactivo en la barra lateral
st.sidebar.header("Filtros")
turno = st.sidebar.selectbox("Turno", ["Todos", "Día", "Noche"])

horas_planificadas = 8424
if turno != "Todos":
    df = df[df["turno"] == turno]
    horas_planificadas = 8424 / 2  # cada turno tiene la mitad de las horas

# Indicadores del año
horas_detenidas = df["minutos"].sum() / 60
disponibilidad = (horas_planificadas - horas_detenidas) / horas_planificadas * 100

col1, col2, col3 = st.columns(3)
col1.metric("Disponibilidad 2026", f"{disponibilidad:.1f} %", f"{disponibilidad - 80:.1f} pts vs meta")
col2.metric("Horas detenidas", f"{horas_detenidas:.0f} h")
col3.metric("N° de detenciones", len(df))

# Pareto de causas
pareto = df.groupby("causa")["minutos"].sum().sort_values(ascending=False).to_frame()
pareto["horas"] = (pareto["minutos"] / 60).round(1)
pareto["porcentaje"] = (pareto["minutos"] / pareto["minutos"].sum() * 100).round(1)
pareto["acumulado"] = (pareto["minutos"].cumsum() / pareto["minutos"].sum() * 100).round(1)
pareto = pareto.reset_index()

st.subheader("Pareto de causas de detención")
grafico = px.bar(pareto, x="causa", y="horas", text="porcentaje")
grafico.update_traces(texttemplate="%{text} %")
st.plotly_chart(grafico)
# Evolución mensual
st.subheader("Evolución mensual de horas detenidas")
df["mes"] = pd.to_datetime(df["fecha"]).dt.month
mensual = df.groupby("mes")["minutos"].sum().reset_index()
mensual["horas"] = (mensual["minutos"] / 60).round(1)
grafico_mes = px.line(mensual, x="mes", y="horas", markers=True)
grafico_mes.update_yaxes(rangemode="tozero")
grafico_mes.update_xaxes(dtick=1)
maximo_mensual = horas_planificadas / 12 * 0.20
grafico_mes.add_hline(y=maximo_mensual, line_dash="dash", line_color="red",
                      annotation_text=f"Máximo para cumplir meta ({maximo_mensual:.0f} h)")
st.plotly_chart(grafico_mes)
st.subheader("Detalle")
st.dataframe(pareto, hide_index=True)