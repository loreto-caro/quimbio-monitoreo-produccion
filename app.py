import pandas as pd
import plotly.express as px
import streamlit as st

from config import (ALERTA_OEE, CAUSAS, DIAS_PARADA, FIN, HORAS_PLANIFICADAS, INICIO,
                    INICIO_PARADA, META, REACTORES, VELOCIDAD_IDEAL)
from config import AZUL_PETROLEO, COBRE

# Textos del semáforo, construidos a partir de las metas
ESTADO_VERDE = f"Cumple meta (≥ {META['OEE']}%)"
ESTADO_AMARILLO = f"Alerta ({ALERTA_OEE}–{META['OEE']}%)"
ESTADO_ROJO = f"Crítico (< {ALERTA_OEE}%)"


def formato_cl(valor, decimales=1):
    """Formatea un número al estilo chileno: punto para los miles y coma para los decimales."""
    texto = f"{valor:,.{decimales}f}"          # estilo inglés: 12,380.5
    return texto.replace(",", "#").replace(".", ",").replace("#", ".")


def calcular_oee(horas_planificadas, horas_detenidas, toneladas, toneladas_buenas):
    """Devuelve disponibilidad, rendimiento, calidad y OEE, en porcentaje."""
    horas_operativas = horas_planificadas - horas_detenidas
    disponibilidad = horas_operativas / horas_planificadas
    rendimiento = toneladas / (VELOCIDAD_IDEAL * horas_operativas)
    calidad = toneladas_buenas / toneladas
    oee = disponibilidad * rendimiento * calidad
    return disponibilidad * 100, rendimiento * 100, calidad * 100, oee * 100


def tarjeta(columna, titulo, valor, meta):
    """Muestra una tarjeta con un porcentaje y su diferencia con la meta."""
    columna.metric(titulo, f"{formato_cl(valor)} %", f"{formato_cl(valor - meta)} pts vs meta")


# ===== Configuración de la página =====
st.set_page_config(page_title="QuimBío · Monitoreo L1", page_icon="🏭", layout="wide")
st.markdown(
    f'<p style="font-family: Montserrat; font-weight: 700; font-size: 22px; '
    f'color: {AZUL_PETROLEO}; margin-bottom: 0;">'
    f'Quim<span style="color: {COBRE};">Bío</span> Minería</p>',
    unsafe_allow_html=True,
)
st.title("Monitoreo de producción · Línea 1")
st.caption(
    "Empresa ficticia – proyecto de portafolio de Loreto Caro · "
    "[Volver al sitio](https://loreto-caro.github.io/quimbio-monitoreo-produccion/)"
)

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

horas_planificadas = HORAS_PLANIFICADAS
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
tarjeta(c1, "OEE", oee, META["OEE"])
tarjeta(c2, "Disponibilidad", disponibilidad, META["Disponibilidad"])
tarjeta(c3, "Rendimiento", rendimiento, META["Rendimiento"])
tarjeta(c4, "Calidad", calidad, META["Calidad"])

c5, c6, c7 = st.columns(3)
c5.metric("Toneladas buenas", f"{formato_cl(toneladas_buenas, 0)} t")
c6.metric("Horas-reactor detenidas", f"{formato_cl(horas_detenidas, 0)} h")
c7.metric("N° de detenciones", formato_cl(len(detenciones), 0))

# ===== Pareto de causas de detención =====
pareto = detenciones.groupby("causa")["minutos"].sum().sort_values(ascending=False).to_frame().reset_index()
pareto["nombre"] = pareto["causa"] + " · " + pareto["causa"].map(CAUSAS)
pareto["horas"] = pareto["minutos"] / 60
pareto["porcentaje"] = pareto["minutos"] / pareto["minutos"].sum() * 100
pareto["acumulado"] = pareto["minutos"].cumsum() / pareto["minutos"].sum() * 100

st.subheader("Pareto de causas de detención")
grafico = px.bar(pareto, x="nombre", y="horas", text="porcentaje", color_discrete_sequence=[AZUL_PETROLEO])
grafico.update_traces(texttemplate="%{text:.1f} %", hovertemplate="%{x}: %{y:,.0f} h<extra></extra>")
grafico.update_xaxes(title="")
grafico.update_yaxes(title="Horas-reactor")
grafico.update_layout(separators=",.")
st.plotly_chart(grafico)

