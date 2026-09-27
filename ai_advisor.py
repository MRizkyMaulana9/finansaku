import streamlit as st
from groq import Groq
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


def get_groq_client():
    """Inisialisasi dan return Groq client."""
    try:
        api_key = st.secrets.get("GROQ_API_KEY", "")
        if not api_key:
            return None
        client = Groq(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"Error inisialisasi Groq: {e}")
        return None


MODEL_NAME = None


def get_available_model(client):
    """Cari model yang tersedia di akun Groq."""
    global MODEL_NAME
    if MODEL_NAME:
        return MODEL_NAME

    # Prioritas model dari yang terbaik (2026)
    preferred = [
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "llama-3.3-70b-versatile",
        "openai/gpt-oss-20b",
        "llama-3.1-8b-instant",
        "gemma2-9b-it",
        "mixtral-8x7b-32768",
    ]

    try:
        available = client.models.list()
        available_ids = [m.id for m in available.data]

        for model in preferred:
            if model in available_ids:
                MODEL_NAME = model
                return MODEL_NAME
    except Exception:
        pass

    # Fallback
    MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"
    return MODEL_NAME


def init_chat_session(client, financial_context: str = ""):
    """Inisialisasi chat messages dengan konteks keuangan."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    if financial_context:
        messages.append({
            "role": "system",
            "content": f"Berikut data keuangan pengguna saat ini:\n\n{financial_context}\n\n"
                       f"Gunakan data ini untuk memberikan saran yang personal dan relevan. "
                       f"Jangan sebutkan bahwa kamu menerima data ini kecuali pengguna bertanya."
        })

    return messages


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


def get_ai_response(client, messages: list, user_message: str):
    """Dapatkan respons AI dari Groq (streaming)."""
    try:
        messages.append({"role": "user", "content": user_message})
        response = client.chat.completions.create(
            model=get_available_model(client),
            messages=messages,
            temperature=0.7,
            max_completion_tokens=1024,
            top_p=0.9,
            stream=True,
        )
        return response
    except Exception as e:
        return f"Maaf, terjadi kesalahan: {str(e)}"


def get_quick_analysis(client, ringkasan: dict) -> str:
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
        response = client.chat.completions.create(
            model=get_available_model(client),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_completion_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Tidak dapat menghasilkan analisis: {str(e)}"
