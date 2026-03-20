import streamlit as st
import pandas as pd
import requests # Это нам понадобится для связи с Faceit/Steam

st.set_page_config(page_title="CS2 Real Analytics", layout="wide")

# --- ФУНКЦИЯ ПОЛУЧЕНИЯ РЕАЛЬНОЙ СТАТИСТИКИ ---
def get_faceit_stats(nickname):
    # Пока это заглушка, но сюда мы вставим реальный запрос к Faceit API
    # Если ник 'ANTer404', имитируем загрузку данных
    if nickname:
        return {"kd": "1.35", "winrate": "58%", "matches": "1,240"}
    return None

# --- ГЛАВНЫЙ ИНТЕРФЕЙС ---
if "logged_in" not in st.session_state:
    st.title("🛡️ Вход в систему")
    with st.form("reg"):
        user = st.text_input("Твой ник в Faceit")
        st.form_submit_button("Начать анализ")
        if user:
            st.session_state["logged_in"] = True
            st.session_state["nickname"] = user
            st.rerun()
else:
    st.sidebar.title(f"👤 {st.session_state['nickname']}")
    if st.sidebar.button("Выйти"):
        del st.session_state["logged_in"]
        st.rerun()

    st.title(f"📊 Аналитика для {st.session_state['nickname']}")
    
    # Пытаемся получить реальные данные
    data = get_faceit_stats(st.session_state['nickname'])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Актуальный K/D", data["kd"])
    col2.metric("Винрейт", data["winrate"])
    col3.metric("Всего матчей", data["matches"])

    st.divider()
    
    # Секция для вставки ссылки на демо или профиль
    st.header("🔗 Добавить матч для разбора")
    demo_url = st.text_input("Вставь ссылку на Faceit Match или Steam Demo:")
    if st.button("Проанализировать демо"):
        if "faceit.com" in demo_url:
            st.success("Матч найден! Идет расшифровка логов...")
            st.progress(40) # Просто для вида, пока не подключим парсер
        else:
            st.error("Пока поддерживаются только ссылки с Faceit.")