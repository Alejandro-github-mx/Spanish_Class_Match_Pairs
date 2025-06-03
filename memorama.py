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

# Inicializar estado de sesión
if "game_initialized" not in st.session_state:
    cards = pairs * 2
    random.shuffle(cards)
    st.session_state.cards = cards
    st.session_state.flipped = [False] * len(cards)
    st.session_state.matched = [False] * len(cards)
    st.session_state.first_card = None
    st.session_state.second_card = None
    st.session_state.turn_start_time = None
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.session_state.game_initialized = True

cards = st.session_state.cards

# Lógica de voltear tarjeta
def flip_card(index):
    if st.session_state.flipped[index] or st.session_state.second_card is not None:
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
            st.session_state.turn_start_time = time.time()

# Resetear cartas si no coinciden
def auto_reset_if_needed():
    if st.session_state.first_card is not None and st.session_state.second_card is not None:
        elapsed = time.time() - st.session_state.turn_start_time
        if elapsed >= 3:
            first = st.session_state.first_card
            second = st.session_state.second_card
            st.session_state.flipped[first] = False
            st.session_state.flipped[second] = False
            st.session_state.first_card = None
            st.session_state.second_card = None
            st.session_state.turn_start_time = None
            st.rerun()

# Mostrar las tarjetas
def render_board():
    cols = st.columns(6)
    for i in range(len(cards)):
        col = cols[i % 6]
        if st.session_state.matched[i] or st.session_state.flipped[i]:
            col.button(cards[i], key=f"card_{i}", disabled=True)
        else:
            if col.button(f"{i + 1}", key=f"card_{i}"):
                flip_card(i)
                st.rerun()

# Verificar si se debe resetear turno por tiempo
if st.session_state.turn_start_time:
    auto_reset_if_needed()

# Verificar si el juego ha terminado
if all(st.session_state.matched):
    duration = int(time.time() - st.session_state.start_time)
    st.balloons()
    st.success("🎉 ¡Felicidades! Has emparejado todas las tarjetas.")
    st.info(f"🧼 Puntaje: {st.session_state.score} de {len(pairs)} pares")
    st.info(f"⏱ Tiempo total: {duration} segundos")
    if st.button("Jugar de nuevo"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
else:
    st.markdown(f"**Pares acertados:** {st.session_state.score} / {len(pairs)}")
    elapsed = int(time.time() - st.session_state.start_time)
    st.markdown(f"**Tiempo transcurrido:** {elapsed} segundos")
    render_board()
