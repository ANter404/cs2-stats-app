import streamlit as st
import requests
import re

# Настройки
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

STEAM_API_KEY = "80562D785863D2DB396C004F7547514D" 
TELEGRAM_LINK = "https://t.me/CS2devLog"
DONATE_LINK = "https://www.donationalerts.com/r/anter404"

# Боковая панель
with st.sidebar:
    st.title("ANTer404 | Project")
    st.markdown(f"[📢 Наш Telegram]({TELEGRAM_LINK})")
    st.markdown(f"[💰 Поддержать проект]({DONATE_LINK})")
    st.divider()
    st.caption("v1.1.4 | С пылу с жару")

st.title("📈 CS2 Pro Analytics")

# Поле ввода
user_input = st.text_input("Вставь ссылку на профиль:", 
                          value="https://steamcommunity.com/profiles/76561198749701067/")

if user_input:
    # Ищем 17 цифр в любом месте ссылки
    found_ids = re.findall(r'\d{17}', user_input)
    
    if found_ids:
        steam_id = found_ids[0]
        
        # Получаем данные профиля
        url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
        
        try:
            response = requests.get(url)
            data = response.json()
            players = data.get('response', {}).get('players', [])
            
            if players:
                player = players[0]
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.image(player['avatarfull'], width=150)
                with col2:
                    st.header(player['personaname'])
                    st.write(f"🆔 Твой ID: `{steam_id}`")
                    st.write(f"🌐 [Ссылка на профиль]({player['profileurl']})")
                
                st.divider()
                st.subheader("📦 Инвентарь CS2")
                # Кнопка для теста инвентаря
                if st.button("Проверить предметы"):
                    st.write("🔍 Запрашиваем список предметов у Steam...")
                    # Ссылка на инвентарь в формате JSON (хитрый способ)
                    inv_url = f"https://steamcommunity.com/inventory/{steam_id}/730/2?l=russian&count=75"
                    st.info(f"Пытаюсь достучаться до инвентаря по адресу: {inv_url}")
                    st.warning("Steam часто блокирует прямые запросы с серверов. Если ничего не появилось — значит, защиту еще не обошли.")
            else:
                st.error("Steam не вернул данные. Возможно, профиль скрыт.")
        except Exception as e:
            st.error(f"Техническая ошибка: {e}")
    else:
        st.warning("Вставь корректную ссылку, содержащую 17 цифр ID.")

st.divider()
st.caption("Powered by Steam Web API")