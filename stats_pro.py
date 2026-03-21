import streamlit as st

# --- КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="CS2 Pro Analytics", layout="wide")

# ТВОЙ ID
YOUR_ADMIN_ID = 7876507389 

# --- ИНИЦИАЛИЗАЦИЯ v1.9.2 ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = 0
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'profile_url' not in st.session_state:
    st.session_state.profile_url = ""
if 'is_premium' not in st.session_state:
    st.session_state.is_premium = False
if 'free_premiums' not in st.session_state:
    st.session_state.free_premiums = 5

# --- ОКНО ВХОДА / РЕГИСТРАЦИИ ---
if not st.session_state.logged_in:
    st.title("📈 CS2 Pro Analytics v1.9.2")
    
    u_id = st.number_input("Telegram ID:", step=1, value=0)
    u_name = st.text_input("Никнейм:")
    u_url = st.text_input("Ссылка на профиль:")
    
    if st.button("Войти"):
        if u_name and u_id > 0 and u_url:
            st.session_state.logged_in = True
            st.session_state.username = u_name
            st.session_state.user_id = u_id
            st.session_state.profile_url = u_url
            st.rerun()
        else:
            st.error("Заполни все поля!")

else:
    # --- САЙДБАР ---
    st.sidebar.header(f"Юзер: {st.session_state.username}")
    
    menu = ["Статистика", "Battle Pass", "ТОП"]
    if st.session_state.user_id == YOUR_ADMIN_ID:
        menu.append("АДМИНКА")
    
    choice = st.sidebar.radio("Меню", menu)

    # --- РАЗДЕЛЫ ---
    if choice == "Статистика":
        st.subheader("Твои показатели")
        st.write(f"Профиль: {st.session_state.profile_url}")
        
        # Тот самый блок для ТикТока
        st.divider()
        if not st.session_state.is_premium:
            st.info(f"Свободно Premium-мест: {st.session_state.free_premiums}")
            if st.button("Забрать Premium 💎"):
                if st.session_state.free_premiums > 0:
                    st.session_state.is_premium = True
                    st.session_state.free_premiums -= 1
                    st.balloons()
                    st.rerun()
        else:
            st.success("У тебя есть Premium!")

    elif choice == "Battle Pass":
        st.subheader("Прогресс BP")
        st.progress(45)
        st.write("Уровень: 11")

    elif choice == "ТОП":
        st.subheader("Лидеры")
        # Показываем тебя со звездой, если есть преимум
        status = "🌟" if st.session_state.is_premium else "👤"
        st.write(f"{status} {st.session_state.username} — 1100 pts")
        st.write("👤 s1mple — 2500 pts")

    elif choice == "АДМИНКА":
        st.subheader("Панель управления")
        new_count = st.number_input("Изменить кол-во премов:", value=st.session_state.free_premiums)
        if st.button("Обновить"):
            st.session_state.free_premiums = int(new_count)
            st.success("Готово!")

    if st.sidebar.button("Выход"):
        st.session_state.logged_in = False
        st.rerun()