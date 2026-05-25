import streamlit as st
from FSM import FSM

st.set_page_config(
    page_title="Ayobantu.com - Platform Donasi Online Indonesia",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Shared global CSS
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --brand-red:        #A61C24;
    --brand-red-light:  #FFF2F3;
    --brand-red-dark:   #86161D;
    --brand-blue:       #0073e6;
    --brand-blue-dark:  #005bb5;
    --brand-yellow:     #D49000;
    --brand-yellow-light:#FFFDF0;
    --brand-green:      #28A745;
    --text-dark:        #1A1A2E;
    --text-gray:        #6C757D;
    --border-color:     #E9ECEF;
    --soft-shadow:      0 4px 20px rgba(0, 0, 0, 0.06);
    --hover-shadow:     0 8px 30px rgba(0, 0, 0, 0.12);
}

html, body, [class*="css"] {
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    color: var(--text-dark);
    font-size: 16px !important;
}
#MainMenu, footer, header[data-testid="stHeader"] { display: none; }

[data-testid="stSidebar"] { display: none; }
</style>
    """,
    unsafe_allow_html=True,
)

# Initialize shared session state
if "fsm" not in st.session_state:
    st.session_state.fsm = FSM()
if "history" not in st.session_state:
    st.session_state.history = []
if "queued_input" not in st.session_state:
    st.session_state.queued_input = None
if "user" not in st.session_state:
    st.session_state.user = None

# Page navigation
beranda = st.Page("pages/beranda.py", title="Beranda", default=True)
chat = st.Page("pages/chat.py", title="Asisten Virtual")
profil = st.Page("pages/profil.py", title="Profil & Donasi")
donasi = st.Page("pages/donasi.py", title="Halaman Donasi")

pg = st.navigation([beranda, chat, profil, donasi], position="hidden")
pg.run()
