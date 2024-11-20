# import streamlit as st
# from groq import Groq

# st.set_page_config(page_title="Mi chat de IA", page_icon="🐼")

# st.title("Mi primera aplicación con Streamlit")

# nombre = st.text_input("¿Cuál es tu nombre?")

# if st.button("Saludar"):
#     st.write(f"¡Hola, {nombre}! gracias por venir!!")

#Clase7
# import streamlit as st
# from groq import Groq

# st.set_page_config(page_title="Mi chat de IA", page_icon="6️⃣", layout="centered")

# MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

# def configurar_pagina():
#     st.title("Mi chat de IA")
#     st.sidebar.title("Configuración de la IA")
#     elegirModelo = st.sidebar.selectbox('Elegí un Modelo', options=MODELOS, index=0)
#     return elegirModelo

# def crear_usuario_groq():
#     clave_secreta = st.secrets["CLAVE_API"]
#     return Groq(api_key=clave_secreta)

# cliente = crear_usuario_groq()
# modelo = configurar_pagina()

# mensaje = st.chat_input("Escribí tu mensaje:")

# def configurar_modelo(cliente, modelo, mensaje):
#     return cliente.chat.completions.create(
#         model=modelo,
#         messages=[{"role": "user", "content": mensaje}]
#     )

# def inicializar_estado():
#     if "mensajes" not in st.session_state:
#         st.session_state.mensajes = []

# inicializar_estado()

# if mensaje:
#     respuesta = configurar_modelo(cliente, modelo, mensaje)
#     st.session_state.mensajes.append({"role": "user", "content": mensaje})
#     st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
#     st.write(st.session_state.mensajes)

#Clase9
import streamlit as st
from groq import Groq

st.set_page_config(page_title="Mi chat de IA", page_icon="6️⃣", layout="centered")

MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

def inicializar_estado():
    """Inicializa el estado de la sesión si no está definido."""
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def configurar_pagina():
    st.title("Mi chat de IA")
    st.sidebar.title("Configuración de la IA")
    elegirModelo = st.sidebar.selectbox('Elegí un Modelo', options=MODELOS, index=0)
    return elegirModelo

def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def configurar_modelo(cliente, modelo, mensaje):
    return cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": mensaje}],
        stream=True
    )

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container()
    with contenedorDelChat:
        mostrar_historial()

def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def main():
    # Inicializar el estado de la sesión
    inicializar_estado()

    # Configurar la página y los modelos
    modelo = configurar_pagina()
    cliente = crear_usuario_groq()

    # Manejar el área de entrada de chat
    mensaje = st.chat_input("Escribí tu mensaje:")
    area_chat()

    if mensaje:
        actualizar_historial("user", mensaje, "🧑‍💻")
        chat_completo = configurar_modelo(cliente, modelo, mensaje)

        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🤖")
        st.rerun()

if __name__ == "__main__":
    main()