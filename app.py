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

horas_planificadas = 8424 * 2  # horas-reactor: 2 reactores, descontando la parada anual de 14 días
if turno != "Todos":
    df = df[df["turno"] == turno]
    horas_planificadas = horas_planificadas / 2  # cada turno tiene la mitad de las horas

# Indicadores del año
horas_detenidas = df["minutos"].sum() / 60
disponibilidad = (horas_planificadas - horas_detenidas) / horas_planificadas * 100

col1, col2, col3 = st.columns(3)
col1.metric("Disponibilidad 2026", f"{disponibilidad:.1f} %", f"{disponibilidad - 80:.1f} pts vs meta")
col2.metric("Horas-reactor detenidas", f"{horas_detenidas:.0f} h")
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

# Evolución mensual de la disponibilidad
st.subheader("Evolución mensual de la disponibilidad")
df["mes"] = pd.to_datetime(df["fecha"]).dt.month
mensual = df.groupby("mes")["minutos"].sum().reset_index()
mensual["horas_detenidas"] = mensual["minutos"] / 60

# Horas-reactor planificadas de cada mes: horas del mes × 2 reactores, menos la parada anual de febrero
horas_del_mes = pd.Series(pd.date_range("2026-01-01", "2027-01-01", freq="h", inclusive="left")).dt.month.value_counts()
mensual["horas_planificadas"] = mensual["mes"].map(horas_del_mes) * 2
mensual.loc[mensual["mes"] == 2, "horas_planificadas"] -= 14 * 24 * 2
if turno != "Todos":
    mensual["horas_planificadas"] = mensual["horas_planificadas"] / 2

mensual["disponibilidad"] = ((mensual["horas_planificadas"] - mensual["horas_detenidas"]) / mensual["horas_planificadas"] * 100).round(1)

grafico_mes = px.line(mensual, x="mes", y="disponibilidad", markers=True)
grafico_mes.update_yaxes(range=[0, 100], title="Disponibilidad (%)")
grafico_mes.update_xaxes(dtick=1)
grafico_mes.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="Meta 80%", annotation_position="top left")
st.plotly_chart(grafico_mes)

st.subheader("Detalle")
st.dataframe(pareto, hide_index=True)