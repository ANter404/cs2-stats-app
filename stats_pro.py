import streamlit as st
import requests
import re
import os

# 1. Настройки
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

# 2. Константы
STEAM_API_KEY = "F0470B6F6D6AFBC9787C40C7507C6B58" 
APP_ID_CS2 = 730
USERS_DB_FILE = "unique_users.txt" # Файл со списком ID
TELEGRAM_LINK = "https://t.me/CS2devLog"

# 3. УМНЫЙ СЧЕТЧИК (Уникальные пользователи)
def get_unique_users():
    """Считывает список уникальных ID из файла"""
    if not os.path.exists(USERS_DB_FILE):
        return []
    with open(USERS_DB_FILE, "r") as f:
        # Читаем строки и убираем лишние пробелы/переносы
        return [line.strip() for line in f.readlines() if line.strip()]

def register_user(steam_id):
    """Добавляет ID в файл, если его там еще нет"""
    unique_ids = get_unique_users()
    if steam_id not in unique_ids:
        with open(USERS_DB_FILE, "a") as f:
            f.write(f"{steam_id}\n")
        return True # Новый пользователь
    return False # Уже был

# 4. Система уровней (RPG формула из v1.7.1)
def calculate_level_rpg(kills, hs):
    total_xp = (kills * 5) + (hs * 15)
    lvl, xp_needed, temp_xp = 1, 500, total_xp
    while temp_xp >= xp_needed:
        temp_xp -= xp_needed
        lvl += 1
        xp_needed = int(xp_needed * 1.2)
    progress = (temp_xp / xp_needed) * 100
    return lvl, progress, total_xp, xp_needed - int(temp_xp)

# 5. Проверка сессии через URL (чтобы не вылетало при F5)
if "user" in st.query_params and 'logged_in' not in st.session_state:
    st.session_state.steam_id = st.query_params["user"]
    st.session_state.logged_in = True

# 6. Сайдбар
with st.sidebar:
    st.title("ANTer404 | Project")
    
    # Показываем количество строк в файле = количество уникальных юзеров
    users_list = get_unique_users()
    st.metric("👤 Уникальных профилей", len(users_list))
    
    if st.session_state.get('logged_in'):
        if st.button("Выйти из системы"):
            st.query_params.clear()
            st.session_state.clear()
            st.rerun()
    
    st.divider()
    st.markdown(f"### [🚀 Наш Telegram]({TELEGRAM_LINK})")
    st.caption("v1.7.2 | Anti-Duplicate System")

# 7. Экран входа
if not st.session_state.get('logged_in'):
    st.title("📈 CS2 Pro Analytics")
    ui = st.text_input("Вставьте ваш Steam ID или ссылку:")
    if st.button("Войти"):
        ids = re.findall(r'\d{17}', ui)
        if ids:
            sid = ids[0]
            st.session_state.steam_id = sid
            st.session_state.logged_in = True
            st.query_params["user"] = sid
            
            # ПРОВЕРКА: Если зашел первый раз — запишем в базу
            register_user(sid) 
            
            st.rerun()

# 8. Основной контент (Статистика и Уровни)
else:
    sid = st.session_state.steam_id
    try:
        # Получаем данные от Steam
        summary = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={sid}").json()
        stats = requests.get(f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={APP_ID_CS2}&key={STEAM_API_KEY}&steamid={sid}").json()
        
        p = summary['response']['players'][0]
        
        col1, col2 = st.columns([1, 4])
        with col1: st.image(p['avatarfull'], width=150)
        with col2:
            st.header(p['personaname'])
            
            if 'playerstats' in stats:
                s_data = {i['name']: i['value'] for i in stats['playerstats']['stats']}
                k, hs = s_data.get('total_kills', 0), s_data.get('total_kills_headshot', 0)
                
                # УРОВНИ
                lvl, prog, txp, rem = calculate_level_rpg(k, hs)
                st.subheader(f"🎖️ RPG Уровень: {lvl}")
                st.progress(prog / 100)
                st.caption(f"Всего опыта: {txp} XP | До следующего уровня: {rem} XP")
                
                # МЕТРИКИ
                st.divider()
                m1, m2, m3 = st.columns(3)
                m1.metric("K/D Ratio", round(k/s_data.get('total_deaths', 1), 2))
                m2.metric("Headshots", hs)
                m3.metric("Total Kills", k)
            else:
                st.warning("Профиль закрыт в настройках приватности Steam.")

    except Exception as e:
        st.error(f"Steam API не отвечает. Ошибка: {e}")