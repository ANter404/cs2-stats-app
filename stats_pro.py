import streamlit as st
import requests
import re
import time

# 1. Настройки страницы
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

# 2. Константы и Контакты
STEAM_API_KEY = "F0470B6F6D6AFBC9787C40C7507C6B58" 
APP_ID_CS2 = 730
TELEGRAM_LINK = "https://t.me/CS2devLog"
TRADE_LINK = "https://steamcommunity.com/tradeoffer/new/?partner=789435339&token=ftuQJ9Sg"
CONTACT_EMAIL = "cs2-pro-help@mail.ru" 

# 3. Сессии (Память входа)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'steam_id' not in st.session_state:
    st.session_state.steam_id = ""

# 4. Боковая панель
with st.sidebar:
    st.title("ANTer404 | Project")
    
    if st.session_state.logged_in:
        st.success("✅ Аккаунт привязан")
        if st.button("Выйти из системы"):
            st.session_state.logged_in = False
            st.session_state.steam_id = ""
            st.rerun()
    
    st.divider()
    st.markdown(f"### [🚀 Наш Telegram]({TELEGRAM_LINK})")
    st.markdown(f"### [🎁 Поддержать трейдом]({TRADE_LINK})")
    
    st.divider()
    st.subheader("🛠️ Техподдержка")
    support_mode = st.checkbox("Написать админу")
    
    st.divider()
    st.caption("v1.4.5 | Fixed Layout")

st.title("📈 CS2 Pro Analytics")

# 5. ЛОГИКА ТЕХПОДДЕРЖКИ
if support_mode:
    st.header("📩 Техническая поддержка")
    st.write("Нашли баг или хотите предложить идею? Заполните форму!")
    
    # Сжатый HTML без лишних пробелов в начале строк
    contact_form = f"""
<form action="https://formsubmit.co/{CONTACT_EMAIL}" method="POST" enctype="multipart/form-data">
<input type="hidden" name="_captcha" value="false">
<input type="email" name="email" placeholder="Ваша почта" required style="width:100%; margin-bottom:10px; padding:10px; border-radius:5px; border:1px solid #333; background:#262730; color:white;">
<textarea name="message" placeholder="Описание проблемы..." required style="width:100%; height:120px; margin-bottom:10px; padding:10px; border-radius:5px; border:1px solid #333; background:#262730; color:white;"></textarea>
<p style="font-size:14px; margin-bottom:5px;">Прикрепить скриншот:</p>
<input type="file" name="attachment" accept="image/*" style="margin-bottom:20px; color:white;">
<button type="submit" style="background-color:#ff4b4b; color:white; border:none; padding:12px; border-radius:5px; width:100%; font-weight:bold; cursor:pointer;">Отправить тикет</button>
</form>
"""
    st.markdown(contact_form, unsafe_allow_html=True)
    st.info(f"Запросы приходят на {CONTACT_EMAIL}")

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
            st.error("Ошибка: Вставьте корректную ссылку на профиль.")

else:
    steam_id = st.session_state.steam_id
    try:
        with st.spinner('Синхронизация...'):
            summary_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
            games_url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={steam_id}&format=json&include_appinfo=1"
            inv_url = f"https://steamcommunity.com/inventory/{steam_id}/{APP_ID_CS2}/2?l=russian&count=100&_={int(time.time())}"
            
            res_summary = requests.get(summary_url).json()
            res_games = requests.get(games_url).json()
            res_inv = requests.get(inv_url).json()
            
            player = res_summary['response']['players'][0]
            
            col1, col2 = st.columns([1, 4])
            with col1:
                st.image(player['avatarfull'], width=150)
            with col2:
                st.header(player['personaname'])
                all_games = res_games.get('response', {}).get('games', [])
                cs2_data = next((g for g in all_games if g['appid'] == APP_ID_CS2), None)
                if cs2_data:
                    hours = round(cs2_data.get('playtime_forever', 0) / 60, 1)
                    st.metric("Часов в CS2", f"{hours} ч.")
            
            st.divider()
            st.subheader("📦 Твой инвентарь")
            if res_inv and 'descriptions' in res_inv:
                items = res_inv['descriptions']
                inv_cols = st.columns(6)
                for idx, item in enumerate(items):
                    with inv_cols[idx % 6]:
                        img_hash = item.get('icon_url')
                        if img_hash:
                            st.image(f"https://community.akamai.steamstatic.com/economy/image/{img_hash}/128fx128f", width=100)
                        name = item.get('market_name')
                        color = item.get('name_color', 'FFFFFF')
                        st.markdown(f"<p style='color:#{color}; font-size:11px; font-weight:bold; line-height:1.1;'>{name}</p>", unsafe_allow_html=True)
                        if item.get('tradable') == 0:
                            st.markdown("<span style='color:#ff4b4b; font-size:10px;'>⏳ Lock</span>", unsafe_allow_html=True)
            else:
                st.info("Инвентарь пуст или скрыт.")
    except:
        st.error("Steam временно недоступен.")

st.divider()
st.caption("Developed by ANTer404 | 2026")