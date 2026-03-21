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
    st.caption("v1.1.3 | © 2026")

st.title("📈 CS2 Pro Analytics")

# Поле ввода (теперь максимально удобное)
user_input = st.text_input("Вставь ссылку на Steam профиль или ID:", 
                          placeholder="https://steamcommunity.com/id/anter404/")

if user_input:
    steam_id = None
    
    # Способ 1: Если ввели просто 17 цифр
    if user_input.isdigit() and len(user_input) == 17:
        steam_id = user_input
    
    # Способ 2: Если в ссылке уже есть цифры (profiles/7656...)
    elif "profiles/" in user_input:
        found = re.findall(r'\d{17}', user_input)
        if found:
            steam_id = found[0]
            
    # Способ 3: Если в ссылке ник (id/nickname)
    elif "id/" in user_input:
        vanity_url = user_input.split("id/")[1].strip("/")
        res_id = requests.get(f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={STEAM_API_KEY}&vanityurl={vanity_url}").json()
        if res_id.get('response', {}).get('success') == 1:
            steam_id = res_id['response']['steamid']

    if steam_id:
        # Получаем данные профиля
        url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
        try:
            res = requests.get(url).json()
            players = res.get('response', {}).get('players', [])
            
            if players:
                player = players[0]
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.image(player['avatarfull'], width=150)
                with col2:
                    st.header(player['personaname'])
                    st.write(f"🆔 SteamID64: `{steam_id}`")
                    st.write(f"🔗 [Открыть профиль в Steam]({player['profileurl']})")
                
                st.divider()
                st.subheader("📦 Инвентарь CS2")
                st.info("🔄 Настраиваем парсинг предметов... Загляни в ТГ за новостями!")
            else:
                st.error("Steam вернул пустой профиль. Проверь настройки приватности.")
        except:
            st.error("Ошибка получения данных. Попробуй обновить страницу.")
    else:
        st.warning("Не удалось распознать ссылку. Попробуй скопировать её целиком из браузера.")

st.divider()
st.caption("Powered by Steam Web API")