import streamlit as st
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from finance_manager import FinanceManager

# ── Page Config ──
st.set_page_config(
    page_title="FinanSaku - Keuangan Pribadi",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ──
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        text-align: center;
        padding: 1rem 0;
    }
    .main-header h1 {
        background: linear-gradient(90deg, #2ecc71, #3498db);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
    }
    .main-header p {
        color: #7f8c8d;
        font-size: 1.1rem;
    }

    /* Metric card styling */
    [data-testid="stMetricValue"] {
        font-size: 1.3rem;
        font-weight: 700;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }

    /* Button styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #2ecc71, #27ae60);
        border: none;
        font-weight: 600;
    }

    /* Chat message styling */
    [data-testid="stChatMessage"] {
        border-radius: 12px;
        margin-bottom: 0.5rem;
    }

    /* Divider */
    hr {
        border-color: rgba(255,255,255,0.1);
    }

    /* Form styling */
    [data-testid="stForm"] {
        border: 1px solid rgba(46, 204, 113, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Initialize Finance Manager ──
if "finance_manager" not in st.session_state:
    st.session_state.finance_manager = FinanceManager()

fm = st.session_state.finance_manager

# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <h1 style='font-size:2rem; margin:0;'>💰 FinanSaku</h1>
        <p style='color:#95a5a6; margin:0.5rem 0 0 0; font-size:0.9rem;'>Asisten Keuangan Pribadimu</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Quick Summary
    st.markdown("### 📊 Ringkasan")
    total_in = fm.total_pemasukan()
    total_out = fm.total_pengeluaran()
    saldo = fm.saldo()

    st.metric("Pemasukan", f"Rp {total_in:,.0f}")
    st.metric("Pengeluaran", f"Rp {total_out:,.0f}")

    saldo_color = "green" if saldo >= 0 else "red"
    st.markdown(
        f"<div style='text-align:center; padding:0.75rem; border-radius:8px; "
        f"background:linear-gradient(135deg, rgba(46,204,113,0.2), rgba(52,152,219,0.2)); "
        f"margin:0.5rem 0;'>"
        f"<p style='margin:0; color:#95a5a6; font-size:0.8rem;'>Saldo</p>"
        f"<p style='margin:0; color:{saldo_color}; font-size:1.5rem; font-weight:700;'>"
        f"Rp {saldo:,.0f}</p></div>",
        unsafe_allow_html=True
    )

    st.divider()
    st.caption("© 2024 FinanSaku | AI-Powered Finance")

# ── Navigation ──
dashboard_page = st.Page("pages/dashboard.py", title="Dashboard", icon="📊", default=True)
pemasukan_page = st.Page("pages/pemasukan.py", title="Pemasukan", icon="📥")
pengeluaran_page = st.Page("pages/pengeluaran.py", title="Pengeluaran", icon="📤")
ai_chat_page = st.Page("pages/ai_chat.py", title="AI Advisor", icon="🤖")
riwayat_page = st.Page("pages/riwayat.py", title="Riwayat", icon="📋")

pg = st.navigation({
    "Utama": [dashboard_page],
    "Transaksi": [pemasukan_page, pengeluaran_page],
    "Tools": [ai_chat_page, riwayat_page]
})

pg.run()
