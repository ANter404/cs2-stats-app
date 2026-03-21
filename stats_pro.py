import streamlit as st
import requests
import re
import time

# 1. Настройки страницы
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

# 2. Константы
STEAM_API_KEY = "F0470B6F6D6AFBC9787C40C7507C6B58" 
APP_ID_CS2 = 730
CONTACT_EMAIL = "cs2-pro-help@mail.ru" 

# 3. Функции для экономики
def get_item_price(market_hash_name):
    """Получает минимальную цену предмета на рынке Steam"""
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
        if st.button("Выйти"):
            st.session_state.logged_in = False
            st.rerun()
    
    st.divider()
    st.subheader("⚙️ Тема")
    theme = st.radio("Выбор:", ["Темная", "Светлая"])
    
    if theme == "Светлая":
        st.markdown("""<style>
            .stApp { background-color: white; color: black; }
            [data-testid="stMetricValue"] { color: #FF4B4B !important; }
            section[data-testid="stSidebar"] { background-color: #f0f2f6; }
            h1, h2, h3, p, span { color: black !important; }
        </style>""", unsafe_allow_html=True)

    st.divider()
    st.caption("v1.6.0 | Market Prices")

# 6. ГЛАВНЫЙ ЭКРАН
if not st.session_state.logged_in:
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
        # Загрузка данных
        summary_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
        stats_url = f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={APP_ID_CS2}&key={STEAM_API_KEY}&steamid={steam_id}"
        inv_url = f"https://steamcommunity.com/inventory/{steam_id}/{APP_ID_CS2}/2?l=russian&count=50"
        
        res_summary = requests.get(summary_url).json()
        res_stats = requests.get(stats_url).json()
        res_inv = requests.get(inv_url).json()
        
        player = res_summary['response']['players'][0]
        
        col1, col2 = st.columns([1, 3])
        with col1: st.image(player['avatarfull'], width=150)
        with col2:
            st.header(player['personaname'])
            if 'playerstats' in res_stats:
                s = {i['name']: i['value'] for i in res_stats['playerstats']['stats']}
                kd = round(s.get('total_kills', 0)/s.get('total_deaths', 1), 2)
                st.metric("Твой K/D", kd)

        st.divider()
        st.subheader("📦 Оценка инвентаря")
        
        if res_inv and 'descriptions' in res_inv:
            items = res_inv['descriptions']
            grid = st.columns(5)
            
            for idx, item in enumerate(items):
                with grid[idx % 5]:
                    img = item.get('icon_url')
                    st.image(f"https://community.akamai.steamstatic.com/economy/image/{img}/100fx100f")
                    
                    name = item.get('market_name')
                    # Попытка забрать цену (с задержкой, чтобы Steam не забанил)
                    if idx < 10: # Ограничим первыми 10 предметами для теста
                        price = get_item_price(item.get('market_hash_name'))
                        st.markdown(f"**{price}**")
                    
                    st.markdown(f"<p style='font-size:10px;'>{name}</p>", unsafe_allow_html=True)
        else:
            st.info("Инвентарь скрыт.")
            
    except:
        st.error("Ошибка API")

st.divider()
st.caption("Удачи с Silk Song! 🐜")