import streamlit as st
import pandas as pd
import time

# Настройка страницы
st.set_page_config(page_title="ANTer404 CS2 Pro Hub", page_icon="📈", layout="wide")

# Проверка авторизации
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# --- ЭКРАН ВХОДА ---
if not st.session_state["logged_in"]:
    st.title("🛡️ CS2 Analytics Dashboard v3.1")
    st.info("Выбери свой путь, боец!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌐 Обычный Игрок (Steam/MM)")
        name = st.text_input("Как тебя зовут?")
        nick = st.text_input("Ник в игре (Steam)")
        if st.button("Войти в кабинет", use_container_width=True):
            if nick:
                st.session_state["logged_in"] = True
                st.session_state["user"] = nick
                st.session_state["method"] = "Steam/Manual"
                st.rerun()
            else:
                st.error("Без ника не пущу!")

    with col2:
        st.subheader("🏆 Профи (Faceit)")
        f_nick = st.text_input("Твой Faceit ID")
        if st.button("Подключить Faceit", use_container_width=True):
            if f_nick:
                st.session_state["logged_in"] = True
                st.session_state["user"] = f_nick
                st.session_state["method"] = "Faceit"
                st.rerun()
            else:
                st.warning("Введи ник для синхронизации!")

# --- ОСНОВНОЙ КОНТЕНТ (ПОСЛЕ ВХОДА) ---
else:
    # Боковая панель
    st.sidebar.title(f"👤 {st.session_state['user']}")
    st.sidebar.write(f"Тип аккаунта: **{st.session_state['method']}**")
    
    page = st.sidebar.radio("Разделы:", ["📊 Моя Стата", "🧮 Калькулятор матча", "🗺️ Гайды по картам", "⚙️ Настройки"])
    
    if st.sidebar.button("Выйти"):
        st.session_state["logged_in"] = False
        st.rerun()

    if page == "📊 Моя Стата":
        st.title(f"Аналитика для {st.session_state['user']}")
        
        # Метрики
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("K/D Ratio", "1.24", "+0.05")
        c2.metric("Winrate", "54%", "2%")
        c3.metric("HS %", "45%", "-1%")
        c4.metric("Матчей", "142")
        
        st.divider()
        st.subheader("📈 Прогресс за неделю")
        # Фейковый график для красоты
        chart_data = pd.DataFrame([1.1, 1.2, 1.05, 1.3, 1.24], columns=['K/D'])
        st.line_chart(chart_data)

    elif page == "🧮 Калькулятор матча":
        st.header("Ввод данных последней игры")
        
        with st.form("match_form"):
            col_a, col_b, col_c = st.columns(3)
            map_name = col_a.selectbox("Карта", ["Mirage", "Inferno", "Dust 2", "Anubis", "Ancient", "Nuke", "Vertigo"])
            kills = col_b.number_input("Киллы", 0, 100, 20)
            deaths = col_c.number_input("Смерти", 1, 100, 15)
            
            submit = st.form_submit_button("Сохранить и рассчитать")
            
            if submit:
                kd = round(kills/deaths, 2)
                st.write(f"### Твой K/D на {map_name}: **{kd}**")
                if kd >= 1.2:
                    st.success("Жестко! Ты реально тащил.")
                    st.balloons()
                elif kd >= 1.0:
                    st.info("Нормально, в плюсе.")
                else:
                    st.error("Надо потренить аим, бро.")

    elif page == "🗺️ Гайды по картам":
        st.header("Библиотека раскидок")
        selected_map = st.selectbox("Выбери карту:", ["Mirage", "Inferno", "Nuke"])
        
        if selected_map == "Mirage":
            st.subheader("Смок в окно (с респы)")
            st.video("https://www.youtube.com/watch?v=XpG8S774Isc")
            st.write("1. Упрись в угол. 2. Целься в антенну. 3. Прыжок + Бросок.")

    elif page == "⚙️ Настройки":
        st.header("Настройки профиля")
        st.text_input("Сменить ник", value=st.session_state['user'])
        st.color_picker("Цвет интерфейса", "#00FFAA")
        st.button("Сохранить изменения")