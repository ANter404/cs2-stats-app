import streamlit as st

# --- КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="CS2 Pro Analytics")

# ТВОЙ ID ДЛЯ АДМИНКИ
YOUR_ADMIN_ID = 7876507389 

# --- БАЗОВЫЕ ДАННЫЕ v1.9.2 ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'is_premium' not in st.session_state:
    st.session_state.is_premium = False
if 'free_premiums' not in st.session_state:
    st.session_state.free_premiums = 5

# --- ВХОД (ТОЛЬКО ТО, ЧТО ТЫ ПРОСИЛ) ---
if not st.session_state.logged_in:
    st.title("CS2 Pro Analytics")
    
    # Твои новые поля для регистрации
    id_input = st.number_input("Telegram ID:", step=1, value=0)
    name_input = st.text_input("Никнейм:")
    url_input = st.text_input("Ссылка на профиль:")
    
    if st.button("Войти"):
        if name_input and id_input > 0 and url_input:
            st.session_state.logged_in = True
            st.session_state.username = name_input
            st.session_state.user_id = id_input
            st.session_state.profile_url = url_input
            st.rerun()
        else:
            st.error("Заполни все поля!")

else:
    # --- ТВОЙ ПРИВЫЧНЫЙ САЙДБАР ---
    st.sidebar.write(f"Привет, {st.session_state.username}")
    
    # Проверка на админа (только для твоего ID)
    menu = ["Статистика", "Battle Pass", "ТОП"]
    if st.session_state.user_id == YOUR_ADMIN_ID:
        menu.append("АДМИНКА")
    
    choice = st.sidebar.radio("Меню", menu)

    # --- ТВОИ РАЗДЕЛЫ (БЕЗ МОЕГО МУСОРА) ---
    if choice == "Статистика":
        st.header("Статистика")
        st.write(f"Ссылка: {st.session_state.profile_url}")
        
        st.divider()
        # Блок с премиумом для ролика
        if not st.session_state.is_premium:
            st.write(f"Осталось фри-премиумов: {st.session_state.free_premiums}")
            if st.button("Забрать Premium 💎"):
                if st.session_state.free_premiums > 0:
                    st.session_state.is_premium = True
                    st.session_state.free_premiums -= 1
                    st.balloons()
                    st.rerun()
        else:
            st.success("Premium активен")

    elif choice == "Battle Pass":
        st.header("Battle Pass")
        st.write("Уровень: 11")
        st.progress(45)

    elif choice == "ТОП":
        st.header("ТОП Игроков")
        # Твой ник со звездой если купил преимум
        if st.session_state.is_premium:
            st.write(f"🌟 {st.session_state.username} — 1100 pts")
        else:
            st.write(f"👤 {st.session_state.username} — 1100 pts")
        st.write("👤 s1mple — 2500 pts")
        st.write("👤 donk — 2400 pts")

    elif choice == "АДМИНКА":
        st.header("Админка")
        new_count = st.number_input("Кол-во премиумов:", value=st.session_state.free_premiums)
        if st.button("Сохранить"):
            st.session_state.free_premiums = int(new_count)
            st.success("Обновлено")

    if st.sidebar.button("Выход"):
        st.session_state.logged_in = False
        st.rerun()