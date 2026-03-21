import streamlit as st
import requests
import re
import os

# 1. Настройки
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

# 2. Константы
STEAM_API_KEY = "F0470B6F6D6AFBC9787C40C7507C6B58" 
APP_ID_CS2 = 730
COUNTER_FILE = "user_count.txt"
TELEGRAM_LINK = "https://t.me/CS2devLog"
TRADE_LINK = "https://steamcommunity.com/tradeoffer/new/?partner=789435339&token=ftuQJ9Sg"
DONATE_LINK = "https://www.donationalerts.com/r/anter404"
CONTACT_EMAIL = "cs2-pro-help@mail.ru" 

# 3. Функции логики
def get_user_count():
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f: f.write("0")
    with open(COUNTER_FILE, "r") as f: return int(f.read())

def increment_user_count():
    count = get_user_count() + 1
    with open(COUNTER_FILE, "w") as f: f.write(str(count))

def get_item_price(hash_name):
    try:
        url = f"https://steamcommunity.com/market/priceoverview/?appid={APP_ID_CS2}&currency=1&market_hash_name={hash_name}"
        res = requests.get(url, timeout=5).json()
        return res.get('lowest_price', 'N/A') if res.get('success') else "N/A"
    except: return "🛠️"

# НОВАЯ ПРОГРЕССИВНАЯ СИСТЕМА УРОВНЕЙ
def calculate_level_v2(kills, hs):
    total_xp = (kills * 5) + (hs * 15) # Уменьшили награду за килл до 5 XP
    
    # Уровни по формуле: 500 * (1.2 ^ уровень)
    lvl = 1
    xp_needed = 500
    temp_xp = total_xp
    
    while temp_xp >= xp_needed:
        temp_xp -= xp_needed
        lvl += 1
        xp_needed = int(xp_needed * 1.2) # С каждым уровнем нужно на 20% больше
        
    progress = (temp_xp / xp_needed) * 100
    return lvl, progress, total_xp, xp_needed - int(temp_xp)

# 4. Проверка сессии
if "user" in st.query_params and 'logged_in' not in st.session_state:
    st.session_state.steam_id = st.query_params["user"]
    st.session_state.logged_in = True

# 5. Сайдбар
with st.sidebar:
    st.title("ANTer404 | Project")
    st.metric("👤 Пользователей", get_user_count())
    if st.session_state.get('logged_in'):
        if st.button("Выйти"):
            st.query_params.clear()
            st.session_state.clear()
            st.rerun()
    st.divider()
    theme = st.radio("Тема:", ["Темная", "Светлая"])
    st.markdown(f"### [🚀 Telegram]({TELEGRAM_LINK})\n### [🎁 Trade]({TRADE_LINK})\n### [💰 Donate]({DONATE_LINK})")
    
    support = st.checkbox("Написать админу")
    st.caption("v1.7.1 | Balanced Levels")

# 6. Основная логика
if support:
    st.header("📩 Техподдержка")
    st.markdown(f'<form action="https://formsubmit.co/{CONTACT_EMAIL}" method="POST"> <input type="email" name="email" placeholder="Email" required style="width:100%; margin-bottom:10px; padding:10px; border-radius:5px;"> <textarea name="message" placeholder="Сообщение" required style="width:100%; height:120px; margin-bottom:10px; padding:10px; border-radius:5px;"></textarea> <button type="submit" style="background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:5px; width:100%; font-weight:bold;">Отправить</button> </form>', unsafe_allow_html=True)

elif not st.session_state.get('logged_in'):
    st.title("📈 CS2 Pro Analytics")
    ui = st.text_input("Steam ID или ссылка:")
    if st.button("Войти"):
        ids = re.findall(r'\d{17}', ui)
        if ids:
            st.session_state.steam_id, st.session_state.logged_in = ids[0], True
            st.query_params["user"] = ids[0]
            increment_user_count()
            st.rerun()
else:
    sid = st.session_state.steam_id
    try:
        # API запросы
        sum_res = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={sid}").json()
        stat_res = requests.get(f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={APP_ID_CS2}&key={STEAM_API_KEY}&steamid={sid}").json()
        game_res = requests.get(f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={sid}&format=json&include_appinfo=1").json()
        inv_res = requests.get(f"https://steamcommunity.com/inventory/{sid}/{APP_ID_CS2}/2?l=russian&count=10").json()
        
        p = sum_res['response']['players'][0]
        
        col1, col2 = st.columns([1, 4])
        with col1: st.image(p['avatarfull'], width=150)
        with col2:
            st.header(p['personaname'])
            # Часы
            games = game_res.get('response', {}).get('games', [])
            cs_g = next((g for g in games if g['appid'] == APP_ID_CS2), None)
            if cs_g: st.write(f"🎮 Часов: **{round(cs_g['playtime_forever']/60, 1)}**")
            
            # Уровни
            if 'playerstats' in stat_res:
                s = {i['name']: i['value'] for i in stat_res['playerstats']['stats']}
                k, hs = s.get('total_kills', 0), s.get('total_kills_headshot', 0)
                lvl, prog, txp, remain = calculate_level_v2(k, hs)
                
                st.subheader(f"🎖️ Уровень: {lvl}")
                st.progress(prog / 100)
                st.caption(f"XP: {txp} | До следующего уровня: {remain} XP")
                
                st.divider()
                # Стата
                m1, m2, m3 = st.columns(3)
                m1.metric("K/D", round(k/s.get('total_deaths', 1), 2))
                m2.metric("HS", hs)
                m3.metric("Kills", k)
        
        st.divider()
        st.subheader("📦 Инвентарь и цены")
        if inv_res and 'descriptions' in inv_res:
            grid = st.columns(5)
            for i, item in enumerate(inv_res['descriptions']):
                with grid[i % 5]:
                    st.image(f"https://community.akamai.steamstatic.com/economy/image/{item['icon_url']}/100fx100f")
                    st.caption(f"💰 {get_item_price(item['market_hash_name'])}")
                    st.markdown(f"<p style='font-size:10px; color:#{item.get('name_color', 'fff')}'>{item['market_name']}</p>", unsafe_allow_html=True)

    except: st.error("Steam API Error")