import pandas as pd
import plotly.express as px
import streamlit as st

# ===== Parámetros (ficha de la empresa, sección 7) =====
VELOCIDAD_IDEAL = 8 / 7                # t/h por reactor (lote de 8 t en 7 h)
HORAS_PLANIFICADAS_ANIO = 8424 * 2     # horas-reactor: 2 reactores, descontando la parada anual
META = {"OEE": 62, "Disponibilidad": 80, "Rendimiento": 85, "Calidad": 92}
ALERTA_OEE = 50                        # bajo este valor, el OEE es crítico (rojo)


def calcular_oee(horas_planificadas, horas_detenidas, toneladas, toneladas_buenas):
    """Devuelve disponibilidad, rendimiento, calidad y OEE, en porcentaje."""
    horas_operativas = horas_planificadas - horas_detenidas
    disponibilidad = horas_operativas / horas_planificadas
    rendimiento = toneladas / (VELOCIDAD_IDEAL * horas_operativas)
    calidad = toneladas_buenas / toneladas
    oee = disponibilidad * rendimiento * calidad
    return disponibilidad * 100, rendimiento * 100, calidad * 100, oee * 100


# ===== Configuración de la página =====
st.set_page_config(page_title="QuimBío · Monitoreo L1", page_icon="🏭", layout="wide")
st.title("🏭 QuimBío Minería · Monitoreo Línea 1")
st.caption("Empresa ficticia – proyecto de portafolio de Loreto")

# ===== Leer los datos =====
detenciones = pd.read_csv("data/detenciones_L1_2026.csv")
lotes = pd.read_csv("data/lotes_L1_2026.csv")
lotes["fin"] = pd.to_datetime(lotes["fin"])

# Turno del lote: según la hora en que terminó
lotes["turno"] = "Noche"
lotes.loc[lotes["fin"].dt.hour.between(8, 19), "turno"] = "Día"

# ===== Filtro por turno =====
st.sidebar.header("Filtros")
turno = st.sidebar.selectbox("Turno", ["Todos", "Día", "Noche"])

horas_planificadas = HORAS_PLANIFICADAS_ANIO
if turno != "Todos":
    detenciones = detenciones[detenciones["turno"] == turno]
    lotes = lotes[lotes["turno"] == turno]
    horas_planificadas = horas_planificadas / 2   # cada turno tiene la mitad de las horas

# ===== Indicadores del año =====
horas_detenidas = detenciones["minutos"].sum() / 60
toneladas = lotes["toneladas"].sum()
toneladas_buenas = lotes["toneladas_buenas"].sum()
disponibilidad, rendimiento, calidad, oee = calcular_oee(horas_planificadas, horas_detenidas, toneladas, toneladas_buenas)

st.subheader("OEE 2026 y sus factores")
c1, c2, c3, c4 = st.columns(4)
c1.metric("OEE", f"{oee:.1f} %", f"{oee - META['OEE']:.1f} pts vs meta")
c2.metric("Disponibilidad", f"{disponibilidad:.1f} %", f"{disponibilidad - META['Disponibilidad']:.1f} pts vs meta")
c3.metric("Rendimiento", f"{rendimiento:.1f} %", f"{rendimiento - META['Rendimiento']:.1f} pts vs meta")
c4.metric("Calidad", f"{calidad:.1f} %", f"{calidad - META['Calidad']:.1f} pts vs meta")

c5, c6, c7 = st.columns(3)
c5.metric("Toneladas buenas", f"{toneladas_buenas:,.0f} t".replace(",", "."))
c6.metric("Horas-reactor detenidas", f"{horas_detenidas:.0f} h")
c7.metric("N° de detenciones", len(detenciones))

# ===== Pareto de causas de detención =====
pareto = detenciones.groupby("causa")["minutos"].sum().sort_values(ascending=False).to_frame()
pareto["horas"] = (pareto["minutos"] / 60).round(1)
pareto["porcentaje"] = (pareto["minutos"] / pareto["minutos"].sum() * 100).round(1)
pareto["acumulado"] = (pareto["minutos"].cumsum() / pareto["minutos"].sum() * 100).round(1)
pareto = pareto.reset_index()

