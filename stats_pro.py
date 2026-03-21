import streamlit as st
import requests
import re
import time

# 1. Настройки страницы
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

# 2. Твои данные
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
    st.markdown(f"💰 [Донат (Деньги)]({DONATE_PAYPAL})")
    st.markdown(f"🎁 [Трейд (Скины)]({TRADE_LINK})")
    st.divider()
    st.caption("v1.3.2 | Compact Inventory")

st.title("📈 CS2 Pro Analytics")

user_input = st.text_input("Вставь ссылку на профиль Steam:", 
                          value="https://steamcommunity.com/profiles/76561198749701067/")

if user_input:
    found_ids = re.findall(r'\d{17}', user_input)
    
    if found_ids:
        steam_id = found_ids[0]
        summary_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
        games_url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={steam_id}&format=json&include_appinfo=1"
        inv_url = f"https://steamcommunity.com/inventory/{steam_id}/{APP_ID_CS2}/2?l=russian&count=100&_={int(time.time())}"
        
        try:
            with st.spinner('Загрузка...'):
                res_summary = requests.get(summary_url, timeout=10).json()
                res_games = requests.get(games_url, timeout=10).json()
                res_inv = requests.get(inv_url, timeout=10).json()
                
                players = res_summary.get('response', {}).get('players', [])
                
                if players:
                    player = players[0]
                    col1, col2 = st.columns([1, 4])
                    
                    with col1:
                        st.image(player['avatarfull'], width=150)
                    
                    with col2:
                        st.header(player['personaname'])
                        all_games = res_games.get('response', {}).get('games', [])
                        cs2_data = next((g for g in all_games if g['appid'] == APP_ID_CS2), None)
                        if cs2_data:
                            total_hours = round(cs2_data.get('playtime_forever', 0) / 60, 1)
                            st.write(f"🎮 Часов в CS2: **{total_hours} ч.**")
                    
                    st.divider()
                    st.subheader("📦 Твой инвентарь")
                    
                    if res_inv and 'descriptions' in res_inv:
                        items = res_inv['descriptions']
                        # Делаем сетку по 6 предметов в ряд, чтобы было компактно
                        cols = st.columns(6) 
                        
                        for idx, item in enumerate(items):
                            with cols[idx % 6]:
                                img_hash = item.get('icon_url')
                                if img_hash:
                                    img_url = f"https://community.akamai.steamstatic.com/economy/image/{img_hash}/100fx100f"
                                    st.image(img_url, use_container_width=True)
                                
                                name = item.get('market_name', 'Предмет')
                                color = item.get('name_color', 'FFFFFF')
                                st.markdown(f"<p style='color:#{color}; font-size: 11px; font-weight:bold; line-height: 1.1;'>{name}</p>", unsafe_allow_html=True)
                                
                                if item.get('tradable') == 0:
                                    st.markdown("<span style='color:#ff4b4b; font-size:9px;'>⏳ Lock</span>", unsafe_allow_html=True)
                                else:
                                    st.markdown("<span style='color:#00ff00; font-size:9px;'>✅ Ready</span>", unsafe_allow_html=True)
                    else:
                        st.info("Инвентарь пока не подтянулся. Попробуй обновить позже.")
                else:
                    st.warning("Профиль не найден.")
        except:
            st.error("Steam занят, обнови страницу через 10 секунд.")
    else:
        st.warning("Вставь ссылку с ID.")

st.divider()
st.caption("ANTer404 Dev | 2026")