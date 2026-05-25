import streamlit as st
from datetime import datetime

# =====================================================================
# BERANDA (Homepage) — Inspired by https://www.ayobantu.com/
# =====================================================================

# Page-specific CSS
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
/* Remove Streamlit default gaps on main container */
.stMainBlockContainer { padding: 0 !important; }

/* ---- Navbar ---- */
.ab-navbar {
    background: white;
    padding: 0.9rem 3rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #eee;
    position: sticky;
    top: 0;
    z-index: 100;
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
.ab-nav-links {
    display: flex;
    align-items: center;
    gap: 2rem;
}
.ab-nav-links a {
    font-size: 0.9rem;
    font-weight: 600;
    color: #1A1A2E;
    text-decoration: none;
    transition: color 0.2s;
}
.ab-nav-links a:hover { color: #A61C24; }
.ab-btn-galang {
    background: linear-gradient(135deg, #A61C24 0%, #86161D 100%);
    color: white !important;
    padding: 0.55rem 1.3rem;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.85rem;
    text-decoration: none;
    transition: transform 0.2s, box-shadow 0.2s;
    box-shadow: 0 4px 12px rgba(166, 28, 36, 0.2);
}
.ab-btn-galang:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(166, 28, 36, 0.3);
}

/* ---- Hero ---- */
.ab-hero {
    background: linear-gradient(135deg, #A61C24 0%, #6B1015 100%);
    color: white;
    padding: 5rem 2rem 4.5rem;
    position: relative;
    overflow: hidden;
}
.ab-hero::before {
    content: "";
    position: absolute;
    top: -120px;
    right: -100px;
    width: 450px;
    height: 450px;
    border-radius: 50%;
    background: rgba(255,255,255,0.04);
}
.ab-hero::after {
    content: "";
    position: absolute;
    bottom: -80px;
    left: -60px;
    width: 300px;
    height: 300px;
    border-radius: 50%;
    background: rgba(255,255,255,0.03);
}
.ab-hero-inner {
    max-width: 1200px;
    margin: 0 auto;
    position: relative;
    z-index: 1;
}
.ab-hero h1 {
    font-family: 'Outfit', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 1rem;
    letter-spacing: -1px;
}
.ab-hero p {
    font-size: 1.1rem;
    opacity: 0.92;
    max-width: 620px;
    line-height: 1.65;
    margin-bottom: 2rem;
}
.ab-hero-cta {
    display: inline-block;
    background: white;
    color: #A61C24;
    font-weight: 700;
    font-size: 0.95rem;
    padding: 0.75rem 2rem;
    border-radius: 8px;
    text-decoration: none;
    transition: transform 0.2s, box-shadow 0.2s;
    box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}
.ab-hero-cta:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}

/* ---- Section Wrapper ---- */
.ab-section {
    max-width: 1140px;
    margin: 0 auto;
    padding: 3rem 2rem;
}
.ab-section-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #1A1A2E;
    margin-bottom: 0.4rem;
}
.ab-section-sub {
    font-size: 0.92rem;
    color: #6C757D;
    margin-bottom: 1.5rem;
}

/* Campaign wrapper to constrain st.columns to section width */
.ab-campaign-wrapper {
    max-width: 1140px;
    margin: 0 auto;
    padding: 0 2rem 2rem;
}

/* ---- Category Strip ---- */
.ab-categories {
    display: flex;
    justify-content: center;
    gap: 2.5rem;
    flex-wrap: wrap;
}
.ab-cat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    text-decoration: none;
    transition: transform 0.2s;
}
.ab-cat-item:hover { transform: translateY(-4px); }
.ab-cat-icon {
    width: 60px;
    height: 60px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: 800;
    font-family: 'Outfit', sans-serif;
    transition: box-shadow 0.2s;
}
.ab-cat-item:hover .ab-cat-icon {
    box-shadow: 0 6px 18px rgba(0,0,0,0.1);
}
.ab-cat-label {
    font-size: 0.82rem;
    font-weight: 600;
    color: #1A1A2E;
}

/* ---- Campaign Cards ---- */
.ab-card-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
}
@media (max-width: 900px) {
    .ab-card-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 600px) {
    .ab-card-grid { grid-template-columns: 1fr; }
}
.ab-card {
    background: white;
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid #eee;
    margin-bottom: 1.5rem;
    transition: transform 0.25s, box-shadow 0.25s;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}
