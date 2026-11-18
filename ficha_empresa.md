# FICHA EMPRESA FICTICIA: QUIMBÍO MINERÍA S.A. (QBM)
Versión 1.1 (definitiva) · 18 de noviembre de 2026

Proyecto de portafolio de Loreto, futura Ingeniera Civil Industrial (UNAB).
Objetivo: construir en Python un sistema de monitoreo y mejora de producción
(producción, mantención, calidad, ambiente y logística), más una página web corporativa.

> **Empresa ficticia.** Todos los datos son inventados con fines de aprendizaje.

---

## 1. IDENTIDAD

- **Nombre:** QuimBío Minería S.A. | **Sigla:** QBM | **Fundación (ficticia):** 2019
- **Rubro:** fabricación de reactivos químicos para la minería del cobre
- **Ubicación:** Parque Industrial Escuadrón, Coronel, Región del Biobío, Chile
- **Despacho:** Puerto de Coronel → Antofagasta / Mejillones (clientes mineros)
- **Lema:** "Química para la minería, hecha con conciencia."
- **Misión:** Fabricar reactivos químicos de alta calidad para la minería chilena,
  con procesos seguros, limpios y transparentes, que generen empleo local y
  respeten a la comunidad que nos acoge.
- **Visión:** Ser al 2030 el proveedor chileno de reactivos mineros de referencia
  en eficiencia operacional y buena vecindad.
- **Valores:** Seguridad primero · Transparencia · Respeto por la comunidad ·
  Excelencia operacional · Mejora continua
- **Certificaciones (ficticias):** ISO 9001, ISO 14001, ISO 45001
- **Contexto real:** Coronel está en zona saturada por MP2,5 (PPDA Concepción
  Metropolitano) y tiene historia de olores de la industria pesquera.
  QuimBío se define como empresa modelo, estricta con comunidad y ambiente.

### Uso interno (NO publicar en la web)
- **Empresas reales comparables, solo como referencia de diseño:** Proquimin, SNF Chile, Molycop.
  No deben aparecer en la página pública, para no sugerir ninguna relación con ellas.
- **Antes de publicar:** verificar en Google y en el registro de empresas que no exista
  una empresa real llamada "QuimBío" o con la sigla "QBM" en el mismo rubro.
  Si existe, cambiar el nombre.

---

## 2. LOS 7 COMPROMISOS (metas medibles)

1. **Cero olores fuera de la planta** → 0 reclamos por olor con fundamento al mes
2. **Aire limpio** (caldera a gas natural) → emisiones < 50% del límite legal
3. **Agua responsable** → ≥ 70% de agua recirculada, 100% de RILes tratados
4. **Residuos** → ≥ 80% de residuos valorizados
5. **Seguridad de procesos** → 0 accidentes graves, 2 simulacros/año con vecinos
6. **Empleo local** → ≥ 60% de la dotación de Coronel y Lota (≥ 90 de 150 personas)
7. **Transparencia** → datos ambientales publicados mensualmente en la web,
   100% de reclamos respondidos en < 48 h

---

## 3. PRODUCTOS

| Línea | Producto | Uso en minería | Presentación |
|---|---|---|---|
| L1 | QBM-FLOC (floculante, poliacrilamida en polvo) | Recuperar agua de relaves | Sacos de 25 kg, maxisacos de 750 kg |
| L2 | QBM-XAN (xantato en pellets) | Colector de flotación de cobre | Maxisacos de 800 kg, tambores |
| L3 | QBM-ESP (espumante líquido) | Formar espuma en la flotación | IBC de 1.000 L, tambores de 200 L |

**Capacidad comprometida:** 30.000 t/año (L1 12.000 · L2 10.000 · L3 8.000)

---

## 4. MÁQUINAS

Código: `QBM-Línea-Tipo+N°`

### Línea 1, Floculantes (proceso por lotes + continuo)
| Código | Equipo | Capacidad |
|---|---|---|
| QBM-L1-R01 | Reactor de polimerización 1 | Lote de 8 t cada 7 h = 1,143 t/h |
| QBM-L1-R02 | Reactor de polimerización 2 | Lote de 8 t cada 7 h = 1,143 t/h |
| QBM-L1-SEC01 | Secador de lecho fluido | 2,8 t/h |
| QBM-L1-MOL01 | Molino y tamiz | 2,8 t/h |
| QBM-L1-ENV01 | Envasadora de sacos de 25 kg | 120 sacos/h = 3,0 t/h |

**Cuello de botella:** reactores (2,286 t/h en conjunto)

