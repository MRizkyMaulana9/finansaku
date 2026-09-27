import streamlit as st
import google.generativeai as genai
from typing import Optional


SYSTEM_PROMPT = """Kamu adalah **FinanSaku AI** — asisten keuangan pribadi yang cerdas, ramah, dan profesional.

Peranmu:
- Membantu pengguna mengelola keuangan pribadi mereka
- Memberikan saran penghematan dan pengelolaan uang yang praktis
- Menganalisis pola pengeluaran dan memberikan rekomendasi
- Membantu membuat budget dan perencanaan keuangan
- Memberikan tips investasi dasar dan tabungan
- Mengevaluasi kesehatan keuangan berdasarkan data pengguna

Aturan:
1. Selalu jawab dalam Bahasa Indonesia yang sopan dan mudah dipahami
2. Gunakan emoji secukupnya untuk membuat percakapan lebih menarik
3. Berikan saran yang spesifik dan actionable, bukan generik
4. Jika pengguna memberikan data keuangan, analisis dengan detail
5. Gunakan format yang rapi (bullet points, numbering) untuk saran
6. Jangan memberikan saran investasi yang terlalu spesifik (saham tertentu), fokus pada prinsip umum
7. Selalu dorong kebiasaan keuangan yang sehat
8. Jika ditanya di luar topik keuangan, arahkan kembali ke topik keuangan dengan sopan
9. Gunakan konteks data keuangan pengguna yang diberikan untuk personalisasi saran
10. Format mata uang dalam Rupiah (Rp)

Gaya komunikasi:
- Ramah tapi profesional
- Menggunakan analogi sederhana untuk konsep keuangan
- Memberikan motivasi dan apresiasi atas langkah keuangan yang baik
- Jujur jika ada pola pengeluaran yang perlu diperbaiki
"""


def get_gemini_model():
    """Inisialisasi dan return model Gemini."""
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
        if not api_key:
            return None

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=SYSTEM_PROMPT,
            generation_config=genai.GenerationConfig(
                temperature=0.7,
                top_p=0.9,
                max_output_tokens=1024,
            )
        )
        return model
    except Exception as e:
        st.error(f"Error inisialisasi Gemini: {e}")
        return None


def init_chat_session(model, financial_context: str = ""):
    """Inisialisasi chat session dengan konteks keuangan."""
    chat = model.start_chat(history=[])

    if financial_context:
        # Kirim konteks keuangan sebagai pesan awal (tidak ditampilkan ke user)
        intro = f"""Berikut adalah data keuangan pengguna saat ini:

{financial_context}

Gunakan data ini untuk memberikan saran yang personal dan relevan.
Jangan sebutkan bahwa kamu menerima data ini kecuali pengguna bertanya tentang keuangan mereka.
Mulai dengan menyapa pengguna dan tanyakan apa yang bisa kamu bantu."""
        chat.send_message(intro)

    return chat


def format_financial_context(ringkasan: dict) -> str:
    """Format ringkasan keuangan menjadi konteks untuk AI."""
    if not ringkasan or ringkasan.get("jumlah_transaksi", 0) == 0:
        return "Pengguna belum memiliki data transaksi."

    context = f"""📊 RINGKASAN KEUANGAN PENGGUNA:
- Total Pemasukan: Rp {ringkasan['total_pemasukan']:,.0f}
- Total Pengeluaran: Rp {ringkasan['total_pengeluaran']:,.0f}
- Saldo Saat Ini: Rp {ringkasan['saldo']:,.0f}
- Rasio Pengeluaran: {ringkasan['rasio_pengeluaran']}% dari pemasukan
- Jumlah Transaksi: {ringkasan['jumlah_transaksi']}
- Kategori Pengeluaran Terbesar: {ringkasan['kategori_terbesar']}

Detail Pengeluaran per Kategori:"""

    for kat, jumlah in ringkasan.get("pengeluaran_per_kategori", {}).items():
        context += f"\n- {kat}: Rp {jumlah:,.0f}"

    context += "\n\nDetail Pemasukan per Sumber:"
    for src, jumlah in ringkasan.get("pemasukan_per_sumber", {}).items():
        context += f"\n- {src}: Rp {jumlah:,.0f}"

    return context


def get_ai_response(chat_session, user_message: str) -> str:
    """Dapatkan respons AI dari chat session (streaming)."""
    try:
        response = chat_session.send_message(user_message, stream=True)
        return response
    except Exception as e:
        return f"Maaf, terjadi kesalahan: {str(e)}"


def get_quick_analysis(model, ringkasan: dict) -> str:
    """Dapatkan analisis cepat keuangan dari AI."""
    if not ringkasan or ringkasan.get("jumlah_transaksi", 0) == 0:
        return "Belum ada data transaksi untuk dianalisis. Mulai catat pemasukan dan pengeluaran Anda!"

    context = format_financial_context(ringkasan)
    prompt = f"""{context}

Berikan analisis singkat (3-5 poin) tentang kesehatan keuangan pengguna ini.
Format dalam bullet points dengan emoji.
Fokus pada:
1. Status kesehatan keuangan (baik/perlu perbaikan)
2. Satu hal positif
3. Satu area yang perlu diperbaiki
4. Satu saran konkret"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Tidak dapat menghasilkan analisis: {str(e)}"
