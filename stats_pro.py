import streamlit as st
import requests
import re

# 1. Настройки страницы
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

# 2. Константы и Ссылки
STEAM_API_KEY = "F0470B6F6D6AFBC9787C40C7507C6B58" # Твой ключ
APP_ID_CS2 = 730

TELEGRAM_LINK = "https://t.me/CS2devLog"
DONATE_PAYPAL = "https://www.donationalerts.com/r/anter404"
# Твоя ссылка на трейд
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
    st.caption("v1.3.0 | Inventory & Trade Lock")

st.title("📈 CS2 Pro Analytics")

# 4. Ввод данных
user_input = st.text_input("Вставь ссылку на профиль Steam:", 
                          placeholder="https://steamcommunity.com/profiles/76561198749701067/")

if user_input:
    found_ids = re.findall(r'\d{17}', user_input)
    
    if found_ids:
        steam_id = found_ids[0]
        
        # Ссылки API
        summary_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
        games_url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={steam_id}&format=json&include_appinfo=1"
        inv_url = f"https://steamcommunity.com/inventory/{steam_id}/{APP_ID_CS2}/2?l=russian&count=100"
        
        try:
            with st.spinner('Синхронизация данных...'):
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
                        
                        # Часы в игре
                        all_games = res_games.get('response', {}).get('games', [])
                        cs2_data = next((g for g in all_games if g['appid'] == APP_ID_CS2), None)
                        if cs2_data:
                            total_hours = round(cs2_data.get('playtime_forever', 0) / 60, 1)
                            st.metric("Часов в CS2", f"{total_hours} ч.")
                        else:
                            st.warning("🎮 Статистика игр скрыта.")
                    
                    st.divider()
                    
                    # 5. СЕКЦИЯ ИНВЕНТАРЯ
                    st.subheader("📦 Твой инвентарь")
                    
                    if res_inv and 'descriptions' in res_inv:
                        items = res_inv['descriptions']
                        assets = res_inv.get('assets', [])
                        
                        cols = st.columns(4)
                        for idx, item in enumerate(items):
                            with cols[idx % 4]:
                                # Картинка предмета
                                img_hash = item.get('icon_url')
                                if img_hash:
                                    img_url = f"https://community.akamai.steamstatic.com/economy/image/{img_hash}/200fx200f"
                                    st.image(img_url, use_container_width=True)
                                
                                # Имя предмета цветом редкости
                                name = item.get('market_name', 'Предмет')
                                color = item.get('name_color', 'FFFFFF')
                                st.markdown(f"<p style='color:#{color}; font-weight:bold; margin-bottom:0;'>{name}</p>", unsafe_allow_html=True)
                                
                                # Проверка на Trade Lock (если есть в assets)
                                is_tradable = item.get('tradable', 1)
                                if is_tradable == 0:
                                    st.error("⏳ Trade Lock")
                    else:
                        st.info("Инвентарь пуст, скрыт или предметы на продаже.")
                        
                else:
                    st.warning("Игрок не найден.")
        except Exception as e:
            st.error("Steam временно ограничил доступ к инвентарю. Попробуй позже.")
    else:
        st.warning("Ссылка не распознана.")

st.divider()
st.caption("Developed by ANTer404 | 2026")