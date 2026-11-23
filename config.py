"""
Parámetros de la planta y metas de gestión de la Línea 1 de QuimBío Minería.

Es la única fuente de estos valores: el simulador y el dashboard los importan desde aquí.
Fuente: docs/ficha_empresa.md (secciones 4, 5 y 7).
"""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# ===== Período de análisis =====
INICIO = datetime(2026, 1, 1, 0, 0)
FIN = datetime(2027, 1, 1, 0, 0)

# ===== Línea 1: cuello de botella (reactores de polimerización) =====
REACTORES = ["QBM-L1-R01", "QBM-L1-R02"]
HORAS_REACCION = 7                                       # duración ideal de un lote
TONELADAS_POR_LOTE = 8
VELOCIDAD_IDEAL = TONELADAS_POR_LOTE / HORAS_REACCION    # t/h por reactor

# ===== Parada anual programada (mantención mayor de verano) =====
INICIO_PARADA = datetime(2026, 2, 1, 8, 0)
DIAS_PARADA = 14

# ===== Horas-reactor planificadas del período =====
# Fecha de corte: medianoche de hoy en Chile (lo posterior aún no ocurre)
HOY = datetime.now(ZoneInfo("America/Santiago")).replace(
    hour=0, minute=0, second=0, microsecond=0, tzinfo=None
)
CORTE = min(HOY, FIN)

# Horas del período, desde el inicio hasta el corte
HORAS_PERIODO = (CORTE - INICIO).total_seconds() / 3600

# Horas de parada que ya ocurrieron antes del corte
FIN_PARADA = INICIO_PARADA + timedelta(days=DIAS_PARADA)
HORAS_PARADA = max(0, (min(CORTE, FIN_PARADA) - INICIO_PARADA).total_seconds() / 3600)

HORAS_PLANIFICADAS = (HORAS_PERIODO - HORAS_PARADA) * len(REACTORES)

# ===== Metas de gestión (ficha, sección 7) =====
META = {"OEE": 62, "Disponibilidad": 80, "Rendimiento": 85, "Calidad": 92}
ALERTA_OEE = 50

# ===== Catálogo de causas de detención (ficha, sección 6) =====
CAUSAS = {
    "D01": "Limpieza entre lotes",
    "D02": "Espera del laboratorio",
    "D03": "Falla mecánica",
    "D04": "Falta de materia prima",
    "D05": "Alarma de seguridad del reactor",
    "D06": "Falla de caldera o corte de vapor",
    "D07": "Alarma de olor o falla del lavador",
    "D08": "Episodio crítico (PPDA)",
}
# Colores de la marca (los mismos del sitio)
AZUL_PETROLEO = "#0B3C5D"
COBRE = "#B87333"