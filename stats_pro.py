import streamlit as st
import requests

# 1. Настройки страницы
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

# 2. Конфигурация (Твои данные)
STEAM_API_KEY = "80562D785863D2DB396C004F7547514D" 
TELEGRAM_LINK = "https://t.me/CS2devLog"
DONATE_LINK = "https://www.donationalerts.com/r/anter404"

# 3. Боковая панель
with st.sidebar:
    st.title("ANTer404 | Project")
    st.write(f"**Версия:** 1.1.1")
    st.markdown(f"[📢 Наш Telegram]({TELEGRAM_LINK})")
    st.markdown(f"[💰 Поддержать проект]({DONATE_LINK})")
    st.divider()
    st.caption("© 2026 ANTer404 Development")

# 4. Основной экран
st.title("📈 CS2 Pro Analytics")

steam_input = st.text_input("Введите Steam ID 64:", placeholder="7656119...")

if steam_input:
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_input}"
    try:
        res = requests.get(url).json()
        if res['response']['players']:
            player = res['response']['players'][0]
            col1, col2 = st.columns([1, 4])
            with col1:
                st.image(player['avatarfull'], width=150)
            with col2:
                st.header(player['personaname'])
                st.write(f"🔗 [Профиль Steam]({player['profileurl']})")
            
            st.divider()
            st.subheader("📦 Инвентарь CS2")
            st.info("Модуль в разработке. Скоро здесь будут ваши скины!")
        else:
            st.error("Пользователь не найден.")
    except Exception as e:
        st.error(f"Ошибка связи со Steam: {e}")