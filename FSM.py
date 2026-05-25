import random
import re
import urllib.parse
from engine import Engine

STATE_DEFAULT = "DEFAULT"
# ACTIVE: Bot is ready to receive campaign search/donation requests or general inquiries.
STATE_ACTIVE = "ACTIVE"
# BROWSE: User is searching or listing campaigns.
STATE_BROWSE = "BROWSE"
# DONATE: User is prompted to input donation amount.
STATE_DONATE = "DONATE"
# PRAYER: User is prompted to input a prayer/message for the donation.
STATE_PRAYER = "PRAYER"
# CONFIRM: User is choosing a payment method or verifying the donation.
STATE_CONFIRM = "CONFIRM"
# END: Conversation has ended.
STATE_END = "END"


class FSM:
    def __init__(self):
        self.engine = Engine()
        self.state = STATE_DEFAULT
        self.pending_campaign = None
        self.pending_amount = None
        self.pending_prayer = None
        self.pending_payment = None
        self.username = "Anonim" # Default if not logged in

    def transition(self, user_input: str, username: str = "Anonim") -> str:
        self.username = username
        intent = self.engine.detect_intent(user_input)

        if intent == "RESET":
            self.state = STATE_DEFAULT
            self.pending_campaign = None
            self.pending_amount = None
            self.pending_prayer = None
            self.pending_payment = None
            return "Sesi direset. Ketik **halo** untuk memulai kembali penjelajahan kampanye sosial."

        if self.state == STATE_DEFAULT:
            return self._from_default(intent, user_input)

        if self.state == STATE_ACTIVE:
            return self._from_active(intent, user_input)

        if self.state == STATE_BROWSE:
            return self._from_browse(intent, user_input)

        if self.state == STATE_DONATE:
            return self._from_donate(intent, user_input)
            
        if self.state == STATE_PRAYER:
            return self._from_prayer(intent, user_input)

        if self.state == STATE_CONFIRM:
            return self._from_confirm(intent, user_input)

        if self.state == STATE_END:
            if intent == "GREET":
                self.state = STATE_ACTIVE
                return "Selamat datang kembali! Ada kampanye sosial lain yang ingin Anda dukung hari ini?"
            return "Ketik **halo** atau **katalog** untuk memulai sesi baru."

        return "Terjadi kesalahan sistem. Silakan ketik **reset** untuk memulai ulang."

    def _from_default(self, intent: str, text: str) -> str:
        self.state = STATE_ACTIVE
        if intent == "GREET":
            return (
                f"Halo **{self.username}**! Selamat datang di Asisten Virtual **Ayobantu.com**\n\n"
                "Saya siap memandu Anda untuk berdonasi secara cepat, aman, dan transparan.\n\n"
                "Berikut beberapa hal yang bisa Anda tanyakan:\n"
                "- **Cari Kampanye** (Ketik judul kampanye, misal: *alifa* atau *banjir*)\n"
                "- **Lihat Koleksi** (Ketik `katalog` atau `kategori` untuk pilar donasi)\n"
                "- **Donasi Langsung** (Ketik `donasi [nama kampanye]`)\n"
                "- **Info Layanan** (Ketik `legalitas`, `metode bayar`, `zakat`, atau `galang dana`)\n\n"
                "Kampanye mana yang ingin Anda bantu hari ini?"
            )
        return self._from_active(intent, text)

    def _from_active(self, intent: str, text: str) -> str:
        if intent in ("SEARCH", "LIST_CATALOG", "CAMPAIGN_MENTIONED"):
            self.state = STATE_BROWSE
            return self._handle_search(text)

        if intent == "LIST_CATEGORY":
            self.state = STATE_BROWSE
            return self.engine.format_categories()

        if intent == "DONATE":
            campaign = self.engine.get_campaign_exact(text)
            if campaign:
                self.state = STATE_DONATE
                self.pending_campaign = campaign
                return (
                    f"Anda memilih untuk berdonasi pada kampanye:\n\n"
                    f"{self.engine.format_campaign_card(campaign)}\n\n"
                    f"Berapa nominal donasi yang ingin Anda berikan? (Ketik nominal angka, contoh: **50000** atau **100000**)"
                )
            self.state = STATE_BROWSE
            return "Kampanye apa yang ingin Anda bantu? Silakan sebutkan nama kampanye atau ketik **katalog** untuk melihat daftar aktif."

        # Inquiries
        if intent == "ASK_ABOUT":
            return (
                "**Tentang Ayobantu.com:**\n\n"
                "Ayobantu adalah platform crowdfunding (galang dana) online terpercaya di Indonesia yang memfasilitasi "
                "kegiatan donasi sosial, medis, pendidikan, bencana alam, keagamaan, dan kelestarian lingkungan.\n\n"
                "Kami berkomitmen untuk menjembatani kepedulian masyarakat dengan transparansi penuh dan akuntabilitas tinggi."
            )

        if intent == "ASK_PAYMENT":
            return self.engine.get_info("metode_bayar")

        if intent == "ASK_FUNDRAISE":
            return self.engine.get_info("galang_dana")

        if intent == "ASK_ZAKAT":
            return self.engine.get_info("zakat")

        if intent == "ASK_LEGAL":
            return self.engine.get_info("legalitas")

        if intent == "THANKS":
            self.state = STATE_END
            return (
                "Sama-sama! Terima kasih atas kepedulian dan kebaikan Anda. Semoga kebaikan Anda dilipatgandakan.\n\n"
                "Salam hangat dari komunitas Ayobantu! Kapan pun Anda ingin berbagi kembali, saya siap membantu."
            )

        if intent == "EXIT":
            self.state = STATE_END
            return "Terima kasih telah berkunjung di Ayobantu. Semoga hari Anda menyenangkan dan penuh berkah!"

        return (
            "Maaf, saya belum memahami instruksi Anda. Anda bisa mengetik:\n\n"
            "- **katalog** — melihat semua kampanye aktif\n"
            "- **kategori** — melihat kategori bantuan\n"
            "- **donasi [nama kampanye]** — melakukan donasi\n"
            "- **legalitas** — cek izin operasional Kemensos RI\n"
            "- **metode bayar** — melihat pilihan pembayaran"
        )

    def _from_browse(self, intent: str, text: str) -> str:
        if intent == "DONATE":
            campaign = self.engine.get_campaign_exact(text)
            if campaign:
                self.state = STATE_DONATE
                self.pending_campaign = campaign
                return (
                    f"Anda memilih untuk berdonasi pada kampanye:\n\n"
                    f"{self.engine.format_campaign_card(campaign)}\n\n"
                    f"Berapa nominal donasi yang ingin Anda berikan? (Ketik nominal angka, contoh: **50000** atau **100000**)"
                )
            self.state = STATE_DONATE
            return "Silakan sebutkan nama kampanye yang ingin Anda bantu untuk melanjutkan proses donasi."

        if intent in ("SEARCH", "CAMPAIGN_MENTIONED", "LIST_CATALOG"):
            return self._handle_search(text)

        if intent == "LIST_CATEGORY":
            return self.engine.format_categories()

        self.state = STATE_ACTIVE
        return self._from_active(intent, text)

    def _from_donate(self, intent: str, text: str) -> str:
        if intent == "NO" or "batal" in text.lower():
            self.pending_campaign = None
            self.state = STATE_ACTIVE
            return "Proses donasi dibatalkan. Ada yang bisa saya bantu lagi?"

        # Try to extract the number from user input
        nums = re.findall(r"\d+", text.replace(".", "").replace(",", ""))
        if nums:
            amount = int(nums[0])
            if amount < 10000:
                return "Mohon maaf, batas minimal donasi adalah **Rp 10.000**. Silakan masukkan nominal donasi yang lebih besar."

            self.pending_amount = amount
            self.state = STATE_PRAYER
            campaign_title = self.pending_campaign["title"]
            return (
                f"Baik, donasi sebesar **Rp {amount:,}** untuk **{campaign_title}**.\n\n"
                f"**Titip Doa/Pesan (Opsional):**\n"
                f"Apakah ada doa, harapan, atau pesan yang ingin Anda sampaikan untuk kampanye ini?\n"
                f"*(Ketik pesan Anda, atau ketik **lewat/skip** jika tidak ada)*"
            )

        return (
            f"Nominal tidak valid. Berapa nominal donasi yang ingin Anda berikan untuk **{self.pending_campaign['title']}**?\n"
            f"(Ketik angka saja, contoh: **20000** atau **50000**)"
        )

    def _from_prayer(self, intent: str, text: str) -> str:
        text_lower = text.lower().strip()
        
        if intent == "NO" or text_lower in ("skip", "lewat", "tidak", "lanjut"):
            self.pending_prayer = "Tanpa pesan."
        else:
            self.pending_prayer = text.strip()
            
        self.state = STATE_CONFIRM
        return (
            f"Pesan dicatat: *\"{self.pending_prayer}\"*\n\n"
            f"Silakan pilih metode pembayaran Anda dengan mengetik salah satu opsi:\n"
            f"- **GoPay**\n"
            f"- **OVO**\n"
            f"- **ShopeePay**\n"
            f"- **DANA**\n"
            f"- **Transfer BCA** / **Mandiri**\n\n"
            f"Atau ketik **batal** untuk membatalkan donasi."
        )

    def _from_confirm(self, intent: str, text: str) -> str:
        text_lower = text.lower().strip()

        if intent == "NO" or "batal" in text_lower:
            self.pending_campaign = None
            self.pending_amount = None
            self.pending_prayer = None
            self.pending_payment = None
            self.state = STATE_ACTIVE
            return "Proses donasi dibatalkan. Ada yang bisa saya bantu lainnya?"

        # Match payment methods
        payment_methods = [
            "gopay", "ovo", "shopeepay", "dana", "bca", "mandiri", "bri", "bni",
        ]
        selected_payment = None
        for pm in payment_methods:
            if pm in text_lower:
                selected_payment = pm.upper()
                break

        if selected_payment:
            self.pending_payment = selected_payment
            campaign = self.pending_campaign
            amount = self.pending_amount
            prayer = self.pending_prayer

            # Insert to DB (this updates campaign collected amount as well)
            trx_id = self.engine.insert_donation(
                username=self.username,
                campaign_code=campaign["code"],
                amount=amount,
                payment_method=selected_payment,
                prayer=prayer
            )

            # Get updated campaign data
            updated_campaign = self.engine.get_campaign_exact(campaign["code"])
            percentage = min(int((updated_campaign["collected"] / updated_campaign["target"]) * 100), 100)

            # Reset state
            self.pending_campaign = None
            self.pending_amount = None
            self.pending_prayer = None
            self.pending_payment = None
            self.state = STATE_ACTIVE

            # Generate QR Code URL for Payment
            qr_data = f"ayobantu.com/pay/{trx_id}?amount={amount}"
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={urllib.parse.quote(qr_data)}&color=1A1A2E"

            return (
                f"**Donasi Berhasil Diproses! Terima Kasih Orang Baik!**\n\n"
                f"Bantuan Anda sangat berarti. Silakan selesaikan pembayaran Anda atau simpan bukti ini:\n\n"
                f"![QRIS Pembayaran]({qr_url})\n\n"
                f"**KUITANSI DIGITAL AYOBANTU**\n"
                f"• Kampanye: **{updated_campaign['title']}**\n"
                f"• Nominal: **Rp {amount:,}**\n"
                f"• Pembayaran: **{selected_payment} (Lunas)**\n"
                f"• Doa: *{prayer}*\n"
                f"• Kode Transaksi: `{trx_id}`\n\n"
                f"**Status Progres Kampanye Sekarang:**\n"
                f"Total Terkumpul: **Rp {updated_campaign['collected']:,}** ({percentage}% dari target)\n\n"
                f"Donasi ini otomatis tercatat di akun profil Anda. Kapan pun Anda ingin berbagi kembali, saya siap membantu."
            )

        if intent == "YES" or text_lower in ("ya", "lanjut", "oke", "siap"):
            return "Silakan ketik metode pembayaran yang Anda inginkan (contoh: **GoPay**, **OVO**, **DANA**, atau **BCA**)."

        return (
            "Mohon ketik metode pembayaran Anda yang sah untuk menyelesaikan donasi:\n"
            "- **GoPay**, **OVO**, **ShopeePay**, **DANA**, atau **BCA**\n"
            "Atau ketik **batal** untuk membatalkan."
        )

    def _handle_search(self, text: str) -> str:
        campaigns = self.engine.find_campaigns(text)
        if campaigns:
            lines = [f"Ditemukan **{len(campaigns)}** kampanye sosial yang cocok:\n"]
            for c in campaigns[:5]: # Tampilkan max 5 agar tidak kepanjangan
                lines.append(self.engine.format_campaign_card(c))
                lines.append("---")
            if len(campaigns) > 5:
                lines.append(f"...dan {len(campaigns) - 5} kampanye lainnya.")
                
            lines.append(
                "Ketik **donasi [nama kampanye]** untuk mulai menyumbang pada program tersebut."
            )
            return "\n".join(lines)
        return (
            self.engine.format_catalog()
            + "\n\nTidak ditemukan kampanye spesifik untuk kata kunci tersebut. Berikut daftar kampanye aktif kami."
        )
