import re
import sqlite3
import random
from datetime import datetime

# =====================================================================
# DATA SEEDING
# =====================================================================

INITIAL_CAMPAIGNS = [
    {
        "code": "AYO-MED-001",
        "title": "Bantu Dek Alifa Sembuh dari Atresia Bilier",
        "author": "Yayasan Peduli Sehat",
        "category": "Medis",
        "target": 150000000,
        "collected": 95500000,
        "verified": 1,
        "days_left": 12,
        "image_url": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=400&q=80",
    },
    {
        "code": "AYO-DIS-001",
        "title": "Solidaritas untuk Korban Banjir Bandang Demak",
        "author": "Aksi Cepat Kemanusiaan",
        "category": "Bencana",
        "target": 200000000,
        "collected": 142300000,
        "verified": 1,
        "days_left": 6,
        "image_url": "https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=400&q=80",
    },
    {
        "code": "AYO-EDU-001",
        "title": "Beasiswa Pendidikan untuk Anak Pesisir",
        "author": "Indonesia Mengajar Bersama",
        "category": "Pendidikan",
        "target": 80000000,
        "collected": 35000000,
        "verified": 1,
        "days_left": 28,
        "image_url": "https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?auto=format&fit=crop&w=400&q=80",
    },
    {
        "code": "AYO-SOC-001",
        "title": "Pangan Layak untuk Lansia Telantar",
        "author": "Dapur Berbagi",
        "category": "Sosial",
        "target": 50000000,
        "collected": 47800000,
        "verified": 0,
        "days_left": 3,
        "image_url": "https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?auto=format&fit=crop&w=400&q=80",
    },
    {
        "code": "AYO-REL-001",
        "title": "Renovasi Masjid Pelosok NTT Hampir Roboh",
        "author": "Cinta Masjid Nusantara",
        "category": "Keagamaan",
        "target": 120000000,
        "collected": 12000000,
        "verified": 1,
        "days_left": 45,
        "image_url": "https://images.unsplash.com/photo-1597935258735-e254c1839512?auto=format&fit=crop&w=400&q=80",
    },
    {
        "code": "AYO-ENV-001",
        "title": "Selamatkan Orangutan Kalimantan dari Kepunahan",
        "author": "Wildlife Conservation Trust",
        "category": "Lingkungan",
        "target": 100000000,
        "collected": 82100000,
        "verified": 1,
        "days_left": 18,
        "image_url": "https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?auto=format&fit=crop&w=400&q=80",
    },
    {
        "code": "AYO-MED-002",
        "title": "Bantu Pejuang Kanker Payudara Berobat",
        "author": "Pita Merah muda",
        "category": "Medis",
        "target": 250000000,
        "collected": 110000000,
        "verified": 1,
        "days_left": 60,
        "image_url": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=400&q=80",
    },
    {
        "code": "AYO-DIS-002",
        "title": "Bantuan Darurat Gempa Bumi Sumedang",
        "author": "Relawan Siaga",
        "category": "Bencana",
        "target": 300000000,
        "collected": 275000000,
        "verified": 1,
        "days_left": 2,
        "image_url": "https://images.unsplash.com/photo-1563804825906-e71e98d9e728?auto=format&fit=crop&w=400&q=80",
    },
]

AYOBANTU_INFO = {
    "cara_donasi": (
        "**Cara berdonasi di Ayobantu:**\n"
        "1. Pilih kampanye sosial aktif yang ingin Anda bantu.\n"
        "2. Masukkan nominal donasi Anda (minimal Rp 10.000).\n"
        "3. Pilih metode pembayaran instan (GoPay, OVO, ShopeePay, DANA) atau Transfer Bank.\n"
        "4. Lakukan pembayaran sesuai petunjuk. Konfirmasi akan diproses secara otomatis!"
    ),
    "metode_bayar": (
        "**Metode Pembayaran yang tersedia di Ayobantu:**\n"
        "- **E-Wallet:** GoPay, OVO, ShopeePay, DANA, LinkAja.\n"
        "- **Virtual Account:** BCA, Mandiri, BNI, BRI, Permata Bank.\n"
        "- **Kartu Kredit:** Visa, Mastercard."
    ),
    "galang_dana": (
        "**Cara menggalang dana di Ayobantu:**\n"
        "1. Klik tombol **Galang Dana** di bagian kanan atas halaman.\n"
        "2. Buat akun, isi profil inisiator, dan unggah KTP/dokumen organisasi untuk verifikasi.\n"
        "3. Tulis cerita kampanye, sertakan foto/video pendukung, serta rincian rencana penggunaan anggaran.\n"
        "4. Setelah diverifikasi tim Ayobantu, kampanye Anda akan aktif dan siap menerima donasi!"
    ),
    "zakat": (
        "**Zakat Online Ayobantu:**\n"
        "Ayobantu bekerja sama dengan Lembaga Amil Zakat resmi (seperti BAZNAS, Lazismu, LAZISNU) untuk menyalurkan zakat maal, zakat fitrah, dan sedekah produktif. "
        "Semua dana zakat disalurkan 100% amanah kepada 8 asnaf penerima zakat yang berhak."
    ),
    "legalitas": (
        "**Aspek Legalitas & Keamanan Ayobantu:**\n"
        "Yayasan Ayo Bantu Peduli Indonesia terdaftar resmi dan memiliki izin penggalangan dana dari **Kementerian Sosial Republik Indonesia (Kemensos RI)** dengan Surat Keputusan Nomor: **343/HUK-PS/2023**.\n"
        "Setiap donasi disalurkan secara transparan dengan laporan berkala di halaman kampanye."
    ),
}

