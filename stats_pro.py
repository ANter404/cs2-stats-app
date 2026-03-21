import streamlit as st

# --- КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

# ТВОЙ ЛИЧНЫЙ ID (7876507389)
YOUR_ADMIN_ID = 7876507389 

# --- ИНИЦИАЛИЗАЦИЯ (v1.9.2) ---
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

# --- ФОРМА РЕГИСТРАЦИИ / ВХОДА ---
if not st.session_state.logged_in:
    st.title("📈 CS2 Pro Analytics")
    st.caption("Версия 1.9.2 | Система профессиональной аналитики")
    
    with st.form("registration_form"):
        st.subheader("📝 Регистрация профиля")
        u_id = st.number_input("Введите ваш Telegram ID:", step=1, value=0)
        u_name = st.text_input("Ваш игровой никнейм:")
        u_url = st.text_input("Ссылка на профиль (Steam/Faceit):", placeholder="https://steamcommunity.com/id/...")
        
        submit = st.form_submit_button("Создать аккаунт")
        
        if submit:
            if u_name and u_id > 0 and u_url:
                st.session_state.logged_in = True
                st.session_state.username = u_name
                st.session_state.user_id = u_id
                st.session_state.profile_url = u_url
                st.rerun()
            else:
                st.error("Ошибка: заполни все поля формы!")

else:
    # --- БОКОВОЕ МЕНЮ ---
    st.sidebar.title(f"👤 {st.session_state.username}")
    
    # Список разделов
    nav_links = ["📊 Статистика", "🔫 Battle Pass", "🏆 ТОП Игроков"]
    
    # ПРОВЕРКА НА АДМИНА
    is_admin = (st.session_state.user_id == YOUR_ADMIN_ID)
    if is_admin:
        nav_links.append("⚙️ АДМИН-ПАНЕЛЬ")
        st.sidebar.warning("⚡ ДОСТУП РАЗРАБОТЧИКА")

    menu = st.sidebar.radio("Навигация:", nav_links)

    # --- РАЗДЕЛЫ ---
    if menu == "📊 Статистика":
        st.header(f"Аналитика профиля: {st.session_state.username}")
        st.write(f"🔗 **Профиль:** {st.session_state.profile_url}")
        
        # Блок Premium для TikTok
        st.divider()
        if not st.session_state.is_premium:
            if st.session_state.free_premiums > 0:
                st.info(f"🎁 АКЦИЯ: Первым 5 людям PREMIUM бесплатно! (Осталось: {st.session_state.free_premiums})")
                if st.button("АКТИВИРОВАТЬ PREMIUM 💎"):
                    st.session_state.is_premium = True
                    st.session_state.free_premiums -= 1
                    st.success("Премиум активирован! Проверь свой статус в ТОП-листе.")
                    st.balloons()
                    st.rerun()
            else:
                st.error("Бесплатные места закончились!")
        else:
            st.success("💎 СТАТУС: PREMIUM АКТИВИРОВАН")

        c1, c2, c3 = st.columns(3)
        c1.metric("K/D Ratio", "1.24")
        c2.metric("Сыграно матчей", "142")
        c3.metric("Уровень", "11 LVL")

    elif menu == "🔫 Battle Pass":
        st.header("Battle Pass: Season 1")
        st.write("Прогресс текущего уровня:")
        st.progress(45)
        st.info("🎯 Квест: Сделать 10 киллов с Desert Eagle (4/10)")

    elif menu == "🏆 ТОП Игроков":
        st.header("Мировой рейтинг")
        leaderboard = [
            {"name": "s1mple", "score": 2500, "prem": True},
            {"name": "donk", "score": 2480, "prem": True},
            {"name": st.session_state.username, "score": 1100, "prem": st.session_state.is_premium}
        ]
        
        for p in sorted(leaderboard, key=lambda x: x['score'], reverse=True):
            status_icon = "🌟" if p['prem'] else "👤"
            st.write(f"{status_icon} **{p['name']}** — `{p['score']} pts`")

    elif menu == "⚙️ АДМИН-ПАНЕЛЬ" and is_admin:
        st.header("Панель управления (Только для тебя)")
        new_val = st.number_input("Изменить количество фри-премиумов:", value=st.session_state.free_premiums)
        if st.button("Сохранить"):
            st.session_state.free_premiums = int(new_val)
            st.toast("Данные обновлены!")

    st.sidebar.divider()
    if st.sidebar.button("🚪 Выйти"):
        st.session_state.logged_in = False
        st.rerun()