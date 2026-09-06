import streamlit as st

# Configuración del título de la pestaña del navegador
st.set_page_config(page_title="Liquidador TSG Moreno", page_icon="🏛️", layout="wide")

# TITULO REQUERIDO
st.markdown("<h2 style='text-align: center; color: #1e3a8a;'>TASAS POR SERVICIOS GENERALES</h2>", unsafe_allow_html=True)
st.write("---")

# =====================================================================
# INTERFAZ DE USUARIO: FORMULARIO DE CARGA DE DATOS
# =====================================================================
col_form1, col_form2 = st.columns(2)

with col_form1:
    partida = st.text_input("PARTIDA N°:", value="1")
    estado_sel = st.radio("Estado:", ["EDIFICADO", "BALDIO"], horizontal=True)
    uso_sel = st.radio("Uso:", ["RESIDENCIAL", "COMERCIAL", "INDUSTRIAL"], horizontal=True)
    var_acceso = st.radio("Acceso Principal:", ["SI", "NO"], index=1, horizontal=True)
    
    st.markdown("**DESCUENTOS:**")
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1: var_bc = st.radio("BC 10%:", ["SI", "NO"], index=1, horizontal=True)
    with col_d2: var_da = st.radio("DA 10%:", ["SI", "NO"], index=1, horizontal=True)
    with col_d3: var_be = st.radio("BE 5%:", ["SI", "NO"], index=1, horizontal=True)
    
    monto_edenor = st.number_input("EDENOR ($):", min_value=0.0, value=0.0, step=10.0)

with col_form2:
    var_zonif = st.radio("ZONIFICACION:", ["A/B", "F", "OTRA"], horizontal=True)
    var_tope = st.radio("LIBERAR TOPE:", ["SI", "NO"], index=1, horizontal=True)
    anio_sel = st.selectbox("VALUACION año:", ["2023 o anterior", "2024", "2025", "2026"], index=3)
    
    sup_terreno = st.number_input("SUPERFICIE DE TERRENO (m²):", min_value=0.0, value=300.0)
    sup_edificada = st.number_input("SUPERFICIE EDIFICADA (m²):", min_value=0.0, value=200.0)
    va = st.number_input("VALUACION ($):", min_value=0.0, value=300000.0, step=1000.0)

# =====================================================================
# MATEMÁTICA Y LÓGICA TRIBUTARIA DE MORENO
# =====================================================================
# Coeficiente CA
if anio_sel == "2023 o anterior": ca = 19.10
elif anio_sel == "2024": ca = 2.76
elif anio_sel == "2025": ca = 1.36
else: ca = 1.00

# Coeficiente CU
if uso_sel == "RESIDENCIAL": cu = 1.0
elif uso_sel == "COMERCIAL": cu = 1.1
else: cu = 1.25

# Coeficiente CB
if estado_sel == "EDIFICADO": cb = 1.0
else: cb = 1.6 if sup_terreno <= 500 else 1.7 if sup_terreno <= 5000 else 2.0

# Coeficiente CAP
if var_acceso == "SI":
    if uso_sel == "RESIDENCIAL" and estado_sel == "EDIFICADO": cap = 1.2
    elif estado_sel == "BALDIO": cap = 1.6
    else: cap = 1.5
else: cap = 1.0

# BI = VA X CA X CU X CB X CAP
bi = round(va * ca * cu * cb * cap, 2)

# Tabla Progresiva
if bi <= 5730000: lim_inf, cfa_val, alic = 0.0, 107883.00, 0.0
elif bi <= 6446250: lim_inf, cfa_val, alic = 5730000.0, 107883.00, 0.0150
elif bi <= 7305750: lim_inf, cfa_val, alic = 6446250.0, 123095.84, 0.0152
elif bi <= 8165250: lim_inf, cfa_val, alic = 7305750.0, 141843.90, 0.0154
elif bi <= 12892500: lim_inf, cfa_val, alic = 8165250.0, 160838.66, 0.0156
elif bi <= 21487500: lim_inf, cfa_val, alic = 12892500.0, 328337.79, 0.0160
elif bi <= 30082500: lim_inf, cfa_val, alic = 21487500.0, 649028.37, 0.0164
elif bi <= 38677500: lim_inf, cfa_val, alic = 30082500.0, 838975.84, 0.0169
elif bi <= 47272500: lim_inf, cfa_val, alic = 38677500.0, 1096761.73, 0.0170
elif bi <= 154447750: lim_inf, cfa_val, alic = 47272500.0, 163308.75, 0.0171
elif bi <= 1000000000: lim_inf, cfa_val, alic = 154447750.0, 4201777.78, 0.0173
else: lim_inf, cfa_val, alic = 1000000000.0, 25380696.47, 0.0183

excedente = max(0.0, bi - lim_inf)
tasa_anual = round(((excedente * alic) + cfa_val), 2)
tasa_mensual = round(tasa_anual / 12, 2)

tasa_proteccion = round(tasa_mensual * 0.095, 2)
tasa_salud = round(tasa_mensual * 0.105, 2)

porcentaje_desc = 0.0
if var_bc == "SI": porcentaje_desc += 0.10
if var_da == "SI": porcentaje_desc += 0.10
if var_be == "SI": porcentaje_desc += 0.05

monto_descuentos_fijos = round(tasa_mensual * porcentaje_desc, 2)
total_descuentos = round(monto_descuentos_fijos + monto_edenor, 2)

tasa_total = round((tasa_mensual + tasa_proteccion + tasa_salud) - total_descuentos, 2)

if var_tope == "NO" and tasa_total < 4500.0:
    tasa_total = 8900.0 if estado_sel == "BALDIO" else 4500.0

# =====================================================================
# PRESENTACIÓN DE RESULTADOS INTEGRADOS EN TIEMPO REAL
# =====================================================================
st.write("---")
st.markdown("### 📊 MARCO INTEGRADO DE RESULTADOS (Cálculo Automático)")

col_res1, col_res2 = st.columns(2)

with col_res1:
    st.write(f"**BI (Valuación Municipal Ajustada):** ${bi:,.2f}")
    st.write(f"**LÍMITE INFERIOR:** ${lim_inf:,.2f}")
    st.write(f"**ALÍCUOTA:** {alic * 100:.2f}%")
    st.write(f"**CUOTA FIJA ANUAL (CFA):** ${cfa_val:,.2f}")
    st.write(f"**TASA ANUAL:** ${tasa_anual:,.2f}")

with col_res2:
    st.write(f"**TASA MENSUAL:** ${tasa_mensual:,.2f}")
    st.write(f"**TASA PROTECCIÓN (9.5%):** ${tasa_proteccion:,.2f}")
    st.write(f"**TASA SALUD (10.5%):** ${tasa_salud:,.2f}")
    st.write(f"**DESCUENTOS APLICADOS:** -${total_descuentos:,.2f}")

st.write("---")
st.error(f"## **TASA TOTAL MENSUAL CON ADICIONALES: ${tasa_total:,.2f}**")

if st.button("🖨️ IMPRIMIR REPORTE"):
    st.success("Comprobante generado. Presione Ctrl+P en su navegador para imprimir.")