# =====================================================================
# SQLITE ENGINE
# =====================================================================

class Engine:
    def __init__(self):
        # Gunakan database file agar data persisten selama proses Streamlit berjalan
        # (check_same_thread=False karena Streamlit bersifat multi-threaded)
        self.conn = sqlite3.connect("ayobantu.db", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_db()
        self.info = AYOBANTU_INFO

    def _init_db(self):
        cursor = self.conn.cursor()
        
        # Tabel Users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabel Campaigns
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS campaigns (
                code TEXT PRIMARY KEY,
                title TEXT,
                author TEXT,
                category TEXT,
                target INTEGER,
                collected INTEGER,
                verified INTEGER,
                days_left INTEGER,
                image_url TEXT
            )
        """)
        
        # Tabel Donations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS donations (
                trx_id TEXT PRIMARY KEY,
                username TEXT,
                campaign_code TEXT,
                amount INTEGER,
                payment_method TEXT,
                prayer TEXT,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(campaign_code) REFERENCES campaigns(code)
            )
        """)
        
        # Seed Data jika tabel campaigns kosong
        cursor.execute("SELECT COUNT(*) as count FROM campaigns")
        if cursor.fetchone()["count"] == 0:
            for c in INITIAL_CAMPAIGNS:
                cursor.execute("""
                    INSERT INTO campaigns (code, title, author, category, target, collected, verified, days_left, image_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (c["code"], c["title"], c["author"], c["category"], c["target"], c["collected"], c["verified"], c["days_left"], c["image_url"]))
            self.conn.commit()

    # ---- DATABASE QUERIES ----

    def get_all_campaigns(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM campaigns ORDER BY category, title")
        return [dict(row) for row in cursor.fetchall()]

    def get_categories(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM campaigns")
        return [row["category"] for row in cursor.fetchall()]

    def get_stats(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) as campaigns, SUM(collected) as total_collected, SUM(target) as total_target, COUNT(DISTINCT category) as categories FROM campaigns")
        res = cursor.fetchone()
        
        c = res["total_collected"] or 0
        t = res["total_target"] or 1
        pct = min(int((c / t) * 100), 100)
        
        return {
            "campaigns": res["campaigns"],
            "collected": c,
            "target": t,
            "percentage": pct,
            "categories": res["categories"]
        }

    def find_campaigns(self, query: str):
        cursor = self.conn.cursor()
        q = f"%{query.lower()}%"
        cursor.execute("""
            SELECT * FROM campaigns 
            WHERE LOWER(title) LIKE ? OR LOWER(category) LIKE ? OR LOWER(code) LIKE ?
        """, (q, q, q))
        return [dict(row) for row in cursor.fetchall()]

    def get_campaign_exact(self, query: str):
        # Mirip find_campaigns, tapi me-return 1 hasil terbaik (pertama)
        res = self.find_campaigns(query)
        if res:
            return res[0]
        return None

    def insert_donation(self, username: str, campaign_code: str, amount: int, payment_method: str, prayer: str):
        cursor = self.conn.cursor()
        trx_id = f"TRX-AB-{random.randint(1000000, 9999999)}"
        
        # Insert ke tabel donasi
        cursor.execute("""
            INSERT INTO donations (trx_id, username, campaign_code, amount, payment_method, prayer, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (trx_id, username, campaign_code, amount, payment_method, prayer, "SUCCESS"))
        
        # Update saldo terkumpul di kampanye
        cursor.execute("""
            UPDATE campaigns SET collected = collected + ? WHERE code = ?
        """, (amount, campaign_code))
        
        self.conn.commit()
        return trx_id

    def get_user_donations(self, username: str):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT d.trx_id, d.amount, d.payment_method, d.prayer, d.created_at, c.title, c.image_url 
            FROM donations d
            JOIN campaigns c ON d.campaign_code = c.code
            WHERE d.username = ?
            ORDER BY d.created_at DESC
        """, (username,))
        return [dict(row) for row in cursor.fetchall()]

    def register_user(self, username: str):
        cursor = self.conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
            self.conn.commit()

    # ---- CHATBOT INTENT LOGIC ----

    def detect_intent(self, text: str) -> str:
        t = text.lower().strip()

        if re.search(r"\b(reset|mulai ulang|restart)\b", t):
            return "RESET"
        if re.search(r"\b(halo|hai|hi|hello|hey|selamat|permisi)\b", t):
            return "GREET"
        if re.search(r"\b(cari|search|temukan|lihat donasi|ada apa|bantu apa|tampilkan)\b", t):
            return "SEARCH"
        if re.search(r"\b(donasi|sumbang|bantu|bayar|kasih|kirim uang)\b", t):
            return "DONATE"
        if re.search(r"\b(katalog|daftar kampanye|semua kampanye|list donasi|program)\b", t):
            return "LIST_CATALOG"
        if re.search(r"\b(kategori|jenis program|pilar|sektor)\b", t):
            return "LIST_CATEGORY"
        if re.search(r"\b(ya|yes|oke|betul|siap|lanjut|benar|iya|setuju|gopay|ovo|shopeepay|dana|bca|mandiri|bni|bri)\b", t):
            return "YES"
        if re.search(r"\b(tidak|enggak|nggak|batal|cancel|no|skip|lewat)\b", t):
            return "NO"
        if re.search(r"\b(terima kasih|makasih|thanks|thank you)\b", t):
            return "THANKS"
        if re.search(r"\b(selesai|keluar|exit|bye|sampai jumpa)\b", t):
            return "EXIT"
        if re.search(r"\b(ayobantu|profil|tentang|apa itu)\b", t):
            return "ASK_ABOUT"
        if re.search(r"\b(metode|cara bayar|rekening|ewallet|e-wallet|pembayaran)\b", t):
            return "ASK_PAYMENT"
        if re.search(r"\b(galang dana|buat kampanye|bikin program|inisiator)\b", t):
            return "ASK_FUNDRAISE"
        if re.search(r"\b(zakat|fitrah|maal)\b", t):
            return "ASK_ZAKAT"
        if re.search(r"\b(legal|izin|kemensos|aman|percaya|resmi)\b", t):
            return "ASK_LEGAL"
        
        # Cek apakah me-mention kode unik kampanye
        cursor = self.conn.cursor()
        cursor.execute("SELECT code FROM campaigns")
        codes = [row["code"].lower() for row in cursor.fetchall()]
        if codes:
            pattern = rf"({'|'.join(re.escape(c) for c in codes)})"
            if re.search(pattern, t):
                return "CAMPAIGN_MENTIONED"

        return "UNKNOWN"

    def format_campaign_card(self, campaign: dict) -> str:
        percentage = min(int((campaign["collected"] / campaign["target"]) * 100), 100)
        verify_status = "✓ Terverifikasi" if campaign["verified"] else "Belum Terverifikasi"
        return (
            f"**{campaign['title']}**\n"
            f"Kategori : {campaign['category']} ({campaign['code']})\n"
            f"Inisiator: {campaign['author']} ({verify_status})\n"
            f"Progres  : **Rp {campaign['collected']:,}** terkumpul dari **Rp {campaign['target']:,}** ({percentage}%)\n"
            f"Sisa Hari: **{campaign['days_left']} hari lagi**"
        )

    def format_catalog(self) -> str:
        campaigns = self.get_all_campaigns()
        lines = ["**Daftar Kampanye Sosial Aktif:**\n"]
        current_cat = None
        for data in campaigns:
            if data["category"] != current_cat:
                current_cat = data["category"]
                lines.append(f"\n**Pilar {current_cat}**")
            percentage = min(int((data["collected"] / data["target"]) * 100), 100)
            lines.append(
                f"  - **{data['title']}**\n    Terkumpul: Rp {data['collected']:,} ({percentage}%) — `{data['code']}`"
            )
        return "\n".join(lines)

    def format_categories(self) -> str:
        categories = self.get_categories()
        cursor = self.conn.cursor()
        
        lines = ["**Pilar Kebaikan / Kategori Bantuan:**\n"]
        for cat in categories:
            cursor.execute("SELECT COUNT(*) as count FROM campaigns WHERE category = ?", (cat,))
            count = cursor.fetchone()["count"]
            lines.append(f"- **{cat}** ({count} kampanye aktif)")
        lines.append("\nKetik nama kategori atau ketik **katalog** untuk melihat rincian kampanye.")
        return "\n".join(lines)

    def get_info(self, key: str) -> str:
        return self.info.get(key, "")