.ab-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.1);
}
.ab-card-img {
    height: 170px;
    background-size: cover;
    background-position: center;
    position: relative;
}
.ab-card-badge {
    position: absolute;
    top: 12px;
    left: 12px;
    background: rgba(0,0,0,0.6);
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    backdrop-filter: blur(4px);
}
.ab-card-body {
    padding: 1rem 1.2rem 1.2rem;
}
.ab-card-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #1A1A2E;
    line-height: 1.35;
    margin-bottom: 1rem;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    min-height: 48px;
}
.ab-progress-bg {
    background: #E9ECEF;
    border-radius: 4px;
    height: 6px;
    overflow: hidden;
    margin-bottom: 0.6rem;
}
.ab-progress-fill {
    background: linear-gradient(90deg, #28A745, #20c997);
    height: 100%;
    border-radius: 4px;
}
.ab-card-stats {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.6rem;
}
.ab-card-amount {
    font-size: 1.05rem;
    font-weight: 700;
    color: #28A745;
}
.ab-card-pct {
    font-size: 0.95rem;
    font-weight: 700;
    color: #1A1A2E;
}
.ab-card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #f0f0f0;
    padding-top: 0.6rem;
    font-size: 0.85rem;
}
.ab-card-days {
    color: #A61C24;
    font-weight: 600;
}
.ab-card-author {
    color: #6C757D;
    font-weight: 500;
}

/* ---- CTA Box ---- */
.ab-cta-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
}
@media (max-width: 700px) {
    .ab-cta-row { grid-template-columns: 1fr; }
}
.ab-cta-box {
    background: white;
    border-radius: 14px;
    padding: 2rem;
    border: 1px solid #eee;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    transition: transform 0.2s;
}
.ab-cta-box:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}
.ab-cta-icon {
    width: 60px;
    height: 60px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    font-size: 1.5rem;
    flex-shrink: 0;
}
.ab-cta-text h4 {
    font-family: 'Outfit', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    margin: 0 0 0.3rem 0;
    color: #1A1A2E;
}
.ab-cta-text p {
    font-size: 0.82rem;
    color: #6C757D;
    margin: 0;
    line-height: 1.4;
}

/* ---- Why Ayobantu ---- */
.ab-why-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
}
@media (max-width: 800px) {
    .ab-why-grid { grid-template-columns: repeat(2, 1fr); }
}
.ab-why-item {
    text-align: center;
    padding: 2rem 1rem;
    background: white;
    border-radius: 14px;
    border: 1px solid #eee;
    transition: transform 0.2s, box-shadow 0.2s;
}
.ab-why-item:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}
.ab-why-icon {
    width: 56px;
    height: 56px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1rem;
    font-family: 'Outfit', sans-serif;
    font-size: 1.3rem;
    font-weight: 800;
}
.ab-why-item h4 {
    font-family: 'Outfit', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
    color: #1A1A2E;
}
.ab-why-item p {
    font-size: 0.82rem;
    color: #6C757D;
    line-height: 1.5;
    margin: 0;
}

