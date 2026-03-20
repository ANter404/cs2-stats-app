import streamlit as st
import pandas as pd

st.set_page_config(page_title="ANTer404 Personal Stats", page_icon="📈")

# Создаем список для хранения истории матчей, если его нет
if "match_history" not in st.session_state:
    st.session_state["match_history"] = []

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.title("🛡️ CS2 Personal Tracker v3.2")
    nick = st.text_input("Введи свой ник для входа")
    if st.button("Войти в систему"):
        if nick:
            st.session_state["logged_in"] = True
            st.session_state["user"] = nick
            st.rerun()
else:
    st.sidebar.title(f"👤 {st.session_state['user']}")
    menu = st.sidebar.radio("Меню", ["📊 Мой Прогресс", "📝 Записать матч"])
    
    if st.sidebar.button("Выход"):
        st.session_state["logged_in"] = False
        st.rerun()

    if menu == "📊 Мой Прогресс":
        st.header(f"Аналитика игрока {st.session_state['user']}")
        
        if not st.session_state["match_history"]:
            st.warning("История пуста. Запиши свой первый матч в меню слева!")
        else:
            df = pd.DataFrame(st.session_state["match_history"])
            
            # Считаем средний K/D
            avg_kd = round(df["K/D"].mean(), 2)
            st.metric("Твой средний K/D", avg_kd, delta=None)
            
            # График прогресса
            st.subheader("График K/D по матчам")
            st.line_chart(df["K/D"])
            
            # Таблица матчей
            st.subheader("Последние игры")
            st.table(df)

    elif menu == "📝 Записать матч":
        st.header("Ввод данных после катки")
        with st.form("add_match"):
            m_map = st.selectbox("Карта", ["Mirage", "Dust 2", "Inferno", "Anubis", "Ancient"])
            k = st.number_input("Киллы", 0, 100, 20)
            d = st.number_input("Смерти", 1, 100, 15)
            win = st.checkbox("Победа?")
            
            if st.form_submit_button("Сохранить игру"):
                kd = round(k/d, 2)
                new_match = {"Карта": m_map, "K/D": kd, "Результат": "Win" if win else "Loss"}
                st.session_state["match_history"].append(new_match)
                st.success(f"Матч на {m_map} сохранен! K/D: {kd}")