import streamlit as st
import random
import time

st.set_page_config(page_title="Memorama - Día a Día", layout="wide")
st.title("🧠 Memorama de Español - Unidad 6: Día a Día")

# Lista de pares (texto idéntico en cada tarjeta)
pairs = [
    "Me despierto", "Desayuno", "A veces", "Miércoles", "La tarde",
    "Yo también", "Primero", "Cena", "Casi siempre", "Voy al trabajo",
    "Yo tampoco", "Luego", "Buenas noches", "De 6 a.m. a 12 p.m.", "Actividades diarias",
    "Yo no", "Siempre", "Después", "Ir", "Lunes","Once menos cuarto"
]

# Crear tablero mezclado
cards = pairs * 2
random.shuffle(cards)

# Inicializar el estado de sesión si es la primera vez
if "flipped" not in st.session_state:
    st.session_state.flipped = [False] * len(cards)
    st.session_state.matched = [False] * len(cards)
    st.session_state.first_card = None
    st.session_state.disable_input = False
    st.session_state.score = 0
    st.session_state.start_time = time.time()

# Mostrar las tarjetas
def render_board():
    cols = st.columns(6)  # 40 tarjetas -> 7 filas x 6 columnas aprox.
    for i, col in enumerate(cols * 7):
        if i >= len(cards):
            break
        if st.session_state.matched[i] or st.session_state.flipped[i]:
            col.button(cards[i], key=i, disabled=True)
        else:
            if col.button("❓", key=i):
                if not st.session_state.disable_input:
                    flip_card(i)

# Lógica de voltear tarjeta
def flip_card(index):
    if st.session_state.flipped[index]:
        return

    st.session_state.flipped[index] = True

    if st.session_state.first_card is None:
        st.session_state.first_card = index
    else:
        second_card = index
        first_index = st.session_state.first_card
        if cards[first_index] == cards[second_card]:
            st.session_state.matched[first_index] = True
            st.session_state.matched[second_card] = True
            st.session_state.score += 1
            st.session_state.first_card = None
        else:
            st.session_state.disable_input = True
            st.experimental_rerun()

# Reiniciar después de mostrar dos cartas equivocadas
if st.session_state.disable_input:
    st.warning("❌ No coinciden. Intenta de nuevo.")
    st.button("Continuar", on_click=lambda: reset_turn())

# Función para resetear el turno si no hay match
def reset_turn():
    for i in range(len(cards)):
        if not st.session_state.matched[i]:
            st.session_state.flipped[i] = False
    st.session_state.first_card = None
    st.session_state.disable_input = False
    st.experimental_rerun()

# Verificar si el juego ha terminado
if all(st.session_state.matched):
    duration = int(time.time() - st.session_state.start_time)
    st.balloons()
    st.success("🎉 ¡Felicidades! Has emparejado todas las tarjetas.")
    st.info(f"🧮 Puntaje: {st.session_state.score} de {len(pairs)} pares")
    st.info(f"⏱ Tiempo total: {duration} segundos")
    if st.button("Jugar de nuevo"):
        st.session_state.clear()
        st.experimental_rerun()
else:
    st.markdown(f"**Pares acertados:** {st.session_state.score} / {len(pairs)}")
    elapsed = int(time.time() - st.session_state.start_time)
    st.markdown(f"**Tiempo transcurrido:** {elapsed} segundos")
    render_board()