### Línea 2, Xantatos (proceso por lotes + continuo; usa CS2, riesgo de inflamabilidad)
| Código | Equipo | Capacidad |
|---|---|---|
| QBM-L2-R01 | Reactor de síntesis 1 | Lote de 5 t cada 5 h = 1,0 t/h |
| QBM-L2-R02 | Reactor de síntesis 2 | Lote de 5 t cada 5 h = 1,0 t/h |
| QBM-L2-SEC01 | Secador al vacío | 2,4 t/h |
| QBM-L2-PEL01 | Peletizadora | 2,4 t/h |
| QBM-L2-ENV01 | Envasadora de maxisacos de 800 kg | 4 maxisacos/h = 3,2 t/h |

**Cuello de botella:** reactores (2,0 t/h en conjunto)

### Línea 3, Espumantes (mezcla rápida)
| Código | Equipo | Capacidad |
|---|---|---|
| QBM-L3-MEZ01 | Estanque de mezcla | Lote de 5 t cada 2,5 h = 2,0 t/h |
| QBM-L3-FIL01 | Filtro de cartuchos | 2,5 t/h |
| QBM-L3-LLE01 | Llenadora de IBC y tambores | 2 IBC/h = 1,8 t/h (densidad 0,9 t/m³) |

**Cuello de botella:** llenadora (1,8 t/h)

### Equipos de apoyo
| Código | Equipo |
|---|---|
| QBM-AMB-LAV01 | Lavador de gases de la L2 (control de olores) |
| QBM-AMB-PTR01 | Planta de tratamiento de RILes |
| QBM-AMB-SO01 a SO04 | Sensores de olor en el perímetro (4) |
| QBM-SRV-CAL01 | Caldera a gas natural (vapor para los secadores) |

**Código de lote:** `QBM-L2026-0001` (correlativo por año)

---

## 5. TURNOS Y DOTACIÓN

### Sistemas de turno
- **L1 y L2:** 24/7, sistema 4x4 (4 días de 12 h, 4 de descanso), grupos A, B, C, D.
  Turno día 08:00–20:00 | Turno noche 20:00–08:00.
  Cada grupo trabaja en promedio unas 42 h semanales.
- **L3:** 24/5 (lunes a viernes), 3 turnos de 8 h: 07–15, 15–23, 23–07.
  3 cuadrillas fijas de 4 personas (40 h semanales).
- **Áreas de apoyo:** lunes a viernes, 08:00–17:30.

### Equipo presente en cada turno 4x4 (14 personas)
Cada persona pertenece a su área de origen y se cuenta **una sola vez** en la dotación.

| Rol en el turno | Cantidad | Área de origen |
|---|---|---|
| Supervisor de turno | 1 | Operaciones |
| Operadores L1 | 4 | Operaciones |
| Operadores L2 | 4 | Operaciones |
| Técnico de seguridad de procesos | 1 | Prevención |
| Mantenedores | 2 | Mantención |
| Analista de laboratorio | 1 | Calidad |
| Operador ambiental | 1 | Ambiente y comunidad |
| **Total por turno** | **14** | |

### Dotación total: 150 personas
| Área | Personal de turno | Personal diurno | Total |
|---|---|---|---|
| Operaciones 4x4 (L1 y L2) | 36 (9 × 4 grupos) | 0 | 36 |
| Operaciones L3 | 12 (4 × 3 cuadrillas) | 0 | 12 |
| Jefatura de producción (gerente de planta, jefe de producción, ingeniero de procesos, planificador) | 0 | 4 | 4 |
| Mantención | 8 (2 × 4 grupos) | 8 (jefe, planificador, 2 eléctricos, 2 instrumentistas, 2 mecánicos) | 16 |
| Calidad | 4 (1 × 4 grupos) | 8 (jefa, 3 analistas de liberación, 2 de materias primas, encargado ISO, administrativo) | 12 |
| Ambiente y comunidad | 4 (1 × 4 grupos) | 4 (jefe de ambiente, encargada de comunidad, analista ambiental, operador PTR) | 8 |
| Prevención de riesgos | 4 (1 × 4 grupos) | 3 (jefe y 2 prevencionistas) | 7 |
| Logística (bodega, despachos, compras) | 0 | 22 | 22 |
| Administración, finanzas, personas, ventas, TI y gerencia | 0 | 33 | 33 |
| **Total** | **68** | **82** | **150** |

