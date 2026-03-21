import streamlit as st
import requests
import re

# 1. Настройки страницы
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

# 2. Константы
STEAM_API_KEY = "F0470B6F6D6AFBC9787C40C7507C6B58" 
APP_ID_CS2 = 730

# ССЫЛКИ ДЛЯ ПОДДЕРЖКИ
TELEGRAM_LINK = "https://t.me/CS2devLog"
DONATE_PAYPAL = "https://www.donationalerts.com/r/anter404"
# Твоя ссылка на трейд добавлена!
TRADE_LINK = "https://steamcommunity.com/tradeoffer/new/?partner=789435339&token=ftuQJ9Sg" 

# 3. Боковая панель
with st.sidebar:
    st.title("ANTer404 | Project")
    st.success("Ключ: Active ✅")
    st.divider()
    
    st.subheader("📢 Сообщество")
    st.markdown(f"🔗 [Наш Telegram канал]({TELEGRAM_LINK})")
    
    st.divider()
    st.subheader("💎 Поддержать автора")
    # Кнопки поддержки
    st.markdown(f"💰 [Задонатить рублём]({DONATE_PAYPAL})")
    st.markdown(f"🎁 [Поддержать скинами]({TRADE_LINK})")
    
    st.divider()
    st.caption("v1.2.8 | Trade Link Integrated")

st.title("📈 CS2 Pro Analytics")

# 4. Ввод данных
user_input = st.text_input("Вставь ссылку на профиль Steam:", 
                          placeholder="https://steamcommunity.com/profiles/76561198749701067/")

if user_input:
    found_ids = re.findall(r'\d{17}', user_input)
    
    if found_ids:
        steam_id = found_ids[0]
        
        # API Эндпоинты
        summary_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
        bans_url = f"https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={STEAM_API_KEY}&steamids={steam_id}"
        games_url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={steam_id}&format=json&include_appinfo=1"
        
        try:
            with st.spinner('Анализируем профиль...'):
                res_summary = requests.get(summary_url, timeout=10).json()
                res_bans = requests.get(bans_url, timeout=10).json()
                res_games = requests.get(games_url, timeout=10).json()
                
                players = res_summary.get('response', {}).get('players', [])
                
                if players:
                    player = players[0]
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        st.image(player['avatarfull'], width=200)
                    
                    with col2:
                        st.header(player['personaname'])
                        
                        # Статус банов
                        b_data = res_bans.get('players', [{}])[0]
                        vac_color = "red" if b_data.get('VACBanned') else "green"
                        st.markdown(f"🛡️ VAC Статус: :{vac_color}[{'Забанен' if b_data.get('VACBanned') else 'Чист'}]")
                        
                        # Время в игре
                        all_games = res_games.get('response', {}).get('games', [])
                        cs2_data = next((game for game in all_games if game['appid'] == APP_ID_CS2), None)
                        
                        if cs2_data:
                            total_hours = round(cs2_data.get('playtime_forever', 0) / 60, 1)
                            recent_hours = round(cs2_data.get('playtime_2weeks', 0) / 60, 1)
                            
                            st.subheader("📊 Статистика CS2")
                            m_col1, m_col2 = st.columns(2)
                            m_col1.metric("Всего часов", f"{total_hours} ч.")
                            m_col2.metric("За последние 2 недели", f"{recent_hours} ч.")
                        else:
                            st.warning("🎮 Информация об играх скрыта в настройках Steam.")

                        st.write(f"🆔 SteamID64: `{steam_id}`")
                    
                    st.divider()
                    st.info("📦 Следующий этап: Вывод инвентаря и цен на предметы")
                    
                else:
                    st.warning("Игрок не найден. Проверь ссылку.")
        except Exception as e:
            st.error(f"Сбой при получении данных: {e}")
    else:
        st.warning("Ссылка должна содержать 17-значный SteamID.")

st.divider()
st.caption("ANTer404 Dev | 2026")