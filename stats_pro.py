import streamlit as st
import requests
import re

# Настройки
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

# Твои ссылки
TELEGRAM_LINK = "https://t.me/CS2devLog"
DONATE_LINK = "https://www.donationalerts.com/r/anter404"

with st.sidebar:
    st.title("ANTer404 | Project")
    st.markdown(f"[📢 Наш Telegram]({TELEGRAM_LINK})")
    st.markdown(f"[💰 Поддержать проект]({DONATE_LINK})")
    st.divider()
    st.caption("v1.2.0 | Direct Mode")

st.title("📈 CS2 Pro Analytics")

# Поле для ключа (на случай, если твой забанили, можно будет вставить другой)
# Но по умолчанию используем твой
api_key = st.sidebar.text_input("Steam API Key:", value="80562D785863D2DB396C004F7547514D", type="password")

user_input = st.text_input("Вставь ссылку на профиль Steam:", 
                          placeholder="Например: https://steamcommunity.com/profiles/76561198...")

if user_input:
    found_ids = re.findall(r'\d{17}', user_input)
    
    if found_ids:
        steam_id = found_ids[0]
        # Используем стандартный эндпоинт без прокси для проверки
        url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_id}"
        
        try:
            with st.spinner('Связываемся со Steam...'):
                # Добавляем очень длинный таймаут
                response = requests.get(url, timeout=30)
                
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
                        st.success("Успешное подключение!")
                    else:
                        st.warning("Steam не нашел игрока. Возможно, профиль скрыт настройками приватности.")
                else:
                    st.error(f"Ошибка Steam API: {response.status_code}")
                    st.info("Это значит, что Steam блокирует сервер хостинга. Не волнуйся, это решаемо.")
        except Exception as e:
            st.error(f"Не удалось получить данные. Steam сбросил соединение.")
    else:
        st.warning("В ссылке должен быть 17-значный ID.")

st.divider()
st.caption("Разработка продолжается. Мы найдем способ обойти ограничения!")