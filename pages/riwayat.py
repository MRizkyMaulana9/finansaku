import streamlit as st
import pandas as pd


def show():
    st.header("📋 Riwayat Transaksi")
    st.caption("Lihat dan kelola semua transaksi keuangan Anda")

    fm = st.session_state.finance_manager

    if not fm.get_semua_transaksi():
        st.info("📝 Belum ada transaksi. Mulai catat pemasukan dan pengeluaran Anda!")
        return

    # ── Filters ──
    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        filter_tipe = st.selectbox(
            "🔍 Filter Tipe",
            ["Semua", "Pemasukan", "Pengeluaran"]
        )

    with col_f2:
        all_categories = sorted(set(
            t["kategori"] for t in fm.get_semua_transaksi()
        ))
        filter_kategori = st.selectbox(
            "📂 Filter Kategori",
            ["Semua"] + all_categories
        )

    with col_f3:
        sort_order = st.selectbox(
            "📊 Urutkan",
            ["Terbaru", "Terlama", "Terbesar", "Terkecil"]
        )

    # ── Apply Filters ──
    transactions = fm.get_semua_transaksi().copy()

    if filter_tipe == "Pemasukan":
        transactions = [t for t in transactions if t["tipe"] == "pemasukan"]
    elif filter_tipe == "Pengeluaran":
        transactions = [t for t in transactions if t["tipe"] == "pengeluaran"]

    if filter_kategori != "Semua":
        transactions = [t for t in transactions if t["kategori"] == filter_kategori]

    # Sort
    if sort_order == "Terbaru":
        transactions = sorted(transactions, key=lambda x: x["tanggal"], reverse=True)
    elif sort_order == "Terlama":
        transactions = sorted(transactions, key=lambda x: x["tanggal"])
    elif sort_order == "Terbesar":
        transactions = sorted(transactions, key=lambda x: x["jumlah"], reverse=True)
    elif sort_order == "Terkecil":
        transactions = sorted(transactions, key=lambda x: x["jumlah"])

    st.divider()

    # ── Summary ──
    st.markdown(f"Menampilkan **{len(transactions)}** transaksi")

    # ── Transaction Cards ──
    for t in transactions:
        tipe_icon = "📥" if t["tipe"] == "pemasukan" else "📤"
        tipe_color = "green" if t["tipe"] == "pemasukan" else "red"
        tipe_label = "Pemasukan" if t["tipe"] == "pemasukan" else "Pengeluaran"

        with st.container():
            col1, col2, col3, col4 = st.columns([0.5, 2.5, 2, 1])

            with col1:
                st.markdown(f"### {tipe_icon}")

            with col2:
                st.markdown(f"**{t['kategori']}**")
                catatan = t.get('catatan', '') or ''
                if catatan:
                    st.caption(catatan)

            with col3:
                prefix = "+" if t["tipe"] == "pemasukan" else "-"
                st.markdown(
                    f"<span style='color:{tipe_color};font-weight:bold;font-size:1.1em'>"
                    f"{prefix} Rp {t['jumlah']:,.0f}</span>",
                    unsafe_allow_html=True
                )
                st.caption(f"📅 {t['tanggal']}")

            with col4:
                if st.button("🗑️", key=f"del_{t['id']}", help="Hapus transaksi"):
                    fm.hapus_transaksi(t["id"])
                    st.rerun()

            st.divider()

    # ── Export ──
    st.subheader("📥 Export Data")
    col_e1, col_e2 = st.columns(2)

    with col_e1:
        csv_data = fm.export_csv()
        st.download_button(
            label="📄 Download CSV",
            data=csv_data,
            file_name="transaksi_keuangan.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col_e2:
        import json
        json_data = json.dumps(fm.get_semua_transaksi(), ensure_ascii=False, indent=2, default=str)
        st.download_button(
            label="📋 Download JSON",
            data=json_data,
            file_name="transaksi_keuangan.json",
            mime="application/json",
            use_container_width=True
        )


show()
