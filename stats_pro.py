import streamlit as st
import requests

# Твой ключ вшит навсегда
STEAM_API_KEY = "F0470B6F6D6AFBC9787C40C7507C6B58"

st.set_page_config(page_title="ANTer404 CS2 Stats", page_icon="📊", layout="wide")

# Проверка сессии
if "steam_user" not in st.session_state:
    st.session_state["steam_user"] = None

def get_steam_data(profile_url):
    try:
        # 1. Получаем SteamID из ссылки
        if "profiles" in profile_url:
            sid = profile_url.strip("/").split("/")[-1]
        else:
            v_url = profile_url.strip("/").split("/")[-1]
            res = requests.get(f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={STEAM_API_KEY}&vanityurl={v_url}").json()
            sid = res['response']['steamid']
        
        # 2. Инфо о профиле (Аватар, Ник)
        user = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={sid}").json()['response']['players'][0]
        
        # 3. Инфо об играх (Ищем CS2 - AppID 730)
        games_url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={sid}&format=json&include_appinfo=1"
        games = requests.get(games_url).json()
        
        cs2_info = None
        if 'games' in games['response']:
            cs2_info = next((g for g in games['response']['games'] if g['appid'] == 730), None)
            
        return user, cs2_info
    except Exception as e:
        return None, None

# --- ИНТЕРФЕЙС ---
if not st.session_state["steam_user"]:
    st.title("🎮 Вход в ANTer404 Analytics")
    st.subheader("Авторизация через Steam")
    
    url = st.text_input("Вставь ссылку на профиль Steam:", placeholder="https://steamcommunity.com/id/your_nick/")
    
    if st.button("Синхронизировать данные", use_container_width=True):
        with st.spinner("Связываемся со Steam..."):
            u, g = get_steam_data(url)
            if u:
                st.session_state["steam_user"] = u
                st.session_state["cs2_data"] = g
                st.rerun()
            else:
                st.error("Ошибка! Проверь ссылку или настройки приватности профиля.")
else:
    u = st.session_state["steam_user"]
    g = st.session_state["cs2_data"]
    
    # Боковая панель
    st.sidebar.image(u['avatarfull'], width=200)
    st.sidebar.title(u['personaname'])
    st.sidebar.write(f"ID: `{u['steamid']}`")
    
    if st.sidebar.button("Выйти из системы"):
        st.session_state["steam_user"] = None
        st.rerun()

    # Основной экран
    st.title(f"🚀 Дашборд игрока: {u['personaname']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("📊 Статистика аккаунта")
        st.write(f"**Страна:** {u.get('loccountrycode', 'Скрыто')}")
        st.write(f"**Профиль:** [Открыть в Steam]({u['profileurl']})")
        if 'timecreated' in u:
            import datetime
            date = datetime.datetime.fromtimestamp(u['timecreated']).year
            st.write(f"**Аккаунт создан:** {date} г.")

    with col2:
        st.success("🔫 Данные Counter-Strike 2")
        if g:
            hours = round(g['playtime_forever'] / 60, 1)
            st.metric("Общее время в игре", f"{hours} ч.")
            
            if 'playtime_2weeks' in g:
                two_weeks = round(g['playtime_2weeks'] / 60, 1)
                st.write(f"🔥 Активность за 14 дней: **{two_weeks} ч.**")
            else:
                st.write("Последние 2 недели не играл.")
        else:
            st.warning("⚠️ Не удалось получить время игры. Сделай 'Игровую информацию' открытой в настройках Steam.")

    st.divider()
    st.subheader("📈 Твои достижения")
    st.write("Скоро здесь будет детальный разбор твоих медалей и ачивок!")