st.subheader("Pareto de causas de detención")
grafico = px.bar(pareto, x="causa", y="horas", text="porcentaje")
grafico.update_traces(texttemplate="%{text} %")
st.plotly_chart(grafico)

# ===== OEE mensual =====
st.subheader("OEE mensual")
detenciones["mes"] = pd.to_datetime(detenciones["fecha"]).dt.month
lotes["mes"] = lotes["fin"].dt.month

mensual = pd.DataFrame({"mes": range(1, 13)})
mensual["horas_detenidas"] = mensual["mes"].map(detenciones.groupby("mes")["minutos"].sum() / 60).fillna(0)
mensual["toneladas"] = mensual["mes"].map(lotes.groupby("mes")["toneladas"].sum())
mensual["toneladas_buenas"] = mensual["mes"].map(lotes.groupby("mes")["toneladas_buenas"].sum())

# Horas-reactor planificadas de cada mes: horas del mes × 2 reactores, menos la parada anual de febrero
horas_del_mes = pd.Series(pd.date_range("2026-01-01", "2027-01-01", freq="h", inclusive="left")).dt.month.value_counts()
mensual["horas_planificadas"] = mensual["mes"].map(horas_del_mes) * 2
mensual.loc[mensual["mes"] == 2, "horas_planificadas"] -= 14 * 24 * 2
if turno != "Todos":
    mensual["horas_planificadas"] = mensual["horas_planificadas"] / 2

# La misma función, ahora aplicada a las 12 filas a la vez
mensual["disponibilidad"], mensual["rendimiento"], mensual["calidad"], mensual["oee"] = calcular_oee(
    mensual["horas_planificadas"], mensual["horas_detenidas"], mensual["toneladas"], mensual["toneladas_buenas"])

# Semáforo de 3 colores (ficha, sección 7)
nombres_meses = {1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
                 7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"}
mensual["nombre_mes"] = mensual["mes"].map(nombres_meses)
mensual["estado"] = "Cumple meta (≥ 62%)"
mensual.loc[mensual["oee"] < META["OEE"], "estado"] = "Alerta (50–62%)"
mensual.loc[mensual["oee"] < ALERTA_OEE, "estado"] = "Crítico (< 50%)"

grafico_mes = px.bar(mensual, x="nombre_mes", y=mensual["oee"].round(1), color="estado", text=mensual["oee"].round(1),
                     color_discrete_map={"Cumple meta (≥ 62%)": "#2E7D32", "Alerta (50–62%)": "#B26A00",
                                         "Crítico (< 50%)": "#C62828"},
                     category_orders={"nombre_mes": list(nombres_meses.values())})
grafico_mes.update_traces(texttemplate="%{text}%", textposition="inside", insidetextanchor="start",
                          textfont_color="white", hovertemplate="%{x}: %{y}%<extra></extra>")
grafico_mes.update_yaxes(range=[0, 100], title="OEE (%)")
grafico_mes.update_xaxes(title="")
grafico_mes.update_layout(legend_title_text="")
grafico_mes.add_hline(y=META["OEE"], line_dash="dash", line_color="black",
                      annotation_text="Meta 62%", annotation_position="top left")
grafico_mes.add_hline(y=ALERTA_OEE, line_dash="dot", line_color="gray",
                      annotation_text="Alerta 50%", annotation_position="bottom left")
st.plotly_chart(grafico_mes)

# Tabla mensual con los tres factores
tabla = mensual[["nombre_mes", "disponibilidad", "rendimiento", "calidad", "oee", "toneladas_buenas"]].round(1)
tabla.columns = ["Mes", "Disponibilidad (%)", "Rendimiento (%)", "Calidad (%)", "OEE (%)", "Toneladas buenas"]
st.dataframe(tabla, hide_index=True)

st.subheader("Detalle del Pareto")
st.dataframe(pareto, hide_index=True)