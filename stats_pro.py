import streamlit as st
import requests
import re
import json

# Настройки
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

STEAM_API_KEY = "80562D785863D2DB396C004F7547514D" 
TELEGRAM_LINK = "https://t.me/CS2devLog"
DONATE_LINK = "https://www.donationalerts.com/r/anter404"

with st.sidebar:
    st.title("ANTer404 | Project")
    st.markdown(f"[📢 Наш Telegram]({TELEGRAM_LINK})")
    st.markdown(f"[💰 Поддержать проект]({DONATE_LINK})")
    st.divider()
    st.caption("v1.1.8 | Обход блокировки")

st.title("📈 CS2 Pro Analytics")

user_input = st.text_input("Вставь ссылку на профиль Steam:", 
                          placeholder="Например: https://steamcommunity.com/profiles/76561198...")

if user_input:
    found_ids = re.findall(r'\d{17}', user_input)
    
    if found_ids:
        steam_id = found_ids[0]
        # Прямая ссылка на API
        api_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
        
        # Ссылка через прокси-сервер (магия обхода 403 ошибки)
        proxy_url = f"https://api.allorigins.win/get?url={requests.utils.quote(api_url)}"
        
        try:
            with st.spinner('Пробиваемся через защиту Steam...'):
                response = requests.get(proxy_url, timeout=15)
                
                if response.status_code == 200:
                    # Прокси возвращает JSON, в котором наши данные лежат в поле 'contents' в виде строки
                    raw_data = response.json()
                    steam_data = json.loads(raw_data['contents'])
                    
                    players = steam_data.get('response', {}).get('players', [])
                    
                    if players:
                        player = players[0]
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            st.image(player['avatarfull'], width=150)
                        with col2:
                            st.header(player['personaname'])
                            st.write(f"🆔 SteamID64: `{steam_id}`")
                            st.write(f"🌐 [Профиль в Steam]({player['profileurl']})")
                        
                        st.success("Связь установлена!")
                    else:
                        st.warning("Steam ответил, но игрока не нашел. Проверь ID.")
                else:
                    st.error(f"Прокси-сервер временно недоступен (Код {response.status_code})")
                    
        except Exception as e:
            st.error(f"Ошибка соединения: {e}")
    else:
        st.warning("В ссылке должен быть 17-значный ID.")

st.divider()
st.caption("Используется защищенный шлюз AllOrigins для обхода блокировок Steam.")