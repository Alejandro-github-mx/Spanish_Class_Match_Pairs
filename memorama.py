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
    "Yo no", "Siempre", "Después", "Ir", "Lunes", "Once menos cuarto"
]

# Crear tablero mezclado
cards = pairs * 2
random.shuffle(cards)

# Inicializar el estado de sesión si es la primera vez
if "flipped" not in st.session_state:
    st.session_state.flipped = [False] * len(cards)
    st.session_state.matched = [False] * len(cards)
    st.session_state.first_card = None
    st.session_state.second_card = None
    st.session_state.waiting = False
    st.session_state.score = 0
    st.session_state.start_time = time.time()

# Función para resetear el turno si no hay match
def reset_turn():
    first = st.session_state.first_card
    second = st.session_state.second_card
    if first is not None and second is not None:
        if not st.session_state.matched[first]:
            st.session_state.flipped[first] = False
        if not st.session_state.matched[second]:
            st.session_state.flipped[second] = False
    st.session_state.first_card = None
    st.session_state.second_card = None
    st.session_state.waiting = False

# Lógica de voltear tarjeta
def flip_card(index):
    if st.session_state.flipped[index] or st.session_state.waiting:
        return

    st.session_state.flipped[index] = True

    if st.session_state.first_card is None:
        st.session_state.first_card = index
    elif st.session_state.second_card is None:
        st.session_state.second_card = index
        first = st.session_state.first_card
        second = st.session_state.second_card
        if cards[first] == cards[second]:
            st.session_state.matched[first] = True
            st.session_state.matched[second] = True
            st.session_state.score += 1
            st.session_state.first_card = None
            st.session_state.second_card = None
        else:
            st.session_state.waiting = True

# Mostrar las tarjetas
def render_board():
    cols = st.columns(6)
    for i in range(len(cards)):
        col = cols[i % 6]
        if st.session_state.matched[i] or st.session_state.flipped[i]:
            col.button(cards[i], key=i, disabled=True)
        else:
            if col.button("❓", key=i):
                flip_card(i)

# Verificar si se debe resetear el turno
if st.session_state.waiting:
    st.warning("❌ No coinciden. Intenta de nuevo.")
    if st.button("Continuar"):
        reset_turn()

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
