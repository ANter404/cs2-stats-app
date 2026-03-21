import streamlit as st
import requests
import re

# Настройки
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

STEAM_API_KEY = "80562D785863D2DB396C004F7547514D" 
TELEGRAM_LINK = "https://t.me/CS2devLog"
DONATE_LINK = "https://www.donationalerts.com/r/anter404"

# Усиленная маскировка
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://steamcommunity.com/'
}

with st.sidebar:
    st.title("ANTer404 | Project")
    st.markdown(f"[📢 Наш Telegram]({TELEGRAM_LINK})")
    st.markdown(f"[💰 Поддержать проект]({DONATE_LINK})")
    st.divider()
    st.caption("v1.1.7 | Анти-бан сборка")

st.title("📈 CS2 Pro Analytics")

user_input = st.text_input("Вставь ссылку на профиль Steam:", 
                          placeholder="Например: https://steamcommunity.com/profiles/76561198...")

if user_input:
    found_ids = re.findall(r'\d{17}', user_input)
    
    if found_ids:
        steam_id = found_ids[0]
        # ИСПОЛЬЗУЕМ HTTPS вместо HTTP
        url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
        
        try:
            # Пробуем сделать запрос
            response = requests.get(url, headers=HEADERS, timeout=10)
            
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
                else:
                    st.warning("Steam не нашел игрока. Проверь настройки приватности своего профиля.")
            else:
                # Если всё еще 403, предлагаем решение
                st.error(f"Ошибка {response.status_code}: Steam блокирует облачный сервер.")
                st.info("💡 Попробуй подождать 5 минут или вставь ссылку еще раз. Мы работаем над обходом блокировки!")
                
        except Exception as e:
            st.error(f"Связь оборвалась. Попробуй обновить страницу.")
    else:
        st.warning("В ссылке должен быть 17-значный ID.")

st.divider()
st.caption("Powered by Steam Web API")