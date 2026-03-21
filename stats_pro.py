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

# 3. Логика уровней и данных
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
    return lvl, int((temp_xp/xp_needed)*100), total_xp

# 4. Сайдбар
with st.sidebar:
    st.title("ANTer404 | Project")
    all_users = get_unique_users()
    st.metric("👤 Уникальных профилей", len(all_users))
    
    page = st.radio("Навигация:", ["Мой профиль", "🏆 Таблица лидеров"])
    
    if st.session_state.get('logged_in'):
        if st.button("Выйти"):
            st.query_params.clear()
            st.session_state.clear()
            st.rerun()
    st.divider()
    st.caption("v1.8.0 | Hall of Fame Update")

# 5. ТАБЛИЦА ЛИДЕРОВ
if page == "🏆 Таблица лидеров":
    st.title("🏆 Глобальный топ игроков")
    leaderboard = []
    
    with st.spinner("Загрузка топа..."):
        for uid in all_users:
            try:
                s_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={uid}"
                st_url = f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={APP_ID_CS2}&key={STEAM_API_KEY}&steamid={uid}"
                
                p_data = requests.get(s_url).json()['response']['players'][0]
                res_st = requests.get(st_url).json()
                
                if 'playerstats' in res_st:
                    s = {i['name']: i['value'] for i in res_st['playerstats']['stats']}
                    lvl, _, txp = calculate_level_rpg(s.get('total_kills', 0), s.get('total_kills_headshot', 0))
                    leaderboard.append({
                        "Игрок": p_data['personaname'],
                        "Уровень": lvl,
                        "Всего XP": txp,
                        "K/D": round(s.get('total_kills', 0)/s.get('total_deaths', 1), 2)
                    })
            except: continue
            
    if leaderboard:
        # Сортировка по XP
        leaderboard = sorted(leaderboard, key=lambda x: x['Всего XP'], reverse=True)
        st.table(leaderboard)
    else:
        st.info("Лидеров пока нет.")

# 6. МОЙ ПРОФИЛЬ (Основная логика)
elif page == "Мой профиль":
    if "user" in st.query_params and 'logged_in' not in st.session_state:
        st.session_state.steam_id, st.session_state.logged_in = st.query_params["user"], True

    if not st.session_state.get('logged_in'):
        st.title("📈 CS2 Pro Analytics")
        ui = st.text_input("Вставьте Steam ID:")
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
            # Сбор данных
            summary = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={sid}").json()['response']['players'][0]
            stats_res = requests.get(f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={APP_ID_CS2}&key={STEAM_API_KEY}&steamid={sid}").json()
            games_res = requests.get(f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={sid}&format=json&include_appinfo=1").json()

            col1, col2 = st.columns([1, 4])
            with col1: st.image(summary['avatarfull'], width=150)
            with col2:
                st.header(summary['personaname'])
                
                # ЧАСЫ
                all_g = games_res.get('response', {}).get('games', [])
                cs_g = next((g for g in all_g if g['appid'] == APP_ID_CS2), None)
                if cs_g: st.write(f"⏱️ Наиграно: **{round(cs_g['playtime_forever']/60, 1)} ч.**")
                
                if 'playerstats' in stats_res:
                    s = {i['name']: i['value'] for i in stats_res['playerstats']['stats']}
                    k, hs = s.get('total_kills', 0), s.get('total_kills_headshot', 0)
                    lvl, prog, txp = calculate_level_rpg(k, hs)
                    
                    st.subheader(f"🎖️ Уровень: {lvl}")
                    st.progress(prog / 100)
                    
                    st.divider()
                    # ДЕТАЛИЗАЦИЯ ОРУЖИЯ (НОВОЕ)
                    st.subheader("🔫 Топ оружия")
                    w_col1, w_col2, w_col3 = st.columns(3)
                    w_col1.metric("AK-47", s.get('total_kills_ak47', 0))
                    w_col2.metric("AWP", s.get('total_kills_awp', 0))
                    w_col3.metric("M4A1", s.get('total_kills_m4a1', 0))
                    
                    st.divider()
                    m1, m2, m3 = st.columns(3)
                    m1.metric("K/D", round(k/s.get('total_deaths', 1), 2))
                    m2.metric("HS", hs)
                    m3.metric("Total Kills", k)
        except: st.error("Ошибка загрузки данных профиля.")