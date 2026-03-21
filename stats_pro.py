import streamlit as st
import pandas as pd

# --- КОНФИГУРАЦИЯ v1.9.0 ---
st.set_page_config(page_title="ANTer404 | Project", layout="wide")

# --- ИНИЦИАЛИЗАЦИЯ (v1.9.2) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'is_premium' not in st.session_state:
    st.session_state.is_premium = False
if 'free_premiums' not in st.session_state:
    st.session_state.free_premiums = 5

# --- ЭКРАН ВХОДА (ОРИГИНАЛ) ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>CS2 Pro Analytics</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        steam_url = st.text_input("Ссылка на профиль:")
        if st.button("Войти"):
            if steam_url:
                st.session_state.logged_in = True
                st.session_state.profile_url = steam_url
                st.rerun()
else:
    # --- САЙДБАР (ПО СКРИНШОТАМ) ---
    with st.sidebar:
        st.title("ANTer404 | Project")
        st.write("👤 Уникальных профилей: 2")
        if st.button("Выйти"):
            st.session_state.logged_in = False
            st.rerun()
        
        st.divider()
        st.markdown("🚀 [Telegram](#)")
        st.markdown("🎁 [Трейд](#)")
        st.markdown("💰 [Донат](#)")
        st.divider()
        st.checkbox("Техподдержка")
        st.caption("v1.9.0 | Tabs & Pass Update")

    # --- ОСНОВНОЙ КОНТЕНТ ---
    st.title("👋 Привет, ANTer404")
    
    # Табы как на скринах
    tabs = st.tabs(["📊 Статистика", "🎯 Battle Pass", "📦 Инвентарь", "🏆 Топ"])

    # 1. СТАТИСТИКА
    with tabs[0]:
        col_ava, col_main = st.columns([1, 4])
        with col_ava:
            st.image("https://via.placeholder.com/150") # Твой Rick аватара
        with col_main:
            st.subheader("🏅 Уровень: 7")
            st.progress(0.85) # Синяя полоска
            st.caption("XP: 5615 | До следующего: 839 XP")
            st.write("⌚ **Часов в игре:** 19.8")

        st.divider()
        st.subheader("🔫 Мастерство оружия")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("AK-47", "61")
        m2.metric("AWP", "63")
        m3.metric("M4A1", "86")
        m4.metric("Knife", "0")
        
        st.divider()
        k1, k2, k3 = st.columns(3)
        k1.metric("K/D", "0.64")
        k2.metric("HS Count", "161")
        k3.metric("Wins", "110")

        # ТВОЯ ЕДИНСТВЕННАЯ ДОБАВЛЕННАЯ ФУНКЦИЯ
        st.divider()
        if not st.session_state.is_premium:
            if st.session_state.free_premiums > 0:
                st.info(f"Акция: Осталось бесплатных Premium-статусов: {st.session_state.free_premiums}")
                if st.button("Забрать Premium 💎"):
                    st.session_state.is_premium = True
                    st.session_state.free_premiums -= 1
                    st.balloons()
                    st.rerun()

    # 2. BATTLE PASS (КВЕСТЫ С ПРОГРЕСС-БАРАМИ)
    with tabs[1]:
        st.header("🎯 Сезонные квесты")
        
        st.write("**Мастер стрельбы:** Набей 1000 киллов")
        st.progress(0.64); st.caption("Прогресс: 640 / 1000")
        
        st.write("**Снайпер:** Поставь 500 хэдшотов")
        st.progress(0.32); st.caption("Прогресс: 161 / 500")
        
        st.write("**Головорез:** 50 фрагов с ножа")
        st.progress(0.0); st.caption("Прогресс: 0 / 50")
        
        st.write("**Победитель:** Выиграй 100 раундов")
        st.progress(1.0); st.caption("Прогресс: 110 / 110")

    # 3. ИНВЕНТАРЬ
    with tabs[2]:
        st.header("📦 Твой инвентарь")
        st.markdown("🔴 **Наклейка | Into The Breach | Париж-2023**")
        st.write("💰 $0.03")

    # 4. ТОП (ТАБЛИЦА)
    with tabs[3]:
        st.header("🏆 Глобальный Топ")
        # Создаем таблицу как на скрине
        df = pd.DataFrame({
            "Игрок": ["ANTer404", "ANTer404"],
            "Уровень": [7, 3],
            "XP": [5615, 1395]
        })
        st.table(df)