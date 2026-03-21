import streamlit as st
import requests
import re
import os

# 1. Настройки и URL-память
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

# 2. Константы
STEAM_API_KEY = "F0470B6F6D6AFBC9787C40C7507C6B58" 
APP_ID_CS2 = 730
COUNTER_FILE = "user_count.txt"

# 3. Функции логики
def get_user_count():
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f: f.write("0")
    with open(COUNTER_FILE, "r") as f: return int(f.read())

def increment_user_count():
    count = get_user_count() + 1
    with open(COUNTER_FILE, "w") as f: f.write(str(count))

# Расчет уровня
def calculate_level(kills, hs):
    xp = (kills * 10) + (hs * 25) # За убийство 10 XP, за хэдшот +25 XP
    level = int(xp / 1000) + 1 # Каждые 1000 XP — новый уровень
    progress = (xp % 1000) / 10 # Процент до следующего уровня
    return level, progress, xp

# 4. Проверка сессии через URL
if "user" in st.query_params and 'logged_in' not in st.session_state:
    st.session_state.steam_id = st.query_params["user"]
    st.session_state.logged_in = True

# 5. Сайдбар
with st.sidebar:
    st.title("ANTer404 | Project")
    st.metric("👤 Всего в системе", get_user_count())
    if st.session_state.get('logged_in'):
        if st.button("Выйти"):
            st.query_params.clear()
            st.session_state.clear()
            st.rerun()
    st.divider()
    theme = st.radio("Тема:", ["Темная", "Светлая"])
    st.caption("v1.7.0 | Battle Pass Update")

# 6. Экран входа
if not st.session_state.get('logged_in'):
    st.title("📈 CS2 Pro Analytics")
    user_input = st.text_input("Вставьте ссылку на Steam для входа:")
    if st.button("Войти и начать прокачку"):
        found = re.findall(r'\d{17}', user_input)
        if found:
            sid = found[0]
            st.session_state.steam_id = sid
            st.session_state.logged_in = True
            st.query_params["user"] = sid
            increment_user_count()
            st.rerun()

# 7. Личный кабинет с Уровнями
else:
    steam_id = st.session_state.steam_id
    try:
        # Загрузка данных
        summary = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}").json()
        stats_res = requests.get(f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={APP_ID_CS2}&key={STEAM_API_KEY}&steamid={steam_id}").json()
        
        player = summary['response']['players'][0]
        
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(player['avatarfull'], width=150)
        with col2:
            st.header(f"Боец: {player['personaname']}")
            
            if 'playerstats' in stats_res:
                s = {i['name']: i['value'] for i in stats_res['playerstats']['stats']}
                kills = s.get('total_kills', 0)
                hs = s.get('total_kills_headshot', 0)
                
                # РАСЧЕТ УРОВНЯ
                lvl, prog, total_xp = calculate_level(kills, hs)
                
                st.subheader(f"🎖️ Уровень: {lvl}")
                st.progress(prog / 100)
                st.caption(f"Всего XP: {total_xp} | До уровня {lvl+1} осталось {100 - int(prog)}%")

                st.divider()
                
                # ЗАДАНИЯ (КВЕСТЫ)
                st.markdown("### 🎯 Текущие квесты")
                q1_target = 1000
                q2_target = 500
                
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Мастер стрельбы:** Набей {q1_target} киллов")
                    st.progress(min(kills/q1_target, 1.0))
                    st.write(f"{kills} / {q1_target}")
                
                with c2:
                    st.write(f"**Снайпер:** Поставь {q2_target} хэдшотов")
                    st.progress(min(hs/q2_target, 1.0))
                    st.write(f"{hs} / {q2_target}")

            else:
                st.warning("⚠️ Открой статку в Steam, чтобы качать уровень!")

    except Exception as e:
        st.error(f"Ошибка API: {e}")