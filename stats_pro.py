import streamlit as st
import requests
import pandas as pd

# --- ТВOЙ КЛЮЧ И НАСТРОЙКИ ---
STEAM_API_KEY = "F0470B6F6D6AFBC9787C40C7507C6B58"

st.set_page_config(page_title="ANTer404 | Project", layout="wide")

# --- ГЛОБАЛЬНАЯ БАЗА (ЧТОБЫ НЕ ТЕРЯТЬ АККАУНТЫ) ---
if 'registered_profiles' not in st.session_state:
    st.session_state.registered_profiles = [] # Список всех зашедших
if 'is_premium' not in st.session_state:
    st.session_state.is_premium = False
if 'free_premiums' not in st.session_state:
    st.session_state.free_premiums = 5

# --- ФУНКЦИИ STEAM API ---
def get_steam64(url):
    if "profiles/" in url: return url.strip("/").split("/")[-1]
    if "id/" in url:
        name = url.strip("/").split("/")[-1]
        res = requests.get(f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={STEAM_API_KEY}&vanityurl={name}").json()
        return res.get('response', {}).get('steamid', url)
    return url

def fetch_all_data(sid):
    # Профиль
    p_res = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={sid}").json()
    u = p_res['response']['players'][0]
    # Уровень
    l_res = requests.get(f"http://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?key={STEAM_API_KEY}&steamid={sid}").json()
    lvl = l_res.get('response', {}).get('player_level', 0)
    # Статистика CS2
    s_res = requests.get(f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key={STEAM_API_KEY}&steamid={sid}").json()
    stats = {item['name']: item['value'] for item in s_res.get('playerstats', {}).get('stats', [])}
    # Инвентарь
    i_res = requests.get(f"http://api.steampowered.com/IEconService/GetInventoryItemsWithDescriptions/v1/?key={STEAM_API_KEY}&steamid={sid}&appid=730&contextid=2").json()
    inv = i_res.get('response', {}).get('descriptions', [])
    return u, lvl, stats, inv

# --- ЛОГИКА ВХОДА ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>CS2 Pro Analytics</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        url_input = st.text_input("Введите ссылку на профиль Steam:")
        if st.button("Войти"):
            try:
                sid = get_steam64(url_input)
                u, lvl, s, inv = fetch_all_data(sid)
                st.session_state.update({"u": u, "s": s, "lvl": lvl, "inv": inv, "logged_in": True})
                # Добавляем в список уникальных профилей
                if sid not in st.session_state.registered_profiles:
                    st.session_state.registered_profiles.append(sid)
                st.rerun()
            except: st.error("Ошибка! Проверьте ссылку или API ключ.")

else:
    u, s, lvl, inv = st.session_state.u, st.session_state.s, st.session_state.lvl, st.session_state.inv

    # --- САЙДБАР (КАК НА СКРИНАХ) ---
    with st.sidebar:
        st.title("ANTer404 | Project")
        st.write(f"👤 Уникальных профилей: **{len(st.session_state.registered_profiles)}**")
        
        if st.button("Выйти / Сменить аккаунт"):
            st.session_state.logged_in = False
            st.rerun()
        
        st.divider()
        # РЕАЛЬНЫЕ ССЫЛКИ
        st.link_button("🚀 Telegram", "https://t.me/your_channel")
        st.link_button("🎁 Трейд-ссылка", "https://steamcommunity.com/tradeoffer/new/...")
        st.link_button("💰 Донат", "https://donationalerts.com/...")
        
        st.divider()
        st.checkbox("Техподдержка", value=True)
        st.caption("v1.9.0 | Full API Sync")

    # --- КОНТЕНТ ---
    st.title(f"👋 Привет, {u['personaname']}")
    
    tabs = st.tabs(["📊 Статистика", "🎯 Battle Pass", "📦 Инвентарь", "🏆 Топ"])

    with tabs[0]:
        c1, c2 = st.columns([1, 4])
        c1.image(u['avatarfull'], width=150)
        with c2:
            st.subheader(f"🏅 Уровень Steam: {lvl}")
            st.progress(min(lvl/100, 1.0))
            st.write(f"**SteamID:** {u['steamid']}")
        
        st.divider()
        st.subheader("🔫 Мастерство оружия")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("AK-47", s.get('total_kills_ak47', 0))
        col2.metric("AWP", s.get('total_kills_awp', 0))
        col3.metric("M4A1", s.get('total_kills_m4a1', 0))
        col4.metric("Knife", s.get('total_kills_knife', 0))

        if not st.session_state.is_premium and st.session_state.free_premiums > 0:
            st.warning(f"Осталось бесплатных Premium: {st.session_state.free_premiums}")
            if st.button("Получить Premium 💎"):
                st.session_state.is_premium = True
                st.session_state.free_premiums -= 1
                st.rerun()

    with tabs[1]:
        st.header("🎯 Сезонные квесты")
        tk = s.get('total_kills', 0)
        st.write(f"**Мастер стрельбы:** {tk} / 1000")
        st.progress(min(tk/1000, 1.0))
        
        ths = s.get('total_kills_headshot', 0)
        st.write(f"**Снайпер:** {ths} / 500")
        st.progress(min(ths/500, 1.0))

    with tabs[2]:
        st.header("📦 Твой инвентарь (Live)")
        if not inv:
            st.write("Инвентарь пуст или скрыт настройками приватности Steam.")
        else:
            for item in inv[:15]:
                with st.expander(f"🔹 {item['name']}"):
                    st.write(f"Тип: {item['type']}")
                    st.write(f"Описание: {item.get('descriptions', [{'value': 'Нет описания'}])[0]['value']}")

    with tabs[3]:
        st.header("🏆 Глобальный Топ")
        # Показываем текущего юзера и список всех, кто заходил
        prefix = "🌟" if st.session_state.is_premium else "👤"
        df = pd.DataFrame({
            "Игрок": [f"{prefix} {u['personaname']}"],
            "Уровень": [lvl],
            "XP (Kills)": [tk]
        })
        st.table(df)