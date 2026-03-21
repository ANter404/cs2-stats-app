import streamlit as st
import requests
import re

st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

# Прячем ключ обратно в переменную
STEAM_API_KEY = "80562D785863D2DB396C004F7547514D" 
TELEGRAM_LINK = "https://t.me/CS2devLog"
DONATE_LINK = "https://www.donationalerts.com/r/anter404"

with st.sidebar:
    st.title("ANTer404 | Project")
    st.markdown(f"[📢 Наш Telegram]({TELEGRAM_LINK})")
    st.markdown(f"[💰 Поддержать проект]({DONATE_LINK})")
    st.divider()
    st.caption("v1.2.1 | Security Patch")

st.title("📈 CS2 Pro Analytics")

user_input = st.text_input("Вставь ссылку на профиль Steam:", 
                          placeholder="Например: https://steamcommunity.com/profiles/76561198...")

if user_input:
    found_ids = re.findall(r'\d{17}', user_input)
    
    if found_ids:
        steam_id = found_ids[0]
        url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
        
        try:
            with st.spinner('Загрузка данных...'):
                response = requests.get(url, timeout=10)
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
                    else:
                        st.warning("Игрок не найден.")
                else:
                    st.error(f"Ошибка доступа (Код {response.status_code})")
        except Exception as e:
            st.error("Ошибка соединения.")