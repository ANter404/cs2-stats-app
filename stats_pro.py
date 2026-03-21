import streamlit as st
import requests
import pandas as pd

# --- ТВOЙ КЛЮЧ ---
STEAM_API_KEY = "F0470B6F6D6AFBC9787C40C7507C6B58"

st.set_page_config(page_title="ANTer404 | Project", layout="wide")

# --- ИНИЦИАЛИЗАЦИЯ (ТВОЯ СИСТЕМА УРОВНЕЙ) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'registered_profiles' not in st.session_state:
    st.session_state.registered_profiles = []
if 'is_premium' not in st.session_state:
    st.session_state.is_premium = False
if 'free_premiums' not in st.session_state:
    st.session_state.free_premiums = 5

def get_steam64(url):
    url = url.strip().strip("/")
    if "profiles/" in url: return url.split("/")[-1]
    if "id/" in url:
        name = url.split("/")[-1]
        res = requests.get(f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={STEAM_API_KEY}&vanityurl={name}").json()
        return res.get('response', {}).get('steamid', url)
    return url

def fetch_all_data(sid):
    # Данные профиля
    p_res = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={sid}").json()
    if not p_res.get('response', {}).get('players'): return None
    u = p_res['response']['players'][0]
    
    # Статистика CS2 для квестов
    s_res = requests.get(f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key={STEAM_API_KEY}&steamid={sid}").json()
    stats = {item['name']: item['value'] for item in s_res.get('playerstats', {}).get('stats', [])}
    
    # Инвентарь
    i_res = requests.get(f"http://api.steampowered.com/IEconService/GetInventoryItemsWithDescriptions/v1/?key={STEAM_API_KEY}&steamid={sid}&appid=730&contextid=2").json()
    inv = i_res.get('response', {}).get('descriptions', [])
    
    return u, stats, inv

# --- ЛОГИКА ВХОДА ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>CS2 Pro Analytics</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        url_input = st.text_input("Введите ссылку на профил Steam:", key="main_login")
        if st.button("ВОЙТИ", use_container_width=True):
            sid = get_steam64(url_input)
            data = fetch_all_data(sid)
            if data:
                st.session_state.u, st.session_state.s, st.session_state.inv = data
                st.session_state.logged_in = True
                if sid not in st.session_state.registered_profiles:
                    st.session_state.registered_profiles.append(sid)
                st.rerun()
            else:
                st.error("Ошибка API: Профиль скрыт или не найден.")

else:
    u, s, inv = st.session_state.u, st.session_state.s, st.session_state.inv
    
    # --- ТВОЯ МЕХАНИКА УРОВНЯ (РАСЧЕТ ИЗ КВЕСТОВ) ---
    kills = s.get('total_kills', 0)
    hs = s.get('total_kills_headshot', 0)
    # Пример логики: 1 килл = 10 XP, 1 HS = 20 XP
    total_xp = (kills * 10) + (hs * 20)
    current_level = (total_xp // 5000) + 1 # Каждые 5000 XP новый уровень
    xp_on_level = total_xp % 5000

    # --- САЙДБАР ---
    with st.sidebar:
        st.title("ANTer404 | Project")
        st.write(f"👤 Профилей в базе: **{len(st.session_state.registered_profiles)}**")
        if st.button("Выйти"):
            st.session_state.logged_in = False
            st.rerun()
        st.divider()
        st.link_button("🚀 Telegram", "https://t.me/...", use_container_width=True)
        st.link_button("🎁 Трейд-ссылка", "https://steamcommunity.com/...", use_container_width=True)
        st.link_button("💰 Донат", "https://...", use_container_width=True)
        st.divider()
        st.caption("v1.9.0 | Custom XP System")

    # --- КОНТЕНТ ---
    st.title(f"👋 Привет, {u['personaname']}")
    tabs = st.tabs(["📊 Статистика", "🎯 Battle Pass", "📦 Инвентарь", "🏆 Топ"])

    with tabs[0]:
        c1, c2 = st.columns([1, 4])
        c1.image(u['avatarfull'], width=150)
        with c2:
            st.subheader(f"🏅 Ваш Уровень: {current_level}")
            st.progress(min(xp_on_level / 5000, 1.0))
            st.caption(f"XP: {xp_on_level} / 5000 до следующего уровня")
            st.write(f"⌚ **Часов в CS2:** {s.get('total_time_played', 0) // 3600} ч.")

        st.divider()
        st.subheader("🔫 Мастерство оружия")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("AK-47", s.get('total_kills_ak47', 0))
        m2.metric("AWP", s.get('total_kills_awp', 0))
        m3.metric("M4A1", s.get('total_kills_m4a1', 0))
        m4.metric("Knife", s.get('total_kills_knife', 0))

        if not st.session_state.is_premium and st.session_state.free_premiums > 0:
            st.info(f"Акция: Доступно Premium-статусов: {st.session_state.free_premiums}")
            if st.button("Забрать Premium 💎"):
                st.session_state.is_premium = True
                st.session_state.free_premiums -= 1
                st.rerun()

    with tabs[1]:
        st.header("🎯 Квесты и Опыт")
        st.write(f"**Мастер стрельбы:** Набей 1000 киллов")
        st.progress(min(kills/1000, 1.0))
        st.caption(f"Прогресс: {kills} / 1000 (+XP)")
        
        st.write(f"**Снайпер:** Поставь 500 хэдшотов")
        st.progress(min(hs/500, 1.0))
        st.caption(f"Прогресс: {hs} / 500 (+XP)")

    with tabs[2]:
        st.header("📦 Инвентарь")
        if not inv: st.write("Скрыт или пуст.")
        for item in inv[:10]:
            st.markdown(f"🔹 **{item['name']}**")
            st.divider()

    with tabs[3]:
        st.header("🏆 Топ игроков")
        prefix = "🌟" if st.session_state.is_premium else "👤"
        st.table(pd.DataFrame({
            "Игрок": [f"{prefix} {u['personaname']}", "System_Admin"],
            "Уровень сайта": [current_level, 99],
            "Всего XP": [total_xp, 1000000]
        }))