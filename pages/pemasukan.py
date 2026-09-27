import streamlit as st
from datetime import date, timedelta
from finance_manager import SUMBER_PEMASUKAN


def show():
    st.header("📥 Catat Pemasukan")
    st.caption("Catat semua sumber pemasukan Anda")

    fm = st.session_state.finance_manager

    # ── Quick Stats ──
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Total Pemasukan", f"Rp {fm.total_pemasukan():,.0f}")
    with col2:
        st.metric("📋 Jumlah Transaksi", f"{len(fm.get_pemasukan())}")
    with col3:
        avg = fm.total_pemasukan() / max(len(fm.get_pemasukan()), 1)
        st.metric("📊 Rata-rata", f"Rp {avg:,.0f}")

    st.divider()

    # ── Form Input ──
    st.subheader("➕ Tambah Pemasukan Baru")

    with st.form("form_pemasukan", clear_on_submit=True):
        col_a, col_b = st.columns(2)

        with col_a:
            jumlah = st.number_input(
                "💵 Jumlah (Rp)",
                min_value=0,
                step=10000,
                format="%d",
                help="Masukkan jumlah pemasukan dalam Rupiah"
            )
            sumber = st.selectbox(
                "📂 Sumber Pemasukan",
                options=SUMBER_PEMASUKAN,
                help="Pilih sumber pemasukan"
            )

        with col_b:
            tanggal = st.date_input(
                "📅 Tanggal",
                value=date.today(),
                max_value=date.today(),
                help="Tanggal pemasukan diterima"
            )
            catatan = st.text_input(
                "📝 Catatan (opsional)",
                placeholder="Contoh: Gaji bulan September",
                help="Tambahkan catatan untuk referensi"
            )

        submitted = st.form_submit_button(
            "✅ Simpan Pemasukan",
            use_container_width=True,
            type="primary"
        )

        if submitted:
            if jumlah <= 0:
                st.error("❌ Jumlah harus lebih dari 0!")
            else:
                fm.tambah_pemasukan(
                    jumlah=jumlah,
                    sumber=sumber,
                    tanggal=str(tanggal),
                    catatan=catatan
                )
                st.success(f"✅ Pemasukan Rp {jumlah:,.0f} dari {sumber} berhasil dicatat!")
                st.balloons()

    # ── Riwayat Pemasukan Terakhir ──
    st.divider()
    st.subheader("📋 Pemasukan Terakhir")

    pemasukan_list = fm.get_pemasukan()
    if pemasukan_list:
        for t in reversed(pemasukan_list[-5:]):
            with st.container():
                col_i, col_j, col_k = st.columns([2, 2, 1])
                with col_i:
                    st.markdown(f"**{t['kategori']}**")
                    st.caption(t.get('catatan', '-') or '-')
                with col_j:
                    st.markdown(f"💰 **Rp {t['jumlah']:,.0f}**")
                with col_k:
                    st.caption(t['tanggal'])
                st.divider()
    else:
        st.info("📝 Belum ada data pemasukan. Mulai catat pemasukan pertama Anda!")


show()
