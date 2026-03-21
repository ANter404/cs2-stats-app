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
    st.caption("v1.1.9 | Ultra Bypass")

st.title("📈 CS2 Pro Analytics")

user_input = st.text_input("Вставь ссылку на профиль Steam:", 
                          placeholder="https://steamcommunity.com/profiles/76561198...")

if user_input:
    found_ids = re.findall(r'\d{17}', user_input)
    
    if found_ids:
        steam_id = found_ids[0]
        api_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
        
        # Используем альтернативный прокси-шлюз
        proxy_url = f"https://api.codetabs.com/v1/proxy?quest={api_url}"
        
        try:
            with st.spinner('Взламываем систему...'):
                response = requests.get(proxy_url, timeout=20)
                
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
                            st.write(f"🆔 SteamID64: `{steam_id}`")
                            st.write(f"🌐 [Профиль в Steam]({player['profileurl']})")
                        st.success("Данные успешно получены через резервный шлюз!")
                    else:
                        st.warning("Steam не нашел игрока. Проверь настройки приватности.")
                else:
                    st.error(f"Ошибка шлюза: {response.status_code}. Пробуем другой метод...")
        except Exception as e:
            st.error(f"Критический сбой: {e}")
    else:
        st.warning("Вставь ссылку, содержащую 17 цифр ID.")

st.divider()
st.caption("Используется технология CodeTabs для обхода сетевых ограничений.")