/* ---- Stats Bar ---- */
.ab-stats-bar {
    background: linear-gradient(135deg, #A61C24 0%, #6B1015 100%);
    color: white;
    border-radius: 14px;
    padding: 2rem 3rem;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    text-align: center;
}
.ab-stats-bar .ab-stat-num {
    font-family: 'Outfit', sans-serif;
    font-size: 2rem;
    font-weight: 800;
}
.ab-stats-bar .ab-stat-lbl {
    font-size: 0.82rem;
    opacity: 0.85;
}

/* ---- Footer ---- */
.ab-footer {
    background: #1A1A2E;
    color: white;
    padding: 2.5rem 3rem;
    text-align: center;
}
.ab-footer-brand {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}
.ab-footer-brand span { color: #D49000; }
.ab-footer p {
    font-size: 0.82rem;
    opacity: 0.7;
    line-height: 1.5;
    max-width: 600px;
    margin: 0 auto;
}
</style>
    """,
    unsafe_allow_html=True,
)

# ---- Data ----
engine = st.session_state.fsm.engine
catalog = engine.get_all_campaigns()
stats = engine.get_stats()

# ===================== NAVBAR =====================
login_label = "Profil Saya" if st.session_state.user else "Login / Daftar"

st.markdown(
    f"""
<div class="ab-navbar">
    <span class="ab-navbar-logo">ayobantu<span>.com</span></span>
    <div class="ab-nav-links">
        <a href="#">Donasi</a>
        <a href="#">Event</a>
        <a href="#">Zakat</a>
        <a href="#" class="ab-btn-galang">Galang Dana</a>
    </div>
</div>
    """,
    unsafe_allow_html=True,
)

# Navbar overlay buttons (streamlined)
col1, col2, col3 = st.columns([8, 1.5, 1])
with col2:
    st.markdown("<div style='margin-top:-3.5rem; text-align:right'>", unsafe_allow_html=True)
    if st.button(login_label, key="nav_login", use_container_width=True):
        st.switch_page("pages/profil.py")
    st.markdown("</div>", unsafe_allow_html=True)

# ===================== HERO =====================
st.markdown(
    """
<div class="ab-hero">
    <div class="ab-hero-inner">
        <h1>Ayo Bantu Mereka<br>yang Membutuhkan</h1>
        <p>Platform donasi online terpercaya di Indonesia. Salurkan bantuan sosial, medis, dan pendidikan secara amanah, cepat, dan transparan bersama ribuan #OrangBaik.</p>
    </div>
</div>
    """,
    unsafe_allow_html=True,
)

# ===================== CHAT CTA BUTTON =====================
st.markdown('<div style="max-width:1140px; margin:0 auto; padding:2rem 2rem 0;">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    if st.button("Mulai Chat dengan Asisten Virtual", key="go_to_chat", use_container_width=True, type="primary"):
        st.switch_page("pages/chat.py")
st.markdown('</div>', unsafe_allow_html=True)

# ===================== CATEGORIES =====================
st.markdown(
    """
<div class="ab-section">
    <h2 class="ab-section-title" style="text-align:center">AyoBantu Mereka yang Membutuhkan</h2>
    <p class="ab-section-sub" style="text-align:center">Pilih kategori favorit kamu</p>
    <div class="ab-categories">
        <div class="ab-cat-item">
            <div class="ab-cat-icon" style="background:#FFEFEF; color:#A61C24;">M</div>
            <span class="ab-cat-label">Medis</span>
        </div>
        <div class="ab-cat-item">
            <div class="ab-cat-icon" style="background:#E3F2FD; color:#005bb5;">B</div>
            <span class="ab-cat-label">Bencana</span>
        </div>
        <div class="ab-cat-item">
            <div class="ab-cat-icon" style="background:#FFFDF0; color:#B0800F;">P</div>
            <span class="ab-cat-label">Pendidikan</span>
        </div>
        <div class="ab-cat-item">
            <div class="ab-cat-icon" style="background:#EFEBE9; color:#5D4037;">S</div>
            <span class="ab-cat-label">Sosial</span>
        </div>
        <div class="ab-cat-item">
            <div class="ab-cat-icon" style="background:#E8F5E9; color:#2E7D32;">K</div>
            <span class="ab-cat-label">Keagamaan</span>
        </div>
        <div class="ab-cat-item">
            <div class="ab-cat-icon" style="background:#E0F2F1; color:#00695C;">L</div>
            <span class="ab-cat-label">Lingkungan</span>
        </div>
    </div>
</div>
    """,
    unsafe_allow_html=True,
)

# ===================== CAMPAIGN GRID =====================

st.markdown(
    '<div class="ab-section">'
    '<h2 class="ab-section-title">Kampanye Pilihan Mendesak</h2>'
    '<p class="ab-section-sub" style="margin-bottom:0">Program yang paling membutuhkan bantuan Anda saat ini</p>'
    '</div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="ab-campaign-wrapper">', unsafe_allow_html=True)

# Row 1 (first 3 cards)
row1 = st.columns(3)
for i in range(min(3, len(catalog))):
    camp = catalog[i]
    pct = min(int((camp["collected"] / camp["target"]) * 100), 100)
    verified = ' <span style="color:#0073e6;font-weight:800">&#10003;</span>' if camp["verified"] else ""
    with row1[i]:
        st.markdown(
            f'<div class="ab-card">'
            f'<div class="ab-card-img" style="background-image:url(\'{camp["image_url"]}\');">'
            f'<span class="ab-card-badge">{camp["category"]}</span></div>'
            f'<div class="ab-card-body">'
            f'<div class="ab-card-title">{camp["title"]}</div>'
            f'<div class="ab-progress-bg"><div class="ab-progress-fill" style="width:{pct}%"></div></div>'
            f'<div class="ab-card-stats"><span class="ab-card-amount">Rp {camp["collected"]:,}</span>'
            f'<span class="ab-card-pct">{pct}%</span></div>'
            f'<div class="ab-card-footer"><span class="ab-card-days">{camp["days_left"]} hari lagi</span>'
            f'<span class="ab-card-author">{camp["author"]}{verified}</span></div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )
        if st.button("Donasi Sekarang", key=f"btn_{camp['code']}", use_container_width=True):
            st.session_state.selected_campaign = camp['code']
            st.switch_page("pages/donasi.py")

# Row 2 (next 3 cards)
if len(catalog) > 3:
    row2 = st.columns(3)
    for i in range(3, min(6, len(catalog))):
        camp = catalog[i]
        pct = min(int((camp["collected"] / camp["target"]) * 100), 100)
        verified = ' <span style="color:#0073e6;font-weight:800">&#10003;</span>' if camp["verified"] else ""
        with row2[i - 3]:
            st.markdown(
                f'<div class="ab-card">'
                f'<div class="ab-card-img" style="background-image:url(\'{camp["image_url"]}\');">'
                f'<span class="ab-card-badge">{camp["category"]}</span></div>'
                f'<div class="ab-card-body">'
                f'<div class="ab-card-title">{camp["title"]}</div>'
                f'<div class="ab-progress-bg"><div class="ab-progress-fill" style="width:{pct}%"></div></div>'
                f'<div class="ab-card-stats"><span class="ab-card-amount">Rp {camp["collected"]:,}</span>'
                f'<span class="ab-card-pct">{pct}%</span></div>'
                f'<div class="ab-card-footer"><span class="ab-card-days">{camp["days_left"]} hari lagi</span>'
                f'<span class="ab-card-author">{camp["author"]}{verified}</span></div>'
                f'</div></div>',
                unsafe_allow_html=True,
            )
            if st.button("Donasi Sekarang", key=f"btn_{camp['code']}", use_container_width=True):
                st.session_state.selected_campaign = camp['code']
                st.switch_page("pages/donasi.py")

st.markdown('</div>', unsafe_allow_html=True)  # close ab-campaign-wrapper

# ===================== CTA BOXES =====================
st.markdown(
    """
<div class="ab-section">
    <div class="ab-cta-row">
        <div class="ab-cta-box">
            <div class="ab-cta-icon" style="background:#FFF2F3; color:#A61C24;">D</div>
            <div class="ab-cta-text">
                <h4>Masih ingin berdonasi lebih banyak?</h4>
                <p>Temukan lebih banyak kampanye sosial aktif untuk Anda dukung.</p>
            </div>
        </div>
        <div class="ab-cta-box">
            <div class="ab-cta-icon" style="background:#FFFDF0; color:#D49000;">G</div>
            <div class="ab-cta-text">
                <h4>#AyoBantu galang dana</h4>
                <p>Buat kampanye penggalangan dana untuk mereka yang membutuhkan.</p>
            </div>
        </div>
    </div>
</div>
    """,
    unsafe_allow_html=True,
)

# ===================== STATS BAR =====================
st.markdown(
    f"""
<div class="ab-section">
    <div class="ab-stats-bar">
        <div>
            <div class="ab-stat-num">{stats['campaigns']}</div>
            <div class="ab-stat-lbl">Kampanye Aktif</div>
        </div>
        <div>
            <div class="ab-stat-num">Rp {stats['collected']:,}</div>
            <div class="ab-stat-lbl">Dana Terkumpul</div>
        </div>
        <div>
            <div class="ab-stat-num">{stats['categories']}</div>
            <div class="ab-stat-lbl">Pilar Kebaikan</div>
        </div>
    </div>
</div>
    """,
    unsafe_allow_html=True,
)

# ===================== WHY AYOBANTU =====================
st.markdown(
    """
<div class="ab-section">
    <h2 class="ab-section-title" style="text-align:center">Kenapa Ayobantu?</h2>
    <p class="ab-section-sub" style="text-align:center">#AyoBantu sesama yang membutuhkan</p>
    <div class="ab-why-grid">
        <div class="ab-why-item">
            <div class="ab-why-icon" style="background:#FFF2F3; color:#A61C24;">B</div>
            <h4>Bantu</h4>
            <p>#AyoBantu sesama yang membutuhkan dengan mudah</p>
        </div>
        <div class="ab-why-item">
            <div class="ab-why-icon" style="background:#E3F2FD; color:#005bb5;">P</div>
            <h4>Praktis</h4>
            <p>Bantu sesama dari mana pun, cukup gunakan HP kita</p>
        </div>
        <div class="ab-why-item">
            <div class="ab-why-icon" style="background:#E8F5E9; color:#2E7D32;">T</div>
            <h4>Tepat Sasaran</h4>
            <p>Program penggalangan dana dapat dipertanggungjawabkan</p>
        </div>
        <div class="ab-why-item">
            <div class="ab-why-icon" style="background:#FFFDF0; color:#D49000;">S</div>
            <h4>Transparan</h4>
            <p>Penyaluran dana dilakukan secara transparan dan terbuka</p>
        </div>
    </div>
</div>
    """,
    unsafe_allow_html=True,
)

# ===================== FOOTER =====================
st.markdown(
    f"""
<div class="ab-footer">
    <div class="ab-footer-brand">ayobantu<span>.com</span></div>
    <p>&copy; {datetime.now().year} Yayasan Ayo Bantu Peduli Indonesia. Terdaftar resmi dengan izin PUB dari Kementerian Sosial RI (SK Kemensos No. 343/HUK-PS/2023). Semua donasi disalurkan secara transparan.</p>
</div>
    """,
    unsafe_allow_html=True,
)
