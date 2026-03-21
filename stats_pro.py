import streamlit as st
import requests
import re
import time

# 1. Настройки страницы
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

# 2. Константы
STEAM_API_KEY = "F0470B6F6D6AFBC9787C40C7507C6B58" 
APP_ID_CS2 = 730
TELEGRAM_LINK = "https://t.me/CS2devLog"
TRADE_LINK = "https://steamcommunity.com/tradeoffer/new/?partner=789435339&token=ftuQJ9Sg"
DONATE_LINK = "https://www.donationalerts.com/r/anter404"
CONTACT_EMAIL = "cs2-pro-help@mail.ru" 

# 3. Функция получения цены (Market API)
def get_item_price(market_hash_name):
    try:
        url = f"https://steamcommunity.com/market/priceoverview/?appid={APP_ID_CS2}&currency=1&market_hash_name={market_hash_name}"
        res = requests.get(url, timeout=5).json()
        if res.get('success'):
            return res.get('lowest_price', 'N/A')
    except:
        return "🛠️"
    return "N/A"

# 4. Сессии
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'steam_id' not in st.session_state: st.session_state.steam_id = ""

# 5. Боковая панель
with st.sidebar:
    st.title("ANTer404 | Project")
    if st.session_state.logged_in:
        st.success("✅ Аккаунт привязан")
        if st.button("Выйти"):
            st.session_state.logged_in = False
            st.rerun()
    
    st.divider()
    st.subheader("⚙️ Настройки")
    theme = st.radio("Тема сайта:", ["Темная", "Светлая"])
    
    if theme == "Светлая":
        st.markdown("""<style>
            .stApp { background-color: white; color: black; }
            [data-testid="stMetricValue"] { color: #FF4B4B !important; }
            section[data-testid="stSidebar"] { background-color: #f0f2f6; }
            h1, h2, h3, p, span { color: black !important; }
        </style>""", unsafe_allow_html=True)

    st.divider()
    st.markdown(f"### [🚀 Наш Telegram]({TELEGRAM_LINK})")
    st.markdown(f"### [🎁 Поддержать трейдом]({TRADE_LINK})")
    st.markdown(f"### [💰 Донат (Деньги)]({DONATE_LINK})")
    
    st.divider()
    st.subheader("🛠️ Техподдержка")
    support_mode = st.checkbox("Написать админу")
    st.caption("v1.6.1 | Full & Market Edition")

# 6. ТЕХПОДДЕРЖКА
if support_mode:
    st.header("📩 Техническая поддержка")
    contact_form = f"""
    <form action="https://formsubmit.co/{CONTACT_EMAIL}" method="POST" enctype="multipart/form-data">
    <input type="email" name="email" placeholder="Твоя почта" required style="width:100%; margin-bottom:10px; padding:10px; border-radius:5px; border:1px solid #333;">
    <textarea name="message" placeholder="Ваш вопрос..." required style="width:100%; height:120px; margin-bottom:10px; padding:10px; border-radius:5px; border:1px solid #333;"></textarea>
    <button type="submit" style="background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:5px; width:100%; font-weight:bold; cursor:pointer;">Отправить</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)

# 7. ГЛАВНЫЙ ЭКРАН
elif not st.session_state.logged_in:
    st.title("📈 CS2 Pro Analytics")
    user_input = st.text_input("Вставьте ссылку на профиль Steam:")
    if st.button("Войти"):
        found = re.findall(r'\d{17}', user_input)
        if found:
            st.session_state.steam_id = found[0]
            st.session_state.logged_in = True
            st.rerun()
else:
    steam_id = st.session_state.steam_id
    try:
        with st.spinner('Синхронизация со Steam...'):
            summary_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
            stats_url = f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={APP_ID_CS2}&key={STEAM_API_KEY}&steamid={steam_id}"
            games_url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={steam_id}&format=json&include_appinfo=1"
            inv_url = f"https://steamcommunity.com/inventory/{steam_id}/{APP_ID_CS2}/2?l=russian&count=50"
            
            res_summary = requests.get(summary_url).json()
            res_stats = requests.get(stats_url).json()
            res_games = requests.get(games_url).json()
            res_inv = requests.get(inv_url).json()
            
            player = res_summary['response']['players'][0]
            
            col1, col2 = st.columns([1, 4])
            with col1: st.image(player['avatarfull'], width=150)
            with col2:
                st.header(player['personaname'])
                all_games = res_games.get('response', {}).get('games', [])
                cs2_data = next((g for g in all_games if g['appid'] == APP_ID_CS2), None)
                if cs2_data:
                    st.write(f"🎮 Часов в CS2: **{round(cs2_data.get('playtime_forever', 0) / 60, 1)} ч.**")
                
                if 'playerstats' in res_stats:
                    s = {i['name']: i['value'] for i in res_stats['playerstats']['stats']}
                    k, d = s.get('total_kills', 0), s.get('total_deaths', 1)
                    st.divider()
                    m1, m2, m3 = st.columns(3)
                    m1.metric("K/D Ratio", round(k/d, 2))
                    m2.metric("Headshots", s.get('total_kills_headshot', 0))
                    m3.metric("Total Kills", k)

            st.divider()
            st.subheader("📦 Твой инвентарь и цены")
            
            if res_inv and 'descriptions' in res_inv:
                items = res_inv['descriptions']
                grid = st.columns(5)
                for idx, item in enumerate(items):
                    with grid[idx % 5]:
                        img = item.get('icon_url')
                        st.image(f"https://community.akamai.steamstatic.com/economy/image/{img}/128fx128f")
                        
                        # ЦЕНЫ (ограничено первыми 10 для скорости)
                        if idx < 10:
                            price = get_item_price(item.get('market_hash_name'))
                            st.markdown(f"💰 **{price}**")
                        
                        name = item.get('market_name')
                        color = item.get('name_color', 'FFFFFF')
                        st.markdown(f"<p style='color:#{color}; font-size:11px; font-weight:bold;'>{name}</p>", unsafe_allow_html=True)
            else:
                st.info("Инвентарь не подгрузился.")
    except:
        st.error("Steam API Error")

st.divider()
st.caption("Developed by ANTer404 | 2026")