### Horas planificadas al año
- **L1 y L2:** 8.424 h (8.760 h del año menos 14 días de parada anual)
- **L3:** 6.000 h (24 h × 5 días × 50 semanas)

---

## 6. CATÁLOGO DE CAUSAS DE DETENCIÓN Y PROBLEMAS (23)

### Disponibilidad (máquina detenida)
| Código | Causa |
|---|---|
| D01 | Limpieza y cambio de producto entre lotes (la mayor pérdida en procesos por lotes) |
| D02 | Espera de liberación del laboratorio |
| D03 | Falla mecánica (agitador, bomba, molino) |
| D04 | Falta de materia prima |
| D05 | Detención por alarma de seguridad del reactor (L2) |
| D06 | Falla de la caldera o corte de vapor |
| D07 | Detención preventiva por alarma de olor o falla del lavador de gases (L2) |
| D08 | Restricción por episodio crítico de contaminación del aire (PPDA) |

### Rendimiento (funciona más lento)
| Código | Causa |
|---|---|
| R01 | Gel muy húmedo, el secador va más lento (L1) |
| R02 | Polvo pegajoso que atasca el molino (L1) |
| R03 | Sacos rotos o ajustes de peso en la envasadora |
| R04 | Ciclo del reactor más largo por control de temperatura |
| R05 | Microparadas de la llenadora por cambio de IBC a tambor (L3) |

### Calidad (sale malo)
| Código | Causa |
|---|---|
| C01 | Monómero residual de acrilamida sobre el límite (L1) |
| C02 | Xantato con humedad que se descompone y genera CS2 (L2) |
| C03 | Granulometría fuera de rango |
| C04 | Lote completo rechazado en la liberación |

### Logística
| Código | Causa |
|---|---|
| L01 | Cierre del puerto de Coronel por marejadas (~20 días/año) → bodega llena → frenar producción |
| L02 | Bodega de xantato con capacidad limitada por seguridad |

### Ambiente y seguridad
| Código | Causa |
|---|---|
| A01 | Sensor de olor del perímetro sobre el umbral |
| A02 | Reclamo de un vecino |
| A03 | Planta de RILes fuera de parámetro |
| S01 | Fuga o emisión de CS2 en la L2 |

---

## 7. METAS E INDICADORES

### Fórmulas

```
OEE            = Disponibilidad × Rendimiento × Calidad

Disponibilidad = Tiempo operativo / Tiempo planificado
Rendimiento    = Producción real / (Velocidad ideal × Horas operativas)
Calidad        = Toneladas buenas / Producción real

Verificación:
OEE            = Toneladas buenas / (Velocidad ideal × Horas planificadas)

MTBF           = Horas de funcionamiento / N° de fallas
MTTR           = Horas de reparación / N° de fallas
```

El OEE se calcula sobre la **máquina cuello de botella** de cada línea.

### Metas de OEE
Referencia de la industria: una planta por lotes bien gestionada opera entre 50% y 65%.

| Línea | Disponibilidad | Rendimiento | Calidad | OEE meta (verde desde) | Alerta (rojo bajo) |
|---|---|---|---|---|---|
| L1 | 80% | 85% | 92% | 62% | 50% |
| L2 | 78% | 85% | 90% | 60% | 48% |
| L3 | 88% | 90% | 95% | 75% | 60% |

**Semáforo:**
- 🟢 Verde: OEE igual o mayor que la meta
- 🟡 Amarillo: OEE entre la alerta y la meta
- 🔴 Rojo: OEE bajo la alerta

### Coherencia entre capacidad y metas (verificado)

```
L1:  8.424 h × 2,286 t/h × 62%  ≈ 11.940 t/año  → capacidad comprometida 12.000 t
L2:  8.424 h × 2,000 t/h × 60%  ≈ 10.110 t/año  → capacidad comprometida 10.000 t
L3:  6.000 h × 1,800 t/h × 75%  ≈  8.100 t/año  → capacidad comprometida  8.000 t
```

### Ejemplo de validación (turno día L1)
Datos: 720 min planificados, D01 60 min, D03 45 min, 20,0 t producidas, 2,0 t rechazadas (C01).

```
Tiempo operativo = 720 − 60 − 45            = 615 min = 10,25 h
Disponibilidad   = 615 / 720                = 85,4%
Rendimiento      = 20,0 / (2,286 × 10,25)   = 85,4%
Calidad          = 18,0 / 20,0              = 90,0%
OEE              = 0,854 × 0,854 × 0,900    = 65,6%
Verificación     = 18,0 / (2,286 × 12)      = 65,6%  ✅
```

