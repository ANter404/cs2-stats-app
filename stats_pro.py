import streamlit as st
import requests
import re
import time

# 1. Настройки страницы
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

# 2. Константы
STEAM_API_KEY = "F0470B6F6D6AFBC9787C40C7507C6B58" 
APP_ID_CS2 = 730
TELEGRAM_LINK = "https://t.me/CS2devLog"
TRADE_LINK = "https://steamcommunity.com/tradeoffer/new/?partner=789435339&token=ftuQJ9Sg"
DONATE_PAYPAL = "https://www.donationalerts.com/r/anter404"
CONTACT_EMAIL = "cs2-pro-help@mail.ru" 

# 3. Сессии и Темы
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'steam_id' not in st.session_state:
    st.session_state.steam_id = ""

# 4. Боковая панель
with st.sidebar:
    st.title("ANTer404 | Project")
    
    if st.session_state.logged_in:
        st.success("✅ Аккаунт привязан")
        if st.button("Выйти"):
            st.session_state.logged_in = False
            st.session_state.steam_id = ""
            st.rerun()
    
    st.divider()
    
    # НОВЫЙ БЛОК: НАСТРОЙКИ
    st.subheader("⚙️ Настройки")
    theme_choice = st.radio("Выберите тему сайта:", ["Темная (Cyber)", "Светлая (Clean)"])
    
    # Логика смены темы (через кастомный CSS)
    if theme_choice == "Светлая (Clean)":
        st.markdown("""
            <style>
            .stApp { background-color: #ffffff; color: #000000; }
            section[data-testid="stSidebar"] { background-color: #f0f2f6; }
            </style>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.markdown(f"### [🚀 Telegram]({TELEGRAM_LINK})")
    st.markdown(f"### [🎁 Trade]({TRADE_LINK})")
    st.markdown(f"### [💰 Donate]({DONATE_PAYPAL})")
    
    st.divider()
    st.subheader("🛠️ Поддержка")
    support_mode = st.checkbox("Написать админу")
    
    st.caption("v1.5.0 | Stats & Themes")

st.title("📈 CS2 Pro Analytics")

# 5. ЛОГИКА ТЕХПОДДЕРЖКИ
if support_mode:
    st.header("📩 Техническая поддержка")
    contact_form = f"""
    <form action="https://formsubmit.co/{CONTACT_EMAIL}" method="POST" enctype="multipart/form-data">
    <input type="email" name="email" placeholder="Ваша почта" required style="width:100%; margin-bottom:10px; padding:10px; border-radius:5px; border:1px solid #333;">
    <textarea name="message" placeholder="Ваш вопрос..." required style="width:100%; height:120px; margin-bottom:10px; padding:10px; border-radius:5px; border:1px solid #333;"></textarea>
    <button type="submit" style="background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:5px; width:100%; font-weight:bold; cursor:pointer;">Отправить</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)

# 6. ГЛАВНЫЙ ЭКРАН
elif not st.session_state.logged_in:
    st.subheader("Добро пожаловать!")
    user_input = st.text_input("Вставьте ссылку на профиль Steam:", placeholder="https://steamcommunity.com/profiles/...")
    if st.button("Войти и сохранить"):
        found_ids = re.findall(r'\d{17}', user_input)
        if found_ids:
            st.session_state.steam_id = found_ids[0]
            st.session_state.logged_in = True
            st.rerun()

else:
    steam_id = st.session_state.steam_id
    try:
        with st.spinner('Анализируем скиллы...'):
            # Запросы
            summary_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
            stats_url = f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={APP_ID_CS2}&key={STEAM_API_KEY}&steamid={steam_id}"
            inv_url = f"https://steamcommunity.com/inventory/{steam_id}/{APP_ID_CS2}/2?l=russian&count=100&_={int(time.time())}"
            
            res_summary = requests.get(summary_url).json()
            res_stats = requests.get(stats_url).json()
            res_inv = requests.get(inv_url).json()
            
            player = res_summary['response']['players'][0]
            
            # Рендер профиля
            col1, col2 = st.columns([1, 4])
            with col1:
                st.image(player['avatarfull'], width=150)
            with col2:
                st.header(player['personaname'])
                
                # ВЫВОД СТАТИСТИКИ
                if 'playerstats' in res_stats:
                    stats = {s['name']: s['value'] for s in res_stats['playerstats']['stats']}
                    kills = stats.get('total_kills', 0)
                    deaths = stats.get('total_deaths', 0)
                    kd = round(kills / deaths, 2) if deaths > 0 else 0
                    hs = stats.get('total_kills_headshot', 0)
                    
                    s1, s2, s3 = st.columns(3)
                    s1.metric("K/D Ratio", kd)
                    s2.metric("Headshots", hs)
                    s3.metric("Total Kills", kills)
                else:
                    st.warning("⚠️ Статистика скрыта настройками приватности Steam.")

            st.divider()
            
            # Инвентарь
            st.subheader("📦 Инвентарь")
            if res_inv and 'descriptions' in res_inv:
                items = res_inv['descriptions']
                cols = st.columns(6)
                for idx, item in enumerate(items):
                    with cols[idx % 6]:
                        img_hash = item.get('icon_url')
                        if img_hash:
                            st.image(f"https://community.akamai.steamstatic.com/economy/image/{img_hash}/128fx128f", width=100)
                        st.markdown(f"<p style='color:#{item.get('name_color', 'FFFFFF')}; font-size:11px; font-weight:bold;'>{item.get('market_name')}</p>", unsafe_allow_html=True)
            else:
                st.info("Инвентарь недоступен.")
                
    except Exception as e:
        st.error(f"Ошибка: {e}")

st.divider()
st.caption("Developed by ANTer404 | 2026")