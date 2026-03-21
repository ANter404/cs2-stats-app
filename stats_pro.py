import streamlit as st
import requests
import re

# Настройки
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

STEAM_API_KEY = "80562D785863D2DB396C004F7547514D" 
TELEGRAM_LINK = "https://t.me/CS2devLog"
DONATE_LINK = "https://www.donationalerts.com/r/anter404"

# Маскировка под обычный браузер
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

with st.sidebar:
    st.title("ANTer404 | Project")
    st.markdown(f"[📢 Наш Telegram]({TELEGRAM_LINK})")
    st.markdown(f"[💰 Поддержать проект]({DONATE_LINK})")
    st.divider()
    st.caption("v1.1.5 | Маскировка: ON")

st.title("📈 CS2 Pro Analytics")

user_input = st.text_input("Вставь ссылку на профиль:", 
                          value="https://steamcommunity.com/profiles/76561198749701067/")

if user_input:
    found_ids = re.findall(r'\d{17}', user_input)
    
    if found_ids:
        steam_id = found_ids[0]
        url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
        
        try:
            # Делаем запрос с маскировкой HEADERS
            response = requests.get(url, headers=HEADERS)
            
            if response.status_code == 200:
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
                    st.info("Раздел в разработке (День 2)")
                else:
                    st.error("Steam API вернул пустой список. Профиль может быть скрыт.")
            else:
                st.error(f"Steam API ответил ошибкой {response.status_code}. Попробуй позже.")
                
        except Exception as e:
            st.error(f"Ошибка парсинга: {e}")
    else:
        st.warning("Вставь корректную ссылку с 17 цифрами.")

st.divider()
st.caption("Powered by Steam Web API")