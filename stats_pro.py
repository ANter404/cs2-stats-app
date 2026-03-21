import streamlit as st
import requests
import re
import os

# 1. Настройки страницы
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

# 2. Константы
STEAM_API_KEY = "F0470B6F6D6AFBC9787C40C7507C6B58" 
APP_ID_CS2 = 730
USERS_DB_FILE = "unique_users.txt"
TELEGRAM_LINK = "https://t.me/CS2devLog"
TRADE_LINK = "https://steamcommunity.com/tradeoffer/new/?partner=789435339&token=ftuQJ9Sg"
DONATE_LINK = "https://www.donationalerts.com/r/anter404"
CONTACT_EMAIL = "cs2-pro-help@mail.ru"

# 3. Функции данных
def get_unique_users():
    if not os.path.exists(USERS_DB_FILE): return []
    with open(USERS_DB_FILE, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def register_user(steam_id):
    ids = get_unique_users()
    if steam_id not in ids:
        with open(USERS_DB_FILE, "a") as f: f.write(f"{steam_id}\n")

def get_item_price(hash_name):
    try:
        url = f"https://steamcommunity.com/market/priceoverview/?appid={APP_ID_CS2}&currency=1&market_hash_name={hash_name}"
        res = requests.get(url, timeout=5).json()
        return res.get('lowest_price', 'N/A') if res.get('success') else "N/A"
    except: return "🛠️"

def calculate_level_rpg(kills, hs):
    total_xp = (kills * 5) + (hs * 15)
    lvl, xp_needed, temp_xp = 1, 500, total_xp
    while temp_xp >= xp_needed:
        temp_xp -= xp_needed
        lvl += 1
        xp_needed = int(xp_needed * 1.2)
    progress = (temp_xp / xp_needed) * 100
    return lvl, progress, total_xp, xp_needed - int(temp_xp)

# 4. Проверка сессии (URL Memory)
if "user" in st.query_params and 'logged_in' not in st.session_state:
    st.session_state.steam_id = st.query_params["user"]
    st.session_state.logged_in = True

# 5. Сайдбар
with st.sidebar:
    st.title("ANTer404 | Project")
    st.metric("👤 Уникальных профилей", len(get_unique_users()))
    
    if st.session_state.get('logged_in'):
        if st.button("Выйти"):
            st.query_params.clear()
            st.session_state.clear()
            st.rerun()
    
    st.divider()
    theme = st.radio("Тема:", ["Темная", "Светлая"])
    if theme == "Светлая":
        st.markdown("<style>.stApp { background-color: white; color: black; } h1,h2,h3,p,span { color: black !important; }</style>", unsafe_allow_html=True)
    
    st.markdown(f"### [🚀 Telegram]({TELEGRAM_LINK})\n### [🎁 Трейд]({TRADE_LINK})\n### [💰 Донат]({DONATE_LINK})")
    
    support = st.checkbox("Техподдержка")
    st.caption("v1.7.3 | Ultimate Stable Edition")

# 6. Основная логика
if support:
    st.header("📩 Техподдержка")
    st.markdown(f'<form action="https://formsubmit.co/{CONTACT_EMAIL}" method="POST"><input type="email" name="email" placeholder="Твоя почта" required style="width:100%; margin-bottom:10px; padding:10px; border-radius:5px;"><textarea name="message" placeholder="Твой вопрос" required style="width:100%; height:120px; margin-bottom:10px; padding:10px; border-radius:5px;"></textarea><button type="submit" style="background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:5px; width:100%; font-weight:bold;">Отправить</button></form>', unsafe_allow_html=True)

elif not st.session_state.get('logged_in'):
    st.title("📈 CS2 Pro Analytics")
    ui = st.text_input("Вставьте Steam ID или ссылку:")
    if st.button("Войти"):
        ids = re.findall(r'\d{17}', ui)
        if ids:
            sid = ids[0]
            st.session_state.steam_id, st.session_state.logged_in = sid, True
            st.query_params["user"] = sid
            register_user(sid)
            st.rerun()
else:
    sid = st.session_state.steam_id
    try:
        # Получение данных
        summary = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={sid}").json()
        stats = requests.get(f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={APP_ID_CS2}&key={STEAM_API_KEY}&steamid={sid}").json()
        games = requests.get(f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={sid}&format=json&include_appinfo=1").json()
        inv = requests.get(f"https://steamcommunity.com/inventory/{sid}/{APP_ID_CS2}/2?l=russian&count=10").json()
        
        p = summary['response']['players'][0]
        
        col1, col2 = st.columns([1, 4])
        with col1: st.image(p['avatarfull'], width=150)
        with col2:
            st.header(p['personaname'])
            # ЧАСЫ (ВЕРНУЛИ)
            all_g = games.get('response', {}).get('games', [])
            cs_g = next((g for g in all_g if g['appid'] == APP_ID_CS2), None)
            if cs_g: st.subheader(f"⏱️ Наиграно: {round(cs_g['playtime_forever']/60, 1)} ч.")
            
            # УРОВНИ И КВЕСТЫ (ВЕРНУЛИ)
            if 'playerstats' in stats:
                s = {i['name']: i['value'] for i in stats['playerstats']['stats']}
                k, hs = s.get('total_kills', 0), s.get('total_kills_headshot', 0)
                lvl, prog, txp, rem = calculate_level_rpg(k, hs)
                
                st.markdown(f"### 🎖️ Уровень: {lvl}")
                st.progress(prog / 100)
                st.caption(f"XP: {txp} | До следующего: {rem} XP")
                
                st.divider()
                st.markdown("### 🎯 Квесты")
                q1, q2 = 1000, 500
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"Килы: {k}/{q1}")
                    st.progress(min(k/q1, 1.0))
                with c2:
                    st.write(f"Хэдшоты: {hs}/{q2}")
                    st.progress(min(hs/q2, 1.0))
                
                st.divider()
                m1, m2, m3 = st.columns(3)
                m1.metric("K/D", round(k/s.get('total_deaths', 1), 2))
                m2.metric("HS", hs)
                m3.metric("Kills", k)

        # ИНВЕНТАРЬ (ВЕРНУЛИ)
        st.divider()
        st.subheader("📦 Инвентарь и цены")
        if inv and 'descriptions' in inv:
            grid = st.columns(5)
            for i, item in enumerate(inv['descriptions']):
                with grid[i % 5]:
                    st.image(f"https://community.akamai.steamstatic.com/economy/image/{item['icon_url']}/100fx100f")
                    st.caption(f"💰 {get_item_price(item['market_hash_name'])}")
                    st.markdown(f"<p style='font-size:10px; color:#{item.get('name_color', 'fff')}'>{item['market_name']}</p>", unsafe_allow_html=True)
    except: st.error("Ошибка API")