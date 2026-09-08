import streamlit as st

st.set_page_config(
    page_title="Liquidador Tasas por Servicios Generales - Municipio de Moreno",
    layout="centered",
)

# Estilos CSS personalizados para modificar colores, fuentes y aspecto general
st.markdown(
    """
    <style>
        /* Color de fondo general de la aplicación */
        .stApp {
            background-color: #f8fafc;
        }
        
        /* Estilo para los títulos principales */
        h3 {
            color: #1e3a8a !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* Personalización de los contenedores de resultados */
        .resultado-box {
            background-color: #ffffff;
            padding: 10px 14px;
            border-radius: 6px;
            border: 1px solid #94a3b8;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        .resultado-label {
            color: #1e3a8a;
            font-weight: 600;
            font-size: 13px;
        }
        
        .resultado-valor {
            color: #0f172a;
            font-weight: bold;
            font-size: 13px;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Encabezado institucional con tono personalizado
st.markdown(
    """
    <div style="background-color: #1e3a8a; padding: 14px; border-radius: 6px; color: white; display: flex; align-items: center;">
        <span style="font-size: 20px; margin-right: 10px;">🏛️</span>
        <span style="font-size: 16px; font-weight: bold;">Liquidador Tasas por Servicios Generales</span>
    </div>
""",
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# Partida municipal centrada
col_p1, col_p2, col_p3 = st.columns([1, 2, 1])
with col_p2:
    partida = st.text_input("PARTIDA MUNICIPAL N°:")

st.markdown("---")

# Controles de entrada organizados en columnas
col1, col2, col3 = st.columns(3)

with col1:
    estado_sel = st.radio("Estado:", ["EDIFICADO", "BALDIO"])
    uso_sel = st.radio("Uso:", ["RESIDENCIAL", "COMERCIAL", "INDUSTRIAL"])

with col2:
    var_acceso = st.radio("Acceso Principal:", ["NO", "SI"])
    var_tope = st.radio("Liberar Tope:", ["NO", "SI"])
    var_zonif = st.selectbox("Zonificación:", ["A/B", "F", "OTRA"])

with col3:
    st.markdown("**Descuentos:**")
    var_bc = st.radio("BC 10%:", ["NO", "SI"], horizontal=True)
    var_da = st.radio("DA 10%:", ["NO", "SI"], horizontal=True)
    var_be = st.radio("BE 5%:", ["NO", "SI"], horizontal=True)
    entry_edenor = st.text_input("EDENOR ($):", "0,00")

st.markdown("---")

col_sup1, col_sup2 = st.columns(2)
with col_sup1:
    entry_sup_terreno = st.text_input(
        "Superficie de Terreno (m²):", "300,00"
    )
with col_sup2:
    entry_sup_edificada = st.text_input(
        "Superficie Edificada (m²):", "0,00"
    )

col_val1, col_val2 = st.columns(2)
with col_val1:
    entry_va = st.text_input("Valuación ($):", "300000,00")
with col_val2:
    anio_sel = st.selectbox(
        "Valuación año:", ["2023 o anterior", "2024", "2025", "2026"]
    )

st.markdown("---")

# Lógica de cálculo
try:
    va = (
        float(entry_va.replace(".", "").replace(",", "."))
        if entry_va
        else 0.0
    )
    sup_terreno = (
        float(entry_sup_terreno.replace(".", "").replace(",", "."))
        if entry_sup_terreno
        else 0.0
    )
    sup_edificada = (
        float(entry_sup_edificada.replace(".", "").replace(",", "."))
        if entry_sup_edificada
        else 0.0
    )
    edenor_val = (
        float(entry_edenor.replace(".", "").replace(",", "."))
        if entry_edenor
        else 0.0
    )

    if anio_sel == "2023 o anterior":
        ca = 19.10
    elif anio_sel == "2024":
        ca = 2.76
    elif anio_sel == "2025":
        ca = 1.36
    else:
        ca = 1.00

    if uso_sel == "RESIDENCIAL":
        cu = 1.0
    elif uso_sel == "COMERCIAL":
        cu = 1.1
    else:
        cu = 1.25

    if estado_sel == "EDIFICADO":
        cb = 1.0
    else:
        cb = 1.6 if sup_terreno <= 500 else 1.7 if sup_terreno <= 5000 else 2.0

    if var_acceso == "SI":
        if uso_sel == "RESIDENCIAL" and estado_sel == "EDIFICADO":
            cap = 1.2
        elif estado_sel == "BALDIO":
            cap = 1.6
        else:
            cap = 1.5
    else:
        cap = 1.0

    bi = round(va * ca * cu * cb * cap, 2)

    if bi <= 5730000:
        lim_inf, cfa_val, alic = 0.0, 107883.00, 0.0
    elif bi <= 6446250:
        lim_inf, cfa_val, alic = 5730000.0, 107883.00, 0.0150
    elif bi <= 7305750:
        lim_inf, cfa_val, alic = 6446250.0, 123095.84, 0.0152
    elif bi <= 8165250:
        lim_inf, cfa_val, alic = 7305750.0, 141843.90, 0.0154
    elif bi <= 12892500:
        lim_inf, cfa_val, alic = 8165250.0, 160838.66, 0.0156
    elif bi <= 21487500:
        lim_inf, cfa_val, alic = 12892500.0, 328337.79, 0.0160
    elif bi <= 30082500:
        lim_inf, cfa_val, alic = 21487500.0, 649028.37, 0.0164
    elif bi <= 38677500:
        lim_inf, cfa_val, alic = 30082500.0, 838975.84, 0.0169
    elif bi <= 47272500:
        lim_inf, cfa_val, alic = 38677500.0, 1096761.73, 0.0170
    elif bi <= 154447750:
        lim_inf, cfa_val, alic = 47272500.0, 163308.75, 0.0171
    elif bi <= 1000000000:
        lim_inf, cfa_val, alic = 154447750.0, 4201777.78, 0.0173
    else:
        lim_inf, cfa_val, alic = 1000000000.0, 25380696.47, 0.0183

    excedente = max(0.0, bi - lim_inf)
    tasa_anual = round(((excedente * alic) + cfa_val), 2)
    tasa_mensual = round(tasa_anual / 12, 2)

    tasa_proteccion = round(tasa_mensual * 0.095, 2)
    tasa_salud = round(tasa_mensual * 0.105, 2)

    monto_bc = round(tasa_mensual * 0.10, 2) if var_bc == "SI" else 0.0
    monto_da = round(tasa_mensual * 0.10, 2) if var_da == "SI" else 0.0
    monto_be = round(tasa_mensual * 0.05, 2) if var_be == "SI" else 0.0

    tasa_total = round(
        (tasa_mensual + tasa_proteccion + tasa_salud)
        - monto_bc
        - monto_da
        - monto_be
        - edenor_val,
        2,
    )

    if var_tope == "NO" and tasa_total < 4500.0:
        tasa_total = 8900.0 if estado_sel == "BALDIO" else 4500.0

    def fmt(val):
        return f"${val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    st.markdown("### Resultados del Cálculo")

    # Coeficientes
    c_r1, c_r2, c_r3, c_r4, c_r5 = st.columns(5)
    c_r1.metric("BI", fmt(bi))
    c_r2.metric("CA", str(ca))
    c_r3.metric("CU", str(cu))
    c_r4.metric("CB", str(cb))
    c_r5.metric("CAP", str(cap))

    def fila_resultado(etiqueta, valor):
        st.markdown(
            f"""
            <div class="resultado-box">
                <span class="resultado-label">{etiqueta}</span>
                <span class="resultado-valor">{valor}</span>
            </div>
        """,
            unsafe_allow_html=True,
        )

    r1, r2 = st.columns(2)
    with r1:
        fila_resultado("Límite inferior:", fmt(lim_inf))
        fila_resultado("CFA:", fmt(cfa_val))
        fila_resultado("TSG Mensual:", fmt(tasa_mensual))
        fila_resultado("DA (Descuento):", f"-{fmt(monto_da)}")
        fila_resultado("Tasa de Protección:", fmt(tasa_proteccion))
    with r2:
        fila_resultado("Alícuota:", f"{alic * 100:.2f}%")
        fila_resultado("TSG Anual:", fmt(tasa_anual))
        fila_resultado("BC (Descuento):", f"-{fmt(monto_bc)}")
        fila_resultado("BE (Descuento):", f"-{fmt(monto_be)}")
        fila_resultado("Tasa de Salud:", fmt(tasa_salud))

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="background-color: #e0f2fe; padding: 12px; border-radius: 6px; border: 1px solid #1e3a8a; display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #1e3a8a; font-weight: bold; font-size: 14px;">TSG por Servicios Generales Total:</span>
            <span style="color: #1e3a8a; font-weight: bold; font-size: 16px;">{fmt(tasa_total)}</span>
        </div>
    """,
        unsafe_allow_html=True,
    )

except ValueError:
    st.error("Por favor, revise que los campos numéricos sean válidos.")