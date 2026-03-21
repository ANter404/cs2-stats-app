import streamlit as st
import requests
import re

# 1. Настройки страницы
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

# 2. Константы
STEAM_API_KEY = "F0470B6F6D6AFBC9787C40C7507C6B58" 
APP_ID_CS2 = 730

TELEGRAM_LINK = "https://t.me/CS2devLog"
DONATE_PAYPAL = "https://www.donationalerts.com/r/anter404"
TRADE_LINK = "https://steamcommunity.com/tradeoffer/new/?partner=789435339&token=ftuQJ9Sg" 

# 3. Боковая панель
with st.sidebar:
    st.title("ANTer404 | Project")
    st.success("Ключ: Active ✅")
    st.divider()
    st.subheader("💎 Поддержка")
    st.markdown(f"💰 [Донат]({DONATE_PAYPAL})")
    st.markdown(f"🎁 [Трейд]({TRADE_LINK})")
    st.divider()
    st.caption("v1.2.9 | Inventory Engine")

st.title("📈 CS2 Pro Analytics")

user_input = st.text_input("Вставь ссылку на профиль Steam:", 
                          placeholder="https://steamcommunity.com/profiles/76561198749701067/")

if user_input:
    found_ids = re.findall(r'\d{17}', user_input)
    
    if found_ids:
        steam_id = found_ids[0]
        
        # Ссылки API
        summary_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
        games_url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={steam_id}&format=json&include_appinfo=1"
        # Ссылка на инвентарь (через общедоступный JSON Steam)
        inv_url = f"https://steamcommunity.com/inventory/{steam_id}/{APP_ID_CS2}/2?l=russian&count=100"
        
        try:
            with st.spinner('Загружаем инвентарь...'):
                res_summary = requests.get(summary_url, timeout=10).json()
                res_games = requests.get(games_url, timeout=10).json()
                res_inv = requests.get(inv_url, timeout=10).json()
                
                players = res_summary.get('response', {}).get('players', [])
                
                if players:
                    player = players[0]
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        st.image(player['avatarfull'], width=200)
                    
                    with col2:
                        st.header(player['personaname'])
                        
                        # Время в игре
                        all_games = res_games.get('response', {}).get('games', [])
                        cs2_data = next((game for game in all_games if game['appid'] == APP_ID_CS2), None)
                        if cs2_data:
                            total_hours = round(cs2_data.get('playtime_forever', 0) / 60, 1)
                            st.metric("Часов в CS2", f"{total_hours} ч.")
                    
                    st.divider()
                    
                    # БЛОК ИНВЕНТАРЯ
                    st.subheader("📦 Инвентарь CS2")
                    
                    if res_inv and 'descriptions' in res_inv:
                        items = res_inv['descriptions']
                        
                        # Создаем сетку (по 4 предмета в ряд)
                        cols = st.columns(4)
                        for idx, item in enumerate(items):
                            with cols[idx % 4]:
                                # Ссылка на картинку Steam Community
                                img_hash = item.get('icon_url')
                                if img_hash:
                                    img_url = f"https://community.akamai.steamstatic.com/economy/image/{img_hash}/200fx200f"
                                    st.image(img_url, use_container_width=True)
                                
                                # Название и редкость
                                name = item.get('market_name', 'Предмет')
                                color = item.get('name_color', 'FFFFFF')
                                st.markdown(f"<p style='color:#{color}; font-weight:bold;'>{name}</p>", unsafe_allow_value=True)
                    else:
                        st.info("Инвентарь пуст или скрыт настройками приватности.")
                        
                else:
                    st.warning("Игрок не найден.")
        except Exception as e:
            st.error(f"Steam временно ограничил доступ к инвентарю. Попробуй обновить через минуту.")
    else:
        st.warning("Вставь корректную ссылку.")

st.divider()
st.caption("ANTer404 Dev | 2026")