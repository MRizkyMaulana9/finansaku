import streamlit as st
from datetime import date
from finance_manager import KATEGORI_PENGELUARAN


def show():
    st.header("📤 Catat Pengeluaran")
    st.caption("Catat dan pantau semua pengeluaran Anda")

    fm = st.session_state.finance_manager

    # ── Quick Stats ──
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💸 Total Pengeluaran", f"Rp {fm.total_pengeluaran():,.0f}")
    with col2:
        st.metric("📋 Jumlah Transaksi", f"{len(fm.get_pengeluaran())}")
    with col3:
        per_kat = fm.pengeluaran_per_kategori()
        terbesar = max(per_kat, key=per_kat.get) if per_kat else "-"
        st.metric("🔝 Kategori Terbesar", terbesar[:20] if len(terbesar) > 20 else terbesar)

    st.divider()

    # ── Form Input ──
    st.subheader("➕ Tambah Pengeluaran Baru")

    with st.form("form_pengeluaran", clear_on_submit=True):
        col_a, col_b = st.columns(2)

        with col_a:
            jumlah = st.number_input(
                "💵 Jumlah (Rp)",
                min_value=0,
                step=5000,
                format="%d",
                help="Masukkan jumlah pengeluaran dalam Rupiah"
            )
            kategori = st.selectbox(
                "📂 Kategori Pengeluaran",
                options=KATEGORI_PENGELUARAN,
                help="Pilih kategori yang sesuai"
            )

        with col_b:
            tanggal = st.date_input(
                "📅 Tanggal",
                value=date.today(),
                max_value=date.today(),
                help="Tanggal transaksi"
            )
            catatan = st.text_input(
                "📝 Deskripsi (opsional)",
                placeholder="Contoh: Makan siang di restoran",
                help="Tambahkan deskripsi untuk referensi"
            )

        submitted = st.form_submit_button(
            "✅ Simpan Pengeluaran",
            use_container_width=True,
            type="primary"
        )

        if submitted:
            if jumlah <= 0:
                st.error("❌ Jumlah harus lebih dari 0!")
            else:
                fm.tambah_pengeluaran(
                    jumlah=jumlah,
                    kategori=kategori,
                    tanggal=str(tanggal),
                    catatan=catatan
                )
                st.success(f"✅ Pengeluaran Rp {jumlah:,.0f} untuk {kategori} berhasil dicatat!")
                st.snow()

    # ── Riwayat Pengeluaran Terakhir ──
    st.divider()
    st.subheader("📋 Pengeluaran Terakhir")

    pengeluaran_list = fm.get_pengeluaran()
    if pengeluaran_list:
        for t in reversed(pengeluaran_list[-5:]):
            with st.container():
                col_i, col_j, col_k = st.columns([2, 2, 1])
                with col_i:
                    st.markdown(f"**{t['kategori']}**")
                    st.caption(t.get('catatan', '-') or '-')
                with col_j:
                    st.markdown(f"💸 **Rp {t['jumlah']:,.0f}**")
                with col_k:
                    st.caption(t['tanggal'])
                st.divider()
    else:
        st.info("📝 Belum ada data pengeluaran. Mulai catat pengeluaran Anda!")


show()
