import streamlit as st
import requests
import re

# Настройки страницы
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

# ТВОЙ НАСТОЯЩИЙ КЛЮЧ
STEAM_API_KEY = "F0470B6F6D6AFBC9787C40C7507C6B58" 
TELEGRAM_LINK = "https://t.me/CS2devLog"
DONATE_LINK = "https://www.donationalerts.com/r/anter404"

# Боковая панель
with st.sidebar:
    st.title("ANTer404 | Project")
    st.success("Ключ активирован! ✅")
    st.divider()
    st.markdown(f"[📢 Наш Telegram]({TELEGRAM_LINK})")
    st.markdown(f"[💰 Поддержать проект]({DONATE_LINK})")
    st.divider()
    st.caption("v1.2.4 | Official Key Build")

st.title("📈 CS2 Pro Analytics")

# Поле ввода
user_input = st.text_input("Вставь ссылку на профиль Steam:", 
                          placeholder="https://steamcommunity.com/profiles/76561198749701067/")

if user_input:
    # Ищем ID в ссылке
    found_ids = re.findall(r'\d{17}', user_input)
    
    if found_ids:
        steam_id = found_ids[0]
        url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
        
        try:
            with st.spinner('Получаем данные из Steam...'):
                # Пробуем прямой запрос с твоим новым ключом
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
                            st.write(f"🌐 [Открыть профиль]({player['profileurl']})")
                        st.balloons() # Маленький праздник в честь успеха!
                    else:
                        st.warning("Steam не нашел игрока. Проверь, не скрыт ли профиль.")
                elif response.status_code == 403:
                    st.error("Ошибка 403: Steam всё еще блокирует сервер Streamlit.")
                    st.info("Если это видишь — значит пора запускать наш 'шлюз' на Vercel, про который я говорил!")
                else:
                    st.error(f"Ошибка Steam: {response.status_code}")
        except Exception as e:
            st.error(f"Техническая заминка: {e}")
    else:
        st.warning("Вставь ссылку, в которой есть 17 цифр ID.")

st.divider()
st.caption("Powered by ANTer404 Development")