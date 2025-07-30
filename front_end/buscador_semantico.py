import streamlit as st
import requests

API_URL = "http://localhost:8000/search"

st.title("🔎 Buscador Semántico de Propuestas Políticas")

query = st.text_input("Escribe tu consulta política o temática", "")

if query:
    with st.spinner("Consultando propuestas..."):
        try:
            response = requests.get(API_URL, params={"q": query})
            response.raise_for_status()  # lanza error si status != 200
            resultados = response.json()

            st.subheader("🔍 Resultados similares:")

            for resultado in resultados:
                st.markdown(f"### 🏛️ {resultado['titulo']}")
                st.markdown(f"**Partido político:** {resultado['partido']}")
                st.markdown(f"**Similitud:** {round(resultado['similitud'], 2)}")
                st.markdown(resultado["texto"])
                st.markdown("---")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Error al conectar con la API: {e}")
