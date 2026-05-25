import streamlit as st
import urllib.parse
from datetime import datetime

# =====================================================================
# HALAMAN DONASI MANUAL
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

.donasi-container {
    max-width: 800px;
    margin: 2rem auto 4rem;
    padding: 2rem;
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.04);
    border: 1px solid #eee;
}

.camp-header {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 2px solid #E9ECEF;
}
.camp-img {
    width: 180px;
    height: 120px;
    border-radius: 12px;
    background-size: cover;
    background-position: center;
    flex-shrink: 0;
}
.camp-info h2 {
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    font-size: 1.6rem;
    color: #1A1A2E;
    margin: 0 0 0.5rem 0;
    line-height: 1.3;
}
.camp-info p {
    color: #6C757D;
    font-size: 1.05rem;
    margin: 0 0 0.5rem 0;
}

.progress-bg {
    background: #E9ECEF;
    border-radius: 4px;
    height: 8px;
    overflow: hidden;
    margin-bottom: 0.5rem;
}
.progress-fill {
    background: linear-gradient(90deg, #28A745, #20c997);
    height: 100%;
    border-radius: 4px;
}
.stats-row {
    display: flex;
    justify-content: space-between;
    font-size: 1rem;
    font-weight: 600;
}

.form-label {
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    font-size: 1.25rem;
    color: #1A1A2E;
    margin-bottom: 0.5rem;
    display: block;
}

.qris-box {
    text-align: center;
    padding: 2rem;
    background: #F8F9FA;
    border-radius: 12px;
    border: 2px dashed #D49000;
    margin-top: 2rem;
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
        st.session_state.selected_campaign = None
        st.switch_page("pages/beranda.py")
    st.markdown("</div>", unsafe_allow_html=True)


if "selected_campaign" not in st.session_state or not st.session_state.selected_campaign:
    st.warning("Tidak ada kampanye yang dipilih. Silakan kembali ke Beranda.")
    st.stop()

# Load Data
engine = st.session_state.fsm.engine
campaign_code = st.session_state.selected_campaign
camp = engine.get_campaign_exact(campaign_code)
username = st.session_state.user if st.session_state.user else "Anonim"

if not camp:
    st.error("Kampanye tidak ditemukan!")
    st.stop()

pct = min(int((camp["collected"] / camp["target"]) * 100), 100)

st.markdown('<div class="donasi-container">', unsafe_allow_html=True)

# Campaign Info Header
st.markdown(
    f"""
    <div class="camp-header">
        <div class="camp-img" style="background-image:url('{camp['image_url']}')"></div>
        <div class="camp-info">
            <h2>{camp['title']}</h2>
            <p>Inisiator: <strong>{camp['author']}</strong> • Kategori: {camp['category']}</p>
            <div class="progress-bg"><div class="progress-fill" style="width:{pct}%"></div></div>
            <div class="stats-row">
                <span style="color:#28A745">Terkumpul: Rp {camp['collected']:,}</span>
                <span>Target: Rp {camp['target']:,}</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Jika donasi berhasil, tunjukkan QRIS dan resi
if "payment_success" in st.session_state and st.session_state.payment_success == campaign_code:
    trx_id = st.session_state.last_trx_id
    amount = st.session_state.last_amount
    prayer = st.session_state.last_prayer
    method = st.session_state.last_method
    
    qr_data = f"ayobantu.com/pay/{trx_id}?amount={amount}"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={urllib.parse.quote(qr_data)}&color=1A1A2E"
    
    st.success("Donasi Berhasil Diproses! Terima kasih Orang Baik.")
    st.markdown(
        f"""
        <div class="qris-box">
            <h3 style="margin-top:0">Scan QRIS untuk Membayar</h3>
            <img src="{qr_url}" alt="QRIS" style="border-radius:12px; margin: 1rem 0; box-shadow:0 4px 12px rgba(0,0,0,0.1)">
            <p style="font-size:0.9rem; color:#6C757D; margin-bottom:0.5rem">ID Transaksi: <strong>{trx_id}</strong></p>
            <p style="font-size:0.9rem; color:#6C757D; margin-bottom:0">Nominal: <strong>Rp {amount:,}</strong> • Metode: <strong>{method}</strong></p>
            <div style="margin-top:1rem; padding:1rem; background:white; border-radius:8px; display:inline-block; border:1px solid #eee">
                <em style="color:#D49000">"{prayer}"</em>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Selesai & Kembali ke Beranda", type="primary", use_container_width=True):
        del st.session_state.payment_success
        st.session_state.selected_campaign = None
        st.switch_page("pages/beranda.py")
        
else:
    # Form Donasi
    st.markdown('<span class="form-label">1. Nominal Donasi</span>', unsafe_allow_html=True)
    amount = st.number_input("Masukkan nominal (Min. Rp 10.000)", min_value=10000, value=50000, step=10000, label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<span class="form-label">2. Metode Pembayaran</span>', unsafe_allow_html=True)
    payment_method = st.selectbox(
        "Pilih metode",
        ["GoPay", "OVO", "ShopeePay", "DANA", "BCA Virtual Account", "Mandiri Virtual Account"],
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<span class="form-label">3. Titip Doa / Dukungan (Opsional)</span>', unsafe_allow_html=True)
    prayer = st.text_area("Tuliskan doa untuk kampanye ini...", placeholder="Semoga berkah dan bermanfaat...", label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Lanjutkan Pembayaran", type="primary", use_container_width=True):
        # Proses Donasi
        final_prayer = prayer.strip() if prayer.strip() else "Tanpa pesan."
        
        trx_id = engine.insert_donation(
            username=username,
            campaign_code=campaign_code,
            amount=amount,
            payment_method=payment_method.upper(),
            prayer=final_prayer
        )
        
        # Simpan state sukses
        st.session_state.payment_success = campaign_code
        st.session_state.last_trx_id = trx_id
        st.session_state.last_amount = amount
        st.session_state.last_prayer = final_prayer
        st.session_state.last_method = payment_method.upper()
        
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
