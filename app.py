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

META_DISPONIBILIDAD = 80
horas_planificadas = 8424 * 2  # horas-reactor: 2 reactores, descontando la parada anual de 14 días
if turno != "Todos":
    df = df[df["turno"] == turno]
    horas_planificadas = horas_planificadas / 2  # cada turno tiene la mitad de las horas

# Indicadores del año
horas_detenidas = df["minutos"].sum() / 60
disponibilidad = (horas_planificadas - horas_detenidas) / horas_planificadas * 100

col1, col2, col3 = st.columns(3)
col1.metric("Disponibilidad 2026", f"{disponibilidad:.1f} %", f"{disponibilidad - META_DISPONIBILIDAD:.1f} pts vs meta")
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

# Disponibilidad mensual con semáforo
st.subheader("Disponibilidad mensual")
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

# Semáforo: nombre del mes y estado frente a la meta
nombres_meses = {1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
                 7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"}
mensual["nombre_mes"] = mensual["mes"].map(nombres_meses)
mensual["estado"] = "Cumple meta"
mensual.loc[mensual["disponibilidad"] < META_DISPONIBILIDAD, "estado"] = "Bajo meta"

grafico_mes = px.bar(mensual, x="nombre_mes", y="disponibilidad", color="estado", text="disponibilidad",
                     color_discrete_map={"Cumple meta": "#2E7D32", "Bajo meta": "#C62828"},
                     category_orders={"nombre_mes": list(nombres_meses.values())})
grafico_mes.update_traces(texttemplate="%{text}%", textposition="inside", insidetextanchor="start", textfont_color="white", hovertemplate="%{x}: %{y}%<extra></extra>")
grafico_mes.update_layout(legend_title_text="")
grafico_mes.update_yaxes(range=[0, 100], title="Disponibilidad (%)")
grafico_mes.update_xaxes(title="")
grafico_mes.add_hline(y=META_DISPONIBILIDAD, line_dash="dash", line_color="black",
                      annotation_text="Meta 80%", annotation_position="top left")
st.plotly_chart(grafico_mes)

st.subheader("Detalle del Pareto")
st.dataframe(pareto, hide_index=True)