import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter

# Configuración de la página
st.set_page_config(page_title="Random Stats", page_icon="🎲")

st.title("🎲 Analizador de Números Aleatorios")
st.markdown("Genera una secuencia de números y analiza su distribución por valor completo o por dígitos individuales.")

# --- Barra Lateral (Configuración) ---
st.sidebar.header("Ajustes del Experimento")

cantidad = st.sidebar.slider("¿Cuántos números generar?", min_value=10, max_value=5000, value=500)
rango_min = st.sidebar.number_input("Valor mínimo", value=0)
rango_max = st.sidebar.number_input("Valor máximo", value=100)

modo = st.sidebar.radio(
    "Visualizar frecuencia por:",
    ("Número Completo", "Dígitos Individuales (0-9)")
)

# --- Lógica de Generación ---
# Usamos un estado de sesión para que los números no cambien cada vez que tocas un botón lateral
if 'data' not in st.session_state or st.sidebar.button("🔄 Regenerar Números"):
    st.session_state.data = np.random.randint(rango_min, rango_max + 1, size=cantidad)

numeros = st.session_state.data

# --- Procesamiento de Datos ---
if modo == "Número Completo":
    st.subheader(f"Frecuencia de Números (Rango {rango_min} - {rango_max})")
    # Contamos ocurrencias y ordenamos por el índice (el número)
    conteo = pd.Series(numeros).value_counts().sort_index()
    st.bar_chart(conteo)

else:
    st.subheader("Frecuencia por Dígito Individual")
    # Convertimos todos los números a string, los juntamos y contamos cada caracter
    cadena_total = "".join(map(str, numeros))
    # Solo nos interesan los dígitos (ignoramos signos negativos si los hay)
    solo_digitos = [d for d in cadena_total if d.isdigit()]
    
    conteo_dict = Counter(solo_digitos)
    # Aseguramos que todos los dígitos del 0 al 9 aparezcan en la gráfica
    df_digitos = pd.DataFrame(
        [conteo_dict.get(str(i), 0) for i in range(10)],
        index=[str(i) for i in range(10)],
        columns=["Frecuencia"]
    )
    st.bar_chart(df_digitos)

# --- Resumen de Datos ---
with st.expander("Ver datos crudos"):
    st.write(numeros)

st.info(f"Se han analizado **{cantidad}** números generados aleatoriamente.")
