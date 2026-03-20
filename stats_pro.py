import streamlit as st
import pandas as pd

# 1. Настройка страницы (Тёмная тема и заголовок)
st.set_page_config(page_title="CS2 Analytic Hub", page_icon="🎯", layout="wide")

# Кастомный CSS для стиля "Киберспорт"
st.markdown("""
    <style>
    .stApp { background-color: #0b0d10; color: #e0e0e0; }
    h1 { color: #ff4b4b; font-family: 'Arial Black'; }
    .stButton>button { background-color: #ff4b4b; color: white; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 2. Шапка сайта
st.title("🔥 CS2 PRO ANALYTICS")
st.write("Твой личный инструмент для анализа каток и улучшения скилла.")

# 3. Боковая панель
with st.sidebar:
    st.header("👤 Профиль игрока")
    name = st.text_input("Твой ник:", "Gamer_1")
    rank = st.slider("Твой уровень Faceit:", 1, 10, 5)
    st.divider()
    st.write(f"Привет, {name}! Твоя цель: Level {rank + 1}")

# 4. Основные показатели (Метрики)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Средний K/D", value="1.24", delta="0.05")
    st.info("💡 Твой K/D выше среднего. Ты хорошо отыгрываешь дуэли.")

with col2:
    st.metric(label="Headshot %", value="52.1%", delta="-2.0%")
    st.warning("⚠️ В последних матчах ты чаще стрелял в тело. Держи прицел выше!")

with col3:
    st.metric(label="Utility Usage", value="78%", delta="10%")
    st.success("✅ Отлично! Ты стал чаще использовать гранаты.")

st.divider()

# 5. Интерактивная карта и советы
st.header("🗺️ Разбор карты: Mirage")

tab_ct, tab_t = st.tabs(["🛡️ Защита (CT)", "⚔️ Атака (T)"])

with tab_ct:
    st.subheader("Позиция: Коннектор")
    st.write("- **Совет:** Всегда имей под рукой дым (Smoke), если враги жмут мид.")
    st.write("- **Тайминг:** Враги из ямы (T-spawn) добегают до мида за 6-7 секунд.")
    st.image("https://files.bo3.gg/uploads/image/575/image/original-34f3c7e7ba0e8d052d9a6064f242540b.webp", caption="Раскидка Smoke в окно")

with tab_t:
    st.subheader("Позиция: Тетрис / Яма")
    st.write("- **Совет:** Не выходи на А-плент без флешки через верх.")
    st.error("Помни: Снайпер в Тикете (Ticket) видит тебя первым!")

# 6. Маленькая таблица для вида
st.write("### Последние матчи")
match_data = {
    'Дата': ['20.03', '19.03', '19.03'],
    'Карта': ['Mirage', 'Inferno', 'Overpass'],
    'Результат': ['Победа', 'Поражение', 'Победа'],
    'K/D': [1.5, 0.8, 1.3]
}
st.table(pd.DataFrame(match_data))

st.write("---")
st.caption("🚀 Создано тобой. Рекламируй этот сайт в Discord и TikTok!")