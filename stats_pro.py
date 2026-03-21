import streamlit as st
import requests
import pandas as pd

# --- ТВОЙ КЛЮЧ (РЕАЛЬНЫЙ) ---
STEAM_API_KEY = "F0470B6F6D6AFBC9787C40C7507C6B58"

st.set_page_config(page_title="ANTer404 | Project", layout="wide")

if 'registered_profiles' not in st.session_state: st.session_state.registered_profiles = []
if 'is_premium' not in st.session_state: st.session_state.is_premium = False
if 'free_premiums' not in st.session_state: st.session_state.free_premiums = 5

def get_steam_id(url):
    url = url.strip().strip("/")
    if "profiles/" in url: return url.split("/")[-1]
    if "id/" in url:
        name = url.split("/")[-1]
        res = requests.get(f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={STEAM_API_KEY}&vanityurl={name}").json()
        return res.get('response', {}).get('steamid', url)
    return url

def fetch_data(sid):
    # 1. Профиль (Ник, Аватар)
    p_res = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={sid}").json()
    u = p_res['response']['players'][0]
    
    # 2. РЕАЛЬНЫЙ УРОВЕНЬ (НЕ 7, А ИЗ СТИМА)
    l_res = requests.get(f"http://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?key={STEAM_API_KEY}&steamid={sid}").json()
    level = l_res.get('response', {}).get('player_level', 0)
    
    # 3. РЕАЛЬНЫЕ ЧАСЫ И СТАТИСТИКА CS2
    s_res = requests.get(f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key={STEAM_API_KEY}&steamid={sid}").json()
    stats = {item['name']: item['value'] for item in s_res.get('playerstats', {}).get('stats', [])}
    
    # 4. РЕАЛЬНЫЙ ИНВЕНТАРЬ (ОПИСАНИЯ ПРЕДМЕТОВ)
    i_res = requests.get(f"http://api.steampowered.com/IEconService/GetInventoryItemsWithDescriptions/v1/?key={STEAM_API_KEY}&steamid={sid}&appid=730&contextid=2").json()
    inv_items = i_res.get('response', {}).get('descriptions', [])
    
    return u, level, stats, inv_items

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>CS2 Pro Analytics</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        url_input = st.text_input("Ссылка на профиль:")
        if st.button("Войти", use_container_width=True):
            try:
                sid = get_steam_id(url_input)
                u, lvl, s, inv = fetch_data(sid)
                st.session_state.update({"u": u, "lvl": lvl, "s": s, "inv": inv, "logged_in": True})
                if sid not in st.session_state.registered_profiles: st.session_state.registered_profiles.append(sid)
                st.rerun()
            except: st.error("Ошибка API: Возможно, профиль скрыт.")
else:
    u, s, lvl, inv = st.session_state.u, st.session_state.s, st.session_state.lvl, st.session_state.inv

    with st.sidebar:
        st.title("ANTer404 | Project")
        st.write(f"👤 Профилей: {len(st.session_state.registered_profiles)}")
        if st.button("Выйти"):
            st.session_state.logged_in = False
            st.rerun()
        st.divider()
        st.link_button("🚀 Telegram", "https://t.me/...")
        st.link_button("🎁 Трейд", "https://steamcommunity.com/...")
        st.link_button("💰 Донат", "https://...")

    st.title(f"👋 Привет, {u['personaname']}")
    t1, t2, t3, t4 = st.tabs(["📊 Статистика", "🎯 Battle Pass", "📦 Инвентарь", "🏆 Топ"])

    with t1:
        c1, c2 = st.columns([1, 4])
        c1.image(u['avatarfull'], width=150)
        with c2:
            st.subheader(f"🏅 Уровень Steam: {lvl}") # ТЕПЕРЬ ТУТ РЕАЛЬНЫЙ УРОВЕНЬ
            st.progress(min(lvl/100, 1.0) if lvl > 0 else 0)
            st.write(f"⌚ **Часов в CS2:** {s.get('total_time_played', 0) // 3600} ч.")

        st.divider()
        st.subheader("🔫 Мастерство оружия")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("AK-47", s.get('total_kills_ak47', 0))
        col2.metric("AWP", s.get('total_kills_awp', 0))
        col3.metric("M4A1", s.get('total_kills_m4a1', 0))
        col4.metric("Knife", s.get('total_kills_knife', 0))

    with t2:
        st.header("🎯 Квесты")
        tk = s.get('total_kills', 0)
        st.write(f"**Прогресс убийств:** {tk} / 1000")
        st.progress(min(tk/1000, 1.0))

    with t3:
        st.header("📦 Твой реальный инвентарь")
        if not inv: st.write("Инвентарь пуст или скрыт.")
        for item in inv[:10]:
            st.markdown(f"🔹 **{item['name']}**")
            st.caption(item.get('type', ''))

    with t4:
        st.header("🏆 Топ")
        st.table(pd.DataFrame({"Игрок": [u['personaname']], "Уровень": [lvl], "Убийства": [tk]}))