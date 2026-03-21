import streamlit as st

# --- КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="CS2 Pro Analytics")

# --- ЛОГИКА ПРЕМИУМА (v1.9.2) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'is_premium' not in st.session_state:
    st.session_state.is_premium = False
if 'free_premiums' not in st.session_state:
    st.session_state.free_premiums = 5  # Счетчик для первых пяти

# --- ОКНО ВХОДА ---
if not st.session_state.logged_in:
    st.title("CS2 Pro Analytics")
    
    steam_url = st.text_input("Ссылка на профиль Steam:")
    
    if st.button("Войти"):
        if steam_url:
            st.session_state.logged_in = True
            st.session_state.profile_url = steam_url
            st.rerun()
        else:
            st.error("Введите ссылку!")

else:
    # --- ОСНОВНОЙ ИНТЕРФЕЙС ---
    st.sidebar.title("Меню")
    menu = st.sidebar.radio("Разделы:", ["Статистика", "ТОП Игроков"])

    if menu == "Статистика":
        st.header("Статистика")
        st.write(f"Профиль: {st.session_state.profile_url}")
        
        st.divider()
        # ТА САМАЯ ФУНКЦИЯ ДЛЯ 5 ЧЕЛОВЕК
        if not st.session_state.is_premium:
            if st.session_state.free_premiums > 0:
                st.info(f"Акция: Осталось бесплатных Premium-статусов: {st.session_state.free_premiums}")
                if st.button("Забрать Premium 💎"):
                    st.session_state.is_premium = True
                    st.session_state.free_premiums -= 1
                    st.balloons() # Эффект праздника
                    st.rerun()
            else:
                st.warning("Бесплатные премиумы закончились")
        else:
            st.success("У вас активирован Premium статус")

    elif menu == "ТОП Игроков":
        st.header("ТОП Игроков")
        # Отображение ника со звездой если есть премиум
        status = "🌟" if st.session_state.is_premium else "👤"
        st.write(f"{status} {st.session_state.profile_url}")

    if st.sidebar.button("Выйти"):
        st.session_state.logged_in = False
        st.rerun()