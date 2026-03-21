import streamlit as st

# --- КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="CS2 Pro Analytics", layout="wide")

# --- ИНИЦИАЛИЗАЦИЯ (v1.9.2) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'is_premium' not in st.session_state:
    st.session_state.is_premium = False
if 'free_premiums' not in st.session_state:
    st.session_state.free_premiums = 5 

# --- СТИЛИ (CSS) ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- ЭКРАН ВХОДА ---
if not st.session_state.logged_in:
    st.title("CS2 Pro Analytics")
    steam_url = st.text_input("Введите ссылку на профиль Steam:")
    
    if st.button("Войти"):
        if steam_url:
            st.session_state.logged_in = True
            st.session_state.profile_url = steam_url
            st.rerun()
        else:
            st.error("Введите ссылку!")

else:
    # --- САЙДБАР ---
    st.sidebar.title("Меню")
    menu = st.sidebar.radio("Разделы:", ["📊 Статистика", "🔫 Battle Pass", "🏆 ТОП Игроков"])

    # --- 1. СТАТИСТИКА ---
    if menu == "📊 Статистика":
        st.header("Статистика")
        st.write(f"Данные профиля: {st.session_state.profile_url}")
        
        st.divider()
        # ТВОЯ ЕДИНСТВЕННАЯ НОВАЯ КНОПКА
        if not st.session_state.is_premium:
            if st.session_state.free_premiums > 0:
                st.info(f"Акция: Осталось бесплатных Premium-статусов: {st.session_state.free_premiums}")
                if st.button("Забрать Premium 💎"):
                    st.session_state.is_premium = True
                    st.session_state.free_premiums -= 1
                    st.balloons()
                    st.rerun()
        else:
            st.success("Premium статус активен")

    # --- 2. BATTLE PASS ---
    elif menu == "🔫 Battle Pass":
        st.header("Battle Pass")
        # Здесь только твои оригинальные квесты и прогресс
        st.progress(0) 
        st.subheader("Квесты")
        st.info("🎯 Сделать киллы с Desert Eagle")
        st.info("💣 Установить пачку")

    # --- 3. ТОП ИГРОКОВ ---
    elif menu == "🏆 ТОП Игроков":
        st.header("ТОП Игроков")
        # Отображение только РЕАЛЬНОГО юзера
        status = "🌟" if st.session_state.is_premium else "👤"
        st.write(f"{status} {st.session_state.profile_url}")

    if st.sidebar.button("Выйти"):
        st.session_state.logged_in = False
        st.rerun()