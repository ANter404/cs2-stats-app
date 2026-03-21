import streamlit as st

# --- КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

# ТВОЙ ЛИЧНЫЙ ID ДЛЯ АДМИНКИ
YOUR_ADMIN_ID = 7876507389 

# --- ИНИЦИАЛИЗАЦИЯ ДАННЫХ (Храним в сессии) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = 0
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'is_premium' not in st.session_state:
    st.session_state.is_premium = False
if 'free_premiums' not in st.session_state:
    st.session_state.free_premiums = 5

# --- ЭКРАН ВХОДА ---
if not st.session_state.logged_in:
    st.title("📈 CS2 Pro Analytics")
    st.caption("v1.10.0 | Твой путь в киберспорт")
    
    with st.container():
        st.write("### Авторизация через Telegram ID")
        u_id = st.number_input("Введите ваш ID (из @userinfobot):", step=1, value=0)
        u_name = st.text_input("Ваш игровой никнейм:")
        
        if st.button("🚀 Войти в систему"):
            if u_name and u_id > 0:
                st.session_state.logged_in = True
                st.session_state.username = u_name
                st.session_state.user_id = u_id
                st.rerun()
            else:
                st.error("Ошибка: введите корректные данные!")

else:
    # --- БОКОВОЕ МЕНЮ ---
    st.sidebar.title(f"👤 {st.session_state.username}")
    
    # Меню навигации
    nav_links = ["📊 Статистика", "🔫 Battle Pass", "🏆 ТОП Игроков"]
    
    # ПРОВЕРКА ПРАВ АДМИНИСТРАТОРА
    is_admin = (st.session_state.user_id == YOUR_ADMIN_ID)
    if is_admin:
        nav_links.append("⚙️ АДМИН-ПАНЕЛЬ")
        st.sidebar.success("✅ Вы авторизованы как Admin")

    menu = st.sidebar.radio("Навигация:", nav_links)

    # --- РАЗДЕЛЫ ---
    if menu == "📊 Статистика":
        st.header("Аналитика игрока")
        
        # Блок Premium для TikTok
        if not st.session_state.is_premium:
            if st.session_state.free_premiums > 0:
                st.info(f"🎁 АКЦИЯ: Первым 5 людям PREMIUM бесплатно! (Осталось: {st.session_state.free_premiums})")
                if st.button("АКТИВИРОВАТЬ 💎"):
                    st.session_state.is_premium = True
                    st.session_state.free_premiums -= 1
                    st.success("Премиум активирован! Проверь свой статус в ТОПе.")
                    st.balloons()
                    st.rerun()
            else:
                st.error("К сожалению, бесплатные Premium-статусы закончились.")
        else:
            st.success("💎 ВАШ СТАТУС: PREMIUM ПОЛЬЗОВАТЕЛЬ")

        c1, c2, c3 = st.columns(3)
        c1.metric("K/D Ratio", "1.24", "+0.05")
        c2.metric("Win Rate", "54%", "📈")
        c3.metric("Уровень", "11 LVL")

    elif menu == "🔫 Battle Pass":
        st.header("Battle Pass: Season 1")
        st.write("Прогресс до 12 уровня:")
        st.progress(45)
        st.info("🎯 Квест дня: Сделать 10 киллов с Desert Eagle (4/10)")

    elif menu == "🏆 ТОП Игроков":
        st.header("Рейтинг CS2 Pro Analytics")
        # Список игроков
        leaderboard = [
            {"name": "s1mple", "score": 2500, "prem": True},
            {"name": "donk", "score": 2480, "prem": True},
            {"name": st.session_state.username, "score": 1100, "prem": st.session_state.is_premium},
            {"name": "User_442", "score": 850, "prem": False}
        ]
        
        for player in sorted(leaderboard, key=lambda x: x['score'], reverse=True):
            status_icon = "🌟" if player['prem'] else "👤"
            color = "gold" if player['prem'] else "white"
            st.markdown(f"{status_icon} **{player['name']}** — `{player['score']} pts`")

    elif menu == "⚙️ АДМИН-ПАНЕЛЬ" and is_admin:
        st.header("Управление проектом")
        st.write("Здесь ты можешь менять настройки в реальном времени.")
        
        new_val = st.slider("Изменить остаток Free Premium:", 0, 100, st.session_state.free_premiums)
        if st.button("Сохранить изменения"):
            st.session_state.free_premiums = new_val
            st.toast("Настройки обновлены!")

    # Кнопка выхода в самом низу сайдбара
    st.sidebar.divider()
    if st.sidebar.button("🚪 Выйти из профиля"):
        st.session_state.logged_in = False
        st.rerun()