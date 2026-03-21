import streamlit as st
import requests
import pandas as pd

# ТВОЙ РЕАЛЬНЫЙ КЛЮЧ
STEAM_API_KEY = "F0470B6F6D6AFBC9787C40C7507C6B58"

st.set_page_config(page_title="ANTer404 | Project", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'is_premium' not in st.session_state: st.session_state.is_premium = False
if 'free_premiums' not in st.session_state: st.session_state.free_premiums = 5

def get_data(sid):
    # 1. Профиль и Уровень
    p_info = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={sid}").json()['response']['players'][0]
    lvl_res = requests.get(f"http://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?key={STEAM_API_KEY}&steamid={sid}").json()
    level = lvl_res.get('response', {}).get('player_level', 0)
    
    # 2. Статистика CS2
    s_res = requests.get(f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key={STEAM_API_KEY}&steamid={sid}").json()
    stats = {s['name']: s['value'] for s in s_res.get('playerstats', {}).get('stats', [])}
    
    # 3. Реальный Инвентарь CS2
    inv_res = requests.get(f"http://api.steampowered.com/IEconService/GetInventoryItemsWithDescriptions/v1/?key={STEAM_API_KEY}&steamid={sid}&appid=730&contextid=2").json()
    items = inv_res.get('response', {}).get('descriptions', [])
    
    return p_info, level, stats, items

if not st.session_state.logged_in:
    st.title("CS2 Pro Analytics")
    url_input = st.text_input("Ссылка на профиль Steam:")
    if st.button("Войти"):
        try:
            sid = url_input.strip("/").split("/")[-1]
            u, lvl, s, inv = get_data(sid)
            st.session_state.update({"u": u, "lvl": lvl, "s": s, "inv": inv, "logged_in": True})
            st.rerun()
        except: st.error("Профиль скрыт или ошибка API")
else:
    u, s, lvl, inv = st.session_state.u, st.session_state.s, st.session_state.lvl, st.session_state.inv

    with st.sidebar:
        st.title("ANTer404 | Project")
        st.write(f"👤 **{u['personaname']}**")
        if st.button("Выйти"):
            st.session_state.logged_in = False
            st.rerun()
        st.divider()
        st.write("🚀 Telegram | 🎁 Трейд | 💰 Донат")

    st.title(f"👋 Привет, {u['personaname']}")
    t1, t2, t3, t4 = st.tabs(["📊 Статистика", "🎯 Battle Pass", "📦 Инвентарь", "🏆 Топ"])

    with t1:
        c1, c2 = st.columns([1, 4])
        c1.image(u['avatarfull'], width=150)
        with c2:
            st.subheader(f"🏅 Уровень Steam: {lvl}")
            st.progress(min(lvl / 100, 1.0))
            st.caption(f"ID: {u['steamid']}")
        
        st.divider()
        st.subheader("🔫 Мастерство оружия (Live)")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("AK-47 Kills", s.get('total_kills_ak47', 0))
        col2.metric("AWP Kills", s.get('total_kills_awp', 0))
        col3.metric("M4A1 Kills", s.get('total_kills_m4a1', 0))
        col4.metric("Knife Kills", s.get('total_kills_knife', 0))

        if not st.session_state.is_premium and st.session_state.free_premiums > 0:
            st.info(f"Акция: Осталось Premium-статусов: {st.session_state.free_premiums}")
            if st.button("Забрать Premium 💎"):
                st.session_state.is_premium = True
                st.session_state.free_premiums -= 1
                st.rerun()

    with t2:
        st.header("🎯 Сезонные квесты")
        tk = s.get('total_kills', 0)
        st.write(f"**Мастер стрельбы:** {tk} / 1000")
        st.progress(min(tk/1000, 1.0))
        
        ths = s.get('total_kills_headshot', 0)
        st.write(f"**Снайпер (HS):** {ths} / 500")
        st.progress(min(ths/500, 1.0))

    with t3:
        st.header("📦 Твой инвентарь (Live)")
        if not inv: st.write("Инвентарь пуст или скрыт.")
        for item in inv[:10]: # Показываем первые 10 предметов
            st.write(f"🔹 {item.get('name')} ({item.get('type')})")

    with t4:
        st.header("🏆 Глобальный Топ")
        prefix = "🌟" if st.session_state.is_premium else "👤"
        st.table(pd.DataFrame({"Игрок": [f"{prefix} {u['personaname']}"], "Уровень": [lvl], "Kills": [tk]}))