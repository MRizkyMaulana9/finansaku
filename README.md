# 💰 FinanSaku - Chatbot Keuangan Pribadi

Aplikasi chatbot keuangan pribadi berbasis AI yang membantu Anda mengelola pemasukan, pengeluaran, dan memberikan saran keuangan yang cerdas.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)

## ✨ Fitur

- 📊 **Dashboard** - Visualisasi lengkap kondisi keuangan (pie chart, bar chart, tren bulanan)
- 📥 **Catat Pemasukan** - Input dan tracking semua sumber pemasukan
- 📤 **Catat Pengeluaran** - Kategorisasi dan pencatatan pengeluaran
- 🤖 **AI Advisor** - Chatbot AI (Google Gemini) untuk konsultasi keuangan
- 📋 **Riwayat** - Lihat, filter, dan export data transaksi

## 🚀 Cara Menjalankan Lokal

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/finansaku.git
cd finansaku
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup API Key
Buat file `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

Dapatkan API key gratis di [Google AI Studio](https://aistudio.google.com/apikey).

### 4. Jalankan Aplikasi
```bash
streamlit run app.py
```

## ☁️ Deploy ke Streamlit Cloud

1. Push kode ke GitHub
2. Buka [share.streamlit.io](https://share.streamlit.io)
3. Connect repository Anda
4. Set `GEMINI_API_KEY` di Settings → Secrets:
   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   ```
5. Klik Deploy!

## 🏗️ Struktur Project

```
finansaku/
├── app.py                    # Main Streamlit app
├── finance_manager.py        # Finance data management
├── ai_advisor.py             # AI chatbot module (Gemini)
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── README.md                # Dokumentasi
├── .streamlit/
│   ├── config.toml          # Streamlit theme
│   └── secrets.toml         # API keys (gitignored)
├── pages/
│   ├── dashboard.py         # Dashboard & visualisasi
│   ├── pemasukan.py         # Form input pemasukan
│   ├── pengeluaran.py       # Form input pengeluaran
│   ├── ai_chat.py           # AI chatbot interface
│   └── riwayat.py           # Riwayat transaksi
└── data/
    └── transactions.json    # Data transaksi (gitignored)
```

## 🤖 AI Configuration

| Parameter | Value |
|-----------|-------|
| Model | Gemini 2.0 Flash |
| Temperature | 0.7 |
| Max Tokens | 1024 |
| Top P | 0.9 |
| Role | Financial Advisor Indonesia |

## 📝 Lisensi

MIT License - Silakan gunakan dan modifikasi sesuai kebutuhan.
