import streamlit as st
import requests

# Настройки страницы
st.set_page_config(page_title="CS2 Pro Analytics", page_icon="📈", layout="wide")

# КОНФИГУРАЦИЯ
STEAM_API_KEY = "80562D785863D2DB396C004F7547514D" 
TELEGRAM_LINK = "https://t.me/CS2devLog"
DONATE_LINK = "https://www.donationalerts.com/r/anter404"

# Кастомный стиль боковой панели
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #1a1c24;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_index=True)

# Боковая панель (Sidebar)
with st.sidebar:
    st.image("https://avatars.akamai.steamstatic.com/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb_full.jpg", width=100)
    st.title("ANTer404 | Project")
    st.info(f"**Версия:** 1.1 (Beta)\n\n**Статус:** Разработка (День 2)")
    
    st.markdown("### 🔗 Ресурсы")
    st.markdown(f"[![Telegram](https://img.shields.io/badge/Telegram-Канал-blue?style=for-the-badge&logo=telegram)]({TELEGRAM_LINK})")
    st.write("")
    st.markdown(f"[![Donate](https://img.shields.io/badge/Поддержать-Разработку-orange?style=for-the-badge&logo=donationalerts)]({DONATE_LINK})")
    
    st.divider()
    st.caption("© 2026 ANTer404 Development")

# Основной интерфейс
st.title("📈 CS2 Pro Analytics")
st.subheader("Система анализа и статистики профилей Steam")

# Ввод Steam ID
steam_input = st.text_input("Введите Steam ID 64 (например, 7656119...):", placeholder="7656119...")

if steam_input:
    # 1. Получаем данные профиля через API
    url_profile = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_input}"
    
    try:
        res = requests.get(url_profile).json()
        
        if res['response']['players']:
            player = res['response']['players'][0]
            col1, col2 = st.columns([1, 4])
            
            with col1:
                st.image(player['avatarfull'], width=150)
            with col2:
                st.header(player['personaname'])
                st.write(f"🌐 [Открыть профиль в Steam]({player['profileurl']})")
                
            # 2. Модуль инвентаря
            st.divider()
            st.header("📦 Инвентарь CS2")
            with st.expander("Просмотр скинов и предметов", expanded=True):
                st.warning("🔄 Модуль загрузки инвентаря находится в процессе интеграции. Ожидайте в v1.2.")
        else:
            st.error("Профиль не найден. Убедитесь, что введен корректный Steam ID 64.")
    except Exception as e:
        st.error(f"Ошибка подключения к Steam API: {e}")

st.divider()
st.caption("Данные подгружаются напрямую через официальный Steam Web API.")