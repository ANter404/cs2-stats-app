import streamlit as st
import requests
import re

# 1. Настройки страницы
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

# 2. Константы (Твой верный ключ и ссылки)
STEAM_API_KEY = "F0470B6F6D6AFBC9787C40C7507C6B58" 
TELEGRAM_LINK = "https://t.me/CS2devLog"
DONATE_LINK = "https://www.donationalerts.com/r/anter404"

# 3. Боковая панель
with st.sidebar:
    st.title("ANTer404 | Project")
    st.success("Ключ: Active ✅")
    st.divider()
    st.markdown(f"[📢 Наш Telegram]({TELEGRAM_LINK})")
    st.markdown(f"[💰 Поддержать проект]({DONATE_LINK})")
    st.divider()
    st.caption("v1.2.5 | Stable Build")

st.title("📈 CS2 Pro Analytics")

# 4. Ввод данных
user_input = st.text_input("Вставь ссылку на профиль Steam:", 
                          placeholder="https://steamcommunity.com/profiles/76561198749701067/")

if user_input:
    # Извлекаем SteamID64
    found_ids = re.findall(r'\d{17}', user_input)
    
    if found_ids:
        steam_id = found_ids[0]
        
        # Ссылки для API
        summary_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
        bans_url = f"https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={STEAM_API_KEY}&steamids={steam_id}"
        
        try:
            with st.spinner('Синхронизация со Steam...'):
                # Запрос данных профиля
                res_summary = requests.get(summary_url, timeout=10)
                # Запрос данных о банах
                res_bans = requests.get(bans_url, timeout=10)
                
                if res_summary.status_code == 200:
                    data = res_summary.json()
                    players = data.get('response', {}).get('players', [])
                    
                    if players:
                        player = players[0]
                        
                        # Отображение профиля
                        col1, col2 = st.columns([1, 3])
                        
                        with col1:
                            st.image(player['avatarfull'], width=200)
                        
                        with col2:
                            st.header(player['personaname'])
                            
                            # Проверка банов
                            if res_bans.status_code == 200:
                                b_data = res_bans.json().get('players', [{}])[0]
                                if b_data.get('VACBanned'):
                                    st.error("🛡️ VAC Статус: Заблокирован")
                                else:
                                    st.success("🛡️ VAC Статус: Чист")
                                    
                                if b_data.get('CommunityBanned'):
                                    st.warning("🚫 Бан в сообществе: Присутствует")
                            
                            st.write(f"🆔 SteamID64: `{steam_id}`")
                            st.write(f"🌐 [Ссылка на профиль в Steam]({player['profileurl']})")
                            
                        st.divider()
                        st.info("📊 Статистика CS2 и Инвентарь появятся в следующем обновлении!")
                        
                    else:
                        st.warning("Профиль не найден. Убедись, что он открыт.")
                else:
                    st.error(f"Ошибка Steam API: {res_summary.status_code}")
                    
        except Exception as e:
            st.error(f"Ошибка соединения: {e}")
    else:
        st.warning("Пожалуйста, вставь корректную ссылку профиля.")

st.divider()
st.caption("Powered by Steam Web API | © 2026 ANTer404")