# ===== OEE mensual =====
st.subheader("OEE mensual")
detenciones["mes"] = pd.to_datetime(detenciones["fecha"]).dt.month
lotes["mes"] = lotes["fin"].dt.month

mensual = pd.DataFrame({"mes": range(1, 13)})
mensual["horas_detenidas"] = mensual["mes"].map(detenciones.groupby("mes")["minutos"].sum() / 60).fillna(0)
mensual["toneladas"] = mensual["mes"].map(lotes.groupby("mes")["toneladas"].sum())
mensual["toneladas_buenas"] = mensual["mes"].map(lotes.groupby("mes")["toneladas_buenas"].sum())

# Horas-reactor planificadas de cada mes: horas del mes × reactores, menos la parada anual
# (supuesto: la parada completa cae dentro del mes en que comienza)
horas_del_mes = pd.Series(pd.date_range(INICIO, FIN, freq="h", inclusive="left")).dt.month.value_counts()
mensual["horas_planificadas"] = mensual["mes"].map(horas_del_mes) * len(REACTORES)
mensual.loc[mensual["mes"] == INICIO_PARADA.month, "horas_planificadas"] -= DIAS_PARADA * 24 * len(REACTORES)
if turno != "Todos":
    mensual["horas_planificadas"] = mensual["horas_planificadas"] / 2

# La misma función, ahora aplicada a las 12 filas a la vez
mensual["disponibilidad"], mensual["rendimiento"], mensual["calidad"], mensual["oee"] = calcular_oee(
    mensual["horas_planificadas"], mensual["horas_detenidas"], mensual["toneladas"], mensual["toneladas_buenas"])

# Semáforo de 3 niveles (ficha, sección 7)
nombres_meses = {1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
                 7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"}
mensual["nombre_mes"] = mensual["mes"].map(nombres_meses)
mensual["estado"] = ESTADO_VERDE
mensual.loc[mensual["oee"] < META["OEE"], "estado"] = ESTADO_AMARILLO
mensual.loc[mensual["oee"] < ALERTA_OEE, "estado"] = ESTADO_ROJO

grafico_mes = px.bar(mensual, x="nombre_mes", y="oee", color="estado", text="oee",
                     color_discrete_map={ESTADO_VERDE: "#2E7D32", ESTADO_AMARILLO: "#B26A00", ESTADO_ROJO: "#C62828"},
                     category_orders={"nombre_mes": list(nombres_meses.values())})
grafico_mes.update_traces(texttemplate="%{text:.1f}%", textposition="inside", insidetextanchor="start",
                          textfont_color="white", hovertemplate="%{x}: %{y:.1f}%<extra></extra>")
grafico_mes.update_yaxes(range=[0, 100], title="OEE (%)")
grafico_mes.update_xaxes(title="")
grafico_mes.update_layout(legend_title_text="", separators=",.")
grafico_mes.add_hline(y=META["OEE"], line_dash="dash", line_color="black",
                      annotation_text=f"Meta {META['OEE']}%", annotation_position="top left")
grafico_mes.add_hline(y=ALERTA_OEE, line_dash="dot", line_color="gray",
                      annotation_text=f"Alerta {ALERTA_OEE}%", annotation_position="bottom left")
st.plotly_chart(grafico_mes)

# Tabla mensual con los tres factores, en formato chileno
tabla = pd.DataFrame({
    "Mes": mensual["nombre_mes"],
    "Disponibilidad (%)": mensual["disponibilidad"].map(formato_cl),
    "Rendimiento (%)": mensual["rendimiento"].map(formato_cl),
    "Calidad (%)": mensual["calidad"].map(formato_cl),
    "OEE (%)": mensual["oee"].map(formato_cl),
    "Toneladas buenas": mensual["toneladas_buenas"].map(lambda valor: formato_cl(valor, 0)),
})
st.dataframe(tabla, hide_index=True)

# ===== Detalle del Pareto =====
st.subheader("Detalle del Pareto")
detalle = pd.DataFrame({
    "Causa": pareto["nombre"],
    "Horas-reactor": pareto["horas"].map(formato_cl),
    "% del tiempo detenido": pareto["porcentaje"].map(formato_cl),
    "% acumulado": pareto["acumulado"].map(formato_cl),
})
st.dataframe(detalle, hide_index=True)