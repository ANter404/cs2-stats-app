import streamlit as st
import requests
import re

# 1. Настройки
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

# Твои данные
STEAM_API_KEY = "80562D785863D2DB396C004F7547514D" 
TELEGRAM_LINK = "https://t.me/CS2devLog"
DONATE_LINK = "https://www.donationalerts.com/r/anter404"

# Маскировка
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

with st.sidebar:
    st.title("ANTer404 | Project")
    st.markdown(f"[📢 Наш Telegram]({TELEGRAM_LINK})")
    st.markdown(f"[💰 Поддержать проект]({DONATE_LINK})")
    st.divider()
    st.caption("v1.1.6 | Стабильная сборка")

st.title("📈 CS2 Pro Analytics")

# ПУСТОЕ ПОЛЕ (заменили value на placeholder)
user_input = st.text_input("Вставь ссылку на профиль Steam:", 
                          placeholder="Например: https://steamcommunity.com/profiles/76561198...")

if user_input:
    # Вытягиваем ID
    found_ids = re.findall(r'\d{17}', user_input)
    
    if found_ids:
        steam_id = found_ids[0]
        url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
        
        try:
            # Делаем запрос с таймаутом, чтобы сайт не вис
            response = requests.get(url, headers=HEADERS, timeout=5)
            
            if response.status_code == 200:
                try:
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
                    else:
                        st.warning("Steam не нашел игрока. Проверь, не скрыт ли профиль.")
                except:
                    st.error("Steam прислал битые данные. Попробуй обновить страницу через минуту.")
            elif response.status_code == 403:
                st.error("Steam заблокировал доступ облачному серверу (Ошибка 403). Попробуй позже.")
            else:
                st.error(f"Ошибка Steam: {response.status_code}")
                
        except Exception as e:
            st.error("Не удалось связаться со Steam. Проверь интернет или попробуй позже.")
    else:
        st.warning("В ссылке не найден SteamID64 (17 цифр).")

st.divider()
st.caption("Powered by Steam Web API")