### Otros indicadores
- **Producción:** cumplimiento del plan ≥ 95% · MTBF ≥ 120 h · MTTR ≤ 2 h ·
  liberación del laboratorio ≤ 4 h por lote
- **Ambiente:** reclamos por olor = 0 · horas sobre el umbral de olor = 0 ·
  agua recirculada ≥ 70% · agua ≤ 1,5 m³/t · energía ≤ 350 kWh/t ·
  residuos valorizados ≥ 80% · reclamos respondidos < 48 h = 100% ·
  dotación local ≥ 60%
- **Seguridad:** accidentes graves = 0 · días sin accidentes · 2 simulacros/año
- **Logística:** OTIF ≥ 95% · ocupación de la bodega de xantato ≤ 80% ·
  días de puerto cerrado al mes (monitoreo)

---

## 8. DATOS FICTICIOS A GENERAR (tablas)

`maquinas` · `trabajadores` · `turnos` · `lotes_produccion` · `detenciones` (con código de causa) ·
`control_calidad` · `mediciones_ambientales` (sensores de olor, agua, energía) ·
`reclamos_comunidad` · `despachos` · `estado_puerto`

**Problemas "sembrados" a propósito** (para que el sistema los descubra en los datos):
- D01 (limpieza entre lotes) es la principal pérdida de disponibilidad en L1 y L2.
- Un reactor de la L2 falla más seguido que el otro (MTBF bajo).
- La envasadora de la L1 tiene más sacos rotos (R03) en el turno noche.
- En invierno aumentan los cierres de puerto (L01) y los episodios críticos (D08).

---

## 9. ORDEN DE CONSTRUCCIÓN (por módulos)

| Orden | Módulo | Contenido |
|---|---|---|
| 1 | Producción L1 | Detenciones, OEE y semáforo |
| 2 | Producción L2 y L3 | Se reutiliza lo construido en L1 |
| 3 | Mantención | MTBF, MTTR y fallas por máquina |
| 4 | Calidad | Lotes rechazados y tiempos de liberación |
| 5 | Ambiente y comunidad | Sensores de olor, agua, energía y reclamos |
| 6 | Logística | Puerto, bodega y despachos |
| 7 | Página web corporativa | Vitrina pública y portal interno |

---

## 10. PÁGINA WEB

- **Sitio público:** Inicio · Nosotros (misión, visión, valores, historia) ·
  Productos · Sostenibilidad (7 compromisos + "Datos ambientales en línea") ·
  Comunidad (mesa vecinal, canal de reclamos, empleo local y aprendices) ·
  Trabaja con nosotros · Contacto
- **Portal interno (login de demostración):** dashboards de Producción (OEE),
  Mantención, Ambiente y comunidad, y Seguridad y logística
- **Pie de página obligatorio:** "Empresa ficticia – proyecto de portafolio de Loreto [apellido]"
- **No incluir** nombres de empresas reales en el sitio público.

---

## 11. CÓMO TRABAJAR CONMIGO (instrucciones para el chat)

- Responde siempre en español y actúa como experto en ingeniería industrial,
  procesos químicos y desarrollo en Python.
- Estoy aprendiendo Python desde cero: explica paso a paso y con el porqué
  de cada cosa, con ejemplos resueltos, y avanza solo cuando yo confirme.
- Me sirve la tabla de dos columnas: a la izquierda el desarrollo,
  a la derecha qué se hace y por qué.
- Las fórmulas van siempre en un bloque aparte, nunca dentro de una frase,
  una lista o una celda de tabla.
- Revisa que los números cuadren y avísame si algo no es realista.

---

## REGISTRO DE CAMBIOS

**Versión 1.1 (18-11-2026)**
- Dotación corregida: cada persona del turno 4x4 se cuenta una sola vez, en su área de origen.
  La versión anterior decía 14 personas por turno pero 64 en Operaciones (14 × 4 = 56) y
  contaba en dos áreas a mantenedores, analistas y operadores ambientales.
  Nueva dotación total: 150 personas (antes 180), con Administración bajando de 47 a 33.
- Compromiso 6 expresado en personas: ≥ 90 de 150.
- Las empresas reales comparables pasan a "Uso interno (NO publicar)".
- Se agrega verificación del nombre antes de publicar.
- Se agrega la verificación de coherencia entre capacidad y metas de OEE.
- Se agregan los problemas "sembrados" en los datos y el orden de construcción por módulos.
- Columna "Rojo bajo" renombrada a "Alerta (rojo bajo)" y semáforo explicado.
