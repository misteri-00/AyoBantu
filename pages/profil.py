import streamlit as st

# =====================================================================
# PROFIL & LOGIN
# =====================================================================

st.markdown(
    """
<style>
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
html, body, .stApp {
    overflow-x: hidden !important;
}
.stMainBlockContainer { padding: 0 !important; }

/* Navbar (sama dengan beranda) */
.ab-navbar {
    background: white;
    padding: 0.9rem 3rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #eee;
}
.ab-navbar-logo {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    font-size: 1.8rem;
    color: #A61C24;
    text-decoration: none;
    letter-spacing: -1px;
}
.ab-navbar-logo span { color: #D49000; }

.auth-container {
    max-width: 450px;
    margin: 4rem auto;
    padding: 2.5rem;
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border: 1px solid #eee;
    text-align: center;
}
.auth-title {
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    font-size: 1.6rem;
    color: #1A1A2E;
    margin-bottom: 0.5rem;
}
.auth-sub {
    font-size: 0.9rem;
    color: #6C757D;
    margin-bottom: 2rem;
}

.profile-container {
    max-width: 1000px;
    margin: 3rem auto;
    padding: 2rem;
}
.prof-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid #E9ECEF;
}
.prof-name {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    font-size: 2rem;
    color: #1A1A2E;
}
.prof-stat-box {
    background: linear-gradient(135deg, #A61C24 0%, #86161D 100%);
    color: white;
    padding: 1.5rem 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 12px rgba(166,28,36,0.2);
}

.don-card {
    background: white;
    border: 1px solid #eee;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    display: flex;
    gap: 1.5rem;
    align-items: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}
.don-img {
    width: 100px;
    height: 100px;
    border-radius: 8px;
    background-size: cover;
    background-position: center;
    flex-shrink: 0;
}
.don-info {
    flex-grow: 1;
}
.don-title {
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    font-size: 1.25rem;
    color: #1A1A2E;
    margin-bottom: 0.3rem;
}
.don-amount {
    font-weight: 700;
    color: #28A745;
    font-size: 1.3rem;
}
.don-meta {
    font-size: 0.9rem;
    color: #6C757D;
    margin-top: 0.2rem;
}
.don-prayer {
    margin-top: 0.5rem;
    font-style: italic;
    font-size: 0.95rem;
    color: #926C0D;
    background: #FFFDF0;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    border-left: 3px solid #D49000;
}
</style>
    """,
    unsafe_allow_html=True,
)

# Navbar
st.markdown(
    """
<div class="ab-navbar">
    <span class="ab-navbar-logo">ayobantu<span>.com</span></span>
</div>
    """,
    unsafe_allow_html=True,
)

# Back button
col1, col2 = st.columns([1, 8])
with col1:
    st.markdown("<div style='padding-top:1rem; padding-left:3rem'>", unsafe_allow_html=True)
    if st.button("Kembali"):
        st.switch_page("pages/beranda.py")
    st.markdown("</div>", unsafe_allow_html=True)


if not st.session_state.user:
    # --- LOGIN PAGE ---
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<div class="auth-title">Masuk ke Akun Anda</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-sub">Pantau donasi dan jadilah pahlawan kebaikan.</div>', unsafe_allow_html=True)
    
    username = st.text_input("Nama Pengguna (Untuk Prototipe)", placeholder="Masukkan nama Anda...")
    if st.button("Masuk / Daftar", type="primary", use_container_width=True):
        if username.strip():
            # Register to DB if new
            st.session_state.fsm.engine.register_user(username.strip())
            st.session_state.user = username.strip()
            st.rerun()
        else:
            st.error("Nama pengguna tidak boleh kosong.")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- PROFILE & DONATION HISTORY ---
    username = st.session_state.user
    engine = st.session_state.fsm.engine
    
    donations = engine.get_user_donations(username)
    total_donated = sum(d["amount"] for d in donations)
    
    st.markdown('<div class="profile-container">', unsafe_allow_html=True)
    
    # Header
    col_l, col_r = st.columns([4, 1])
    with col_l:
        st.markdown(f'<div class="prof-name">Halo, {username}!</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="color:#6C757D">Terima kasih telah menjadi #OrangBaik</div>', unsafe_allow_html=True)
    with col_r:
        if st.button("Keluar (Logout)", use_container_width=True):
            st.session_state.user = None
            st.rerun()
            
    st.markdown('<hr style="margin: 1.5rem 0">', unsafe_allow_html=True)
    
    # Stats
    st.markdown(
        f'<div class="prof-stat-box">'
        f'<div style="font-size:0.9rem; opacity:0.9">Total Kebaikan Tersalurkan</div>'
        f'<div style="font-family:\'Outfit\',sans-serif; font-size:2.5rem; font-weight:800">Rp {total_donated:,}</div>'
        f'<div style="font-size:0.8rem; margin-top:0.3rem">Mendukung {len(donations)} program kampanye sosial</div>'
        f'</div>',
        unsafe_allow_html=True
    )
    
    # History List
    st.markdown('<h3 style="font-family:\'Outfit\',sans-serif; color:#1A1A2E">Riwayat Donasi</h3>', unsafe_allow_html=True)
    
    if not donations:
        st.info("Anda belum melakukan donasi. Yuk mulai berbagi hari ini!")
    else:
        for d in donations:
            date_str = d['created_at'].split()[0]
            prayer_html = f'<div class="don-prayer">"{d["prayer"]}"</div>' if d["prayer"] and d["prayer"] != "Tanpa pesan." else ""
            
            st.markdown(
                f'<div class="don-card">'
                f'<div class="don-img" style="background-image:url(\'{d["image_url"]}\')"></div>'
                f'<div class="don-info">'
                f'<div class="don-title">{d["title"]}</div>'
                f'<div class="don-amount">Rp {d["amount"]:,}</div>'
                f'<div class="don-meta">ID: {d["trx_id"]} • {date_str} • Pembayaran: {d["payment_method"]}</div>'
                f'{prayer_html}'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True
            )
            
    st.markdown('</div>', unsafe_allow_html=True)
