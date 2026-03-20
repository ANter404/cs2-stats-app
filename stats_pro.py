import streamlit as st
import requests

# ВСТАВЬ СВОЙ КЛЮЧ СЮДА (между кавычек)
STEAM_API_KEY = "F0470B6F6D6AFBC9787C40C7507C6B58"

st.set_page_config(page_title="CS2 Steam Analytics", page_icon="🎮", layout="wide")

if "steam_user" not in st.session_state:
    st.session_state["steam_user"] = None

def get_steam_user(profile_url):
    # Упрощенная логика: вытягиваем ID из ссылки
    # Ссылка может быть https://steamcommunity.com/id/nickname/ или /profiles/number
    try:
        if "profiles" in profile_url:
            steam_id = profile_url.strip("/").split("/")[-1]
        else:
            vanity_url = profile_url.strip("/").split("/")[-1]
            res = requests.get(f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={STEAM_API_KEY}&vanityurl={vanity_url}")
            steam_id = res.json()['response']['steamid']
        
        # Получаем инфу о юзере
        user_res = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}")
        return user_res.json()['response']['players'][0]
    except:
        return None

if not st.session_state["steam_user"]:
    st.title("🛡️ Вход через Steam")
    st.write("Вставь ссылку на свой профиль Steam, чтобы подтянуть реальную статистику")
    
    url = st.text_input("Ссылка на профиль", placeholder="https://steamcommunity.com/id/your_nick/")
    if st.button("Войти и синхронизировать"):
        with st.spinner("Связываемся со Steam..."):
            user_data = get_steam_user(url)
            if user_data:
                st.session_state["steam_user"] = user_data
                st.rerun()
            else:
                st.error("Не удалось найти профиль. Проверь ссылку или ключ API!")
else:
    # --- ЛИЧНЫЙ КАБИНЕТ ---
    user = st.session_state["steam_user"]
    
    st.sidebar.image(user['avatarfull'], width=150)
    st.sidebar.title(user['personaname'])
    if st.sidebar.button("Выйти"):
        st.session_state["steam_user"] = None
        st.rerun()

    st.title(f"📊 Аналитика игрока {user['personaname']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Карточка профиля")
        st.write(f"**SteamID:** {user['steamid']}")
        st.write(f"**Статус:** {'В сети' if user['personastate'] == 1 else 'Оффлайн'}")
        st.write(f"**Ссылка:** [Открыть профиль]({user['profileurl']})")
    
    with col2:
        st.info("Тут теперь будут твои реальные часы из CS2 (нужно добавить метод GetUserStats)")