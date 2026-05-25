import streamlit as st
from datetime import datetime
from FSM import FSM

# =====================================================================
# ASISTEN VIRTUAL (Chat Page) — ChatGPT-like Interface
# =====================================================================

# Page-specific CSS
st.markdown(
    """
<style>
html, body, .stApp {
    overflow-x: hidden !important;
}
.block-container {
    padding-top: 0 !important;
    padding-bottom: 6rem;
    max-width: 760px !important;
    margin: 0 auto;
}
.stMainBlockContainer { padding-top: 0 !important; }

/* Chat page navbar */
.chat-navbar {
    background: white;
    padding: 0.65rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #eee;
    margin-bottom: 1rem;
}
.chat-navbar-left {
    display: flex;
    align-items: center;
    gap: 0.8rem;
}
.chat-navbar-logo {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    font-size: 1.25rem;
    color: #A61C24;
    text-decoration: none;
    letter-spacing: -0.5px;
}
.chat-navbar-logo span { color: #D49000; }
.chat-navbar-divider {
    width: 1px;
    height: 20px;
    background: #E9ECEF;
}
.chat-navbar-title {
    font-family: 'Outfit', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    color: #1A1A2E;
}
.chat-navbar-status {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.72rem;
    font-weight: 600;
    color: #28A745;
}
.chat-status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #28A745;
    animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
    0% { box-shadow: 0 0 0 0 rgba(40,167,69,0.5); }
    70% { box-shadow: 0 0 0 5px rgba(40,167,69,0); }
    100% { box-shadow: 0 0 0 0 rgba(40,167,69,0); }
}

/* Top bar with back + FSM */
.chat-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
    padding: 0 0.5rem;
}

/* FSM badge */
.chat-fsm-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #FFFDF0;
    border: 1px solid #E8D48A;
    border-radius: 6px;
    padding: 0.3rem 0.7rem;
    font-size: 0.7rem;
}
.chat-fsm-state {
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    color: #926C0D;
}
.chat-fsm-desc {
    color: #6D500B;
}

/* Chat message styling - smaller text */
[data-testid="stChatMessage"] {
    font-size: 0.88rem !important;
    line-height: 1.55 !important;
    padding: 0.8rem 1rem !important;
}
[data-testid="stChatMessage"] p {
    font-size: 1rem !important;
    line-height: 1.6 !important;
    margin-bottom: 0.3rem !important;
}
[data-testid="stChatMessage"] strong {
    font-weight: 700 !important;
}
[data-testid="stChatMessage"] code {
    font-size: 0.9rem !important;
}

/* Quick action chips */
.stButton > button {
    border-radius: 20px !important;
    font-weight: 600 !important;
    font-size: 0.75rem !important;
    padding: 0.35rem 0.8rem !important;
    transition: all 0.2s !important;
}

/* Chips label */
.chips-label {
    font-family: 'Outfit', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #6C757D;
    margin-bottom: 0.4rem;
}

/* Footer link */
.chat-footer-text {
    text-align: center;
    font-size: 0.7rem;
    color: #aaa;
    margin-top: 1.5rem;
    padding-bottom: 1rem;
}
</style>
    """,
    unsafe_allow_html=True,
)


def send_message(text: str):
    text = text.strip()
    if not text:
        return
    st.session_state.history.append({"role": "user", "content": text})
    username = st.session_state.user if st.session_state.user else "Anonim"
    reply = st.session_state.fsm.transition(text, username)
    st.session_state.history.append({"role": "assistant", "content": reply})


# ===================== NAVBAR =====================
st.markdown(
    """
<div class="chat-navbar">
    <div class="chat-navbar-left">
        <span class="chat-navbar-logo">ayobantu<span>.com</span></span>
        <div class="chat-navbar-divider"></div>
        <span class="chat-navbar-title">Asisten Virtual</span>
    </div>
    <div class="chat-navbar-status">
        <span class="chat-status-dot"></span>Online
    </div>
</div>
    """,
    unsafe_allow_html=True,
)

# Back button + FSM badge in one row
col_back, col_fsm = st.columns([1, 3])
with col_back:
    if st.button("Kembali", key="back_home", use_container_width=True):
        st.switch_page("pages/beranda.py")

STATE_INFO = {
    "DEFAULT": ("01", "Mulai Percakapan"),
    "ACTIVE": ("02", "Asisten Siap Membantu"),
    "BROWSE": ("03", "Memilih Kampanye Sosial"),
    "DONATE": ("04", "Menentukan Nominal Donasi"),
    "CONFIRM": ("05", "Konfirmasi Metode Pembayaran"),
    "END": ("06", "Transaksi Donasi Selesai"),
}
cur_state = st.session_state.fsm.state
num, desc = STATE_INFO.get(cur_state, ("00", ""))
with col_fsm:
    st.markdown(
        f'<div style="text-align:right; padding-top:0.4rem">'
        f'<div class="chat-fsm-badge">'
        f'<span class="chat-fsm-state">State: {cur_state} ({num}/06)</span>'
        f'<span class="chat-fsm-desc">- {desc}</span>'
        f"</div></div>",
        unsafe_allow_html=True,
    )

# Initialize history if empty
if not st.session_state.history:
    username = st.session_state.user if st.session_state.user else "Anonim"
    opening = st.session_state.fsm.transition("halo", username)
    st.session_state.history.append({"role": "assistant", "content": opening})

# Render Chat History natively (scrollable, ChatGPT style)
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Dynamic Quick Action Chips based on FSM state
state = st.session_state.fsm.state
if state == "CONFIRM":
    chips = [
        ("Bayar via GoPay", "gopay"),
        ("Bayar via OVO", "ovo"),
        ("Bayar via DANA", "dana"),
        ("Batalkan Donasi", "batal"),
    ]
elif state == "DONATE":
    chips = [
        ("Rp 20.000", "20000"),
        ("Rp 50.000", "50000"),
        ("Rp 100.000", "100000"),
        ("Batalkan", "batal"),
    ]
else:
    chips = [
        ("Daftar Kampanye", "katalog"),
        ("Pilar Bantuan", "kategori"),
        ("Izin Kemensos", "legalitas"),
        ("Zakat Online", "zakat"),
        ("Galang Dana", "galang dana"),
    ]

st.markdown('<div class="chips-label">Aksi Cepat</div>', unsafe_allow_html=True)
chip_cols = st.columns(len(chips))
for idx, (label, cmd) in enumerate(chips):
    if chip_cols[idx].button(label, key=f"chip_{state}_{idx}", use_container_width=True):
        st.session_state.queued_input = cmd
        st.rerun()

# Reset button - small, right-aligned
with st.columns([5, 1])[1]:
    if st.button("Reset", key="reset_chat", use_container_width=True):
        st.session_state.fsm = FSM()
        st.session_state.history = []
        st.rerun()

# Chat Text Input
user_input = st.chat_input("Tanyakan seputar kampanye atau tulis nominal donasi...")

# Action processors
if st.session_state.queued_input:
    queued = st.session_state.queued_input
    st.session_state.queued_input = None
    send_message(queued)
    st.rerun()

if user_input:
    send_message(user_input)
    st.rerun()

# Footer
st.markdown(
    '<div class="chat-footer-text">ayobantu.com - Platform Donasi Online Terpercaya</div>',
    unsafe_allow_html=True,
)
