import streamlit as st
import requests
import re

# 1. Настройки страницы
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

# 2. Константы
STEAM_API_KEY = "F0470B6F6D6AFBC9787C40C7507C6B58" 
APP_ID_CS2 = 730 # ID Counter-Strike 2 в Steam

# 3. Боковая панель
with st.sidebar:
    st.title("ANTer404 | Project")
    st.success("Ключ: Active ✅")
    st.divider()
    st.markdown("[📢 Наш Telegram](https://t.me/CS2devLog)")
    st.caption("v1.2.6 | Stats Update")

st.title("📈 CS2 Pro Analytics")

user_input = st.text_input("Вставь ссылку на профиль Steam:", 
                          placeholder="https://steamcommunity.com/profiles/76561198749701067/")

if user_input:
    found_ids = re.findall(r'\d{17}', user_input)
    
    if found_ids:
        steam_id = found_ids[0]
        
        # API Эндпоинты
        summary_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
        bans_url = f"https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={STEAM_API_KEY}&steamids={steam_id}"
        # Новый эндпоинт для времени в играх
        games_url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={steam_id}&format=json&include_appinfo=1"
        
        try:
            with st.spinner('Анализируем игровые данные...'):
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
                        
                        # Блок статуса безопасности
                        b_data = res_bans.get('players', [{}])[0]
                        vac_color = "red" if b_data.get('VACBanned') else "green"
                        st.markdown(f"🛡️ VAC Статус: :{vac_color}[{'Забанен' if b_data.get('VACBanned') else 'Чист'}]")
                        
                        # Извлекаем время в CS2
                        all_games = res_games.get('response', {}).get('games', [])
                        cs2_data = next((game for game in all_games if game['appid'] == APP_ID_CS2), None)
                        
                        if cs2_data:
                            # Время в Steam API отдается в минутах
                            total_minutes = cs2_data.get('playtime_forever', 0)
                            total_hours = round(total_minutes / 60, 1)
                            
                            st.subheader("📊 Статистика CS2")
                            metrics_col1, metrics_col2 = st.columns(2)
                            metrics_col1.metric("Всего часов", f"{total_hours} ч.")
                            
                            # Время за последние 2 недели
                            recent_minutes = cs2_data.get('playtime_2weeks', 0)
                            recent_hours = round(recent_minutes / 60, 1)
                            metrics_col2.metric("За 2 недели", f"{recent_hours} ч.")
                        else:
                            st.warning("🎮 Данные об играх скрыты или CS2 не найдена в библиотеке.")

                        st.write(f"🆔 SteamID64: `{steam_id}`")
                        st.write(f"🔗 [Профиль в Steam]({player['profileurl']})")

                    st.divider()
                    st.info("💡 Следующий шаг: Инвентарь и скины")
                    
                else:
                    st.warning("Профиль не найден.")
        except Exception as e:
            st.error(f"Ошибка получения данных: {e}")