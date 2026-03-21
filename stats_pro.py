import streamlit as st
import requests
import re
import os

# 1. Настройки
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

# 2. Константы
STEAM_API_KEY = "F0470B6F6D6AFBC9787C40C7507C6B58" 
APP_ID_CS2 = 730
USERS_DB_FILE = "unique_users.txt"
TELEGRAM_LINK = "https://t.me/CS2devLog"
TRADE_LINK = "https://steamcommunity.com/tradeoffer/new/?partner=789435339&token=ftuQJ9Sg"
DONATE_LINK = "https://www.donationalerts.com/r/anter404"
CONTACT_EMAIL = "cs2-pro-help@mail.ru"

# 3. Функции (База, Уровни, Цены)
def get_unique_users():
    if not os.path.exists(USERS_DB_FILE): return []
    with open(USERS_DB_FILE, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def register_user(steam_id):
    ids = get_unique_users()
    if steam_id not in ids:
        with open(USERS_DB_FILE, "a") as f: f.write(f"{steam_id}\n")

def calculate_level_rpg(kills, hs):
    total_xp = (kills * 5) + (hs * 15)
    lvl, xp_needed, temp_xp = 1, 500, total_xp
    while temp_xp >= xp_needed:
        temp_xp -= xp_needed
        lvl += 1
        xp_needed = int(xp_needed * 1.2)
    return lvl, int((temp_xp/xp_needed)*100), total_xp, xp_needed - int(temp_xp)

def get_item_price(hash_name):
    try:
        url = f"https://steamcommunity.com/market/priceoverview/?appid={APP_ID_CS2}&currency=1&market_hash_name={hash_name}"
        res = requests.get(url, timeout=5).json()
        return res.get('lowest_price', 'N/A') if res.get('success') else "N/A"
    except: return "🛠️"

# 4. Сайдбар
with st.sidebar:
    st.title("ANTer404 | Project")
    all_users = get_unique_users()
    st.metric("👤 Уникальных профилей", len(all_users))
    
    if st.session_state.get('logged_in'):
        if st.button("Выйти"):
            st.query_params.clear()
            st.session_state.clear()
            st.rerun()
    
    st.divider()
    st.markdown(f"### [🚀 Telegram]({TELEGRAM_LINK})\n### [🎁 Трейд]({TRADE_LINK})\n### [💰 Донат]({DONATE_LINK})")
    st.divider()
    support = st.checkbox("Техподдержка")
    st.caption("v1.9.0 | Tabs & Pass Update")

# 5. Вход или техподдержка
if support:
    st.header("📩 Техподдержка")
    st.markdown(f'<form action="https://formsubmit.co/{CONTACT_EMAIL}" method="POST"><input type="email" name="email" placeholder="Email" required style="width:100%; margin-bottom:10px; padding:10px; border-radius:5px;"><textarea name="message" placeholder="Вопрос" required style="width:100%; height:120px; margin-bottom:10px; padding:10px; border-radius:5px;"></textarea><button type="submit" style="background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:5px; width:100%; font-weight:bold;">Отправить</button></form>', unsafe_allow_html=True)

elif not st.session_state.get('logged_in'):
    if "user" in st.query_params:
        st.session_state.steam_id, st.session_state.logged_in = st.query_params["user"], True
        st.rerun()
    st.title("📈 CS2 Pro Analytics")
    ui = st.text_input("Steam ID:")
    if st.button("Войти"):
        ids = re.findall(r'\d{17}', ui)
        if ids:
            st.session_state.steam_id, st.session_state.logged_in = ids[0], True
            st.query_params["user"] = ids[0]
            register_user(ids[0])
            st.rerun()

# 6. Основной интерфейс (ВКЛАДКИ)
else:
    sid = st.session_state.steam_id
    try:
        # Сбор данных один раз для всех вкладок
        summary = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={sid}").json()['response']['players'][0]
        stats_res = requests.get(f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={APP_ID_CS2}&key={STEAM_API_KEY}&steamid={sid}").json()
        games_res = requests.get(f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={sid}&format=json&include_appinfo=1").json()
        
        # Хедер профиля
        st.markdown(f"### 👋 Привет, {summary['personaname']}")
        
        # Создание вкладок
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Статистика", "🎯 Battle Pass", "📦 Инвентарь", "🏆 Топ"])

        if 'playerstats' in stats_res:
            s = {i['name']: i['value'] for i in stats_res['playerstats']['stats']}
            k, hs = s.get('total_kills', 0), s.get('total_kills_headshot', 0)
            lvl, prog, txp, rem = calculate_level_rpg(k, hs)

            # --- ВКЛАДКА 1: СТАТИСТИКА ---
            with tab1:
                col1, col2 = st.columns([1, 3])
                with col1: st.image(summary['avatarfull'], width=150)
                with col2:
                    st.subheader(f"🎖️ Уровень: {lvl}")
                    st.progress(prog / 100)
                    st.caption(f"XP: {txp} | До следующего: {rem} XP")
                    all_g = games_res.get('response', {}).get('games', [])
                    cs_g = next((g for g in all_g if g['appid'] == APP_ID_CS2), None)
                    if cs_g: st.write(f"⏱️ Часов в игре: **{round(cs_g['playtime_forever']/60, 1)}**")

                st.divider()
                st.subheader("🔫 Мастерство оружия")
                w1, w2, w3, w4 = st.columns(4)
                w1.metric("AK-47", s.get('total_kills_ak47', 0))
                w2.metric("AWP", s.get('total_kills_awp', 0))
                w3.metric("M4A1", s.get('total_kills_m4a1', 0))
                w4.metric("Knife", s.get('total_kills_knife', 0))
                
                st.divider()
                m1, m2, m3 = st.columns(3)
                m1.metric("K/D", round(k/s.get('total_deaths', 1), 2))
                m2.metric("HS Count", hs)
                m3.metric("Wins", s.get('total_wins', 0))

            # --- ВКЛАДКА 2: BATTLE PASS (КВЕСТЫ) ---
            with tab2:
                st.header("🎯 Сезонные квесты")
                quests = [
                    ("Мастер стрельбы", "Набей 1000 киллов", k, 1000),
                    ("Снайпер", "Поставь 500 хэдшотов", hs, 500),
                    ("Головорез", "50 фрагов с ножа", s.get('total_kills_knife', 0), 50),
                    ("Победитель", "Выиграй 100 раундов", s.get('total_wins', 0), 100),
                    ("Гренадёр", "Убей 20 человек гранатой", s.get('total_kills_hegrenade', 0), 20)
                ]
                for name, desc, cur, goal in quests:
                    st.write(f"**{name}**: {desc}")
                    st.progress(min(cur/goal, 1.0))
                    st.caption(f"Прогресс: {cur} / {goal}")
                    st.write("")

            # --- ВКЛАДКА 3: ИНВЕНТАРЬ ---
            with tab3:
                st.header("📦 Твой инвентарь")
                inv_res = requests.get(f"https://steamcommunity.com/inventory/{sid}/{APP_ID_CS2}/2?l=russian&count=15").json()
                if inv_res and 'descriptions' in inv_res:
                    grid = st.columns(5)
                    for i, item in enumerate(inv_res['descriptions']):
                        with grid[i % 5]:
                            st.image(f"https://community.akamai.steamstatic.com/economy/image/{item['icon_url']}/100fx100f")
                            st.caption(f"💰 {get_item_price(item['market_hash_name'])}")
                            st.markdown(f"<p style='font-size:10px; color:#{item.get('name_color', 'fff')}'>{item['market_name']}</p>", unsafe_allow_html=True)
                else: st.warning("Инвентарь скрыт или пуст.")

        # --- ВКЛАДКА 4: ТОП ---
        with tab4:
            st.header("🏆 Глобальный Топ")
            leaderboard = []
            for uid in all_users:
                try:
                    res_p = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={uid}").json()['response']['players'][0]
                    res_s = requests.get(f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={APP_ID_CS2}&key={STEAM_API_KEY}&steamid={uid}").json()
                    if 'playerstats' in res_s:
                        st_dict = {i['name']: i['value'] for i in res_s['playerstats']['stats']}
                        lvl_t, _, txp_t, _ = calculate_level_rpg(st_dict.get('total_kills', 0), st_dict.get('total_kills_headshot', 0))
                        leaderboard.append({"Игрок": res_p['personaname'], "Уровень": lvl_t, "XP": txp_t})
                except: continue
            if leaderboard:
                st.table(sorted(leaderboard, key=lambda x: x['XP'], reverse=True))

    except Exception as e: st.error(f"Ошибка данных. Убедитесь, что профиль открыт. {e}")