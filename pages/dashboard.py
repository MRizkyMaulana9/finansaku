import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def show():
    st.header("📊 Dashboard Keuangan")
    st.caption("Ringkasan lengkap kondisi keuangan Anda")

    fm = st.session_state.finance_manager

    total_in = fm.total_pemasukan()
    total_out = fm.total_pengeluaran()
    saldo = fm.saldo()
    rasio = (total_out / total_in * 100) if total_in > 0 else 0

    # ── Metric Cards ──
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="💰 Total Pemasukan",
            value=f"Rp {total_in:,.0f}"
        )
    with col2:
        st.metric(
            label="💸 Total Pengeluaran",
            value=f"Rp {total_out:,.0f}"
        )
    with col3:
        st.metric(
            label="🏦 Saldo",
            value=f"Rp {saldo:,.0f}",
            delta=f"{'Surplus' if saldo >= 0 else 'Defisit'}",
            delta_color="normal" if saldo >= 0 else "inverse"
        )
    with col4:
        st.metric(
            label="📉 Rasio Pengeluaran",
            value=f"{rasio:.1f}%",
            delta="Sehat" if rasio <= 70 else "Perlu Perhatian",
            delta_color="normal" if rasio <= 70 else "inverse"
        )

    st.divider()

    if not fm.get_semua_transaksi():
        st.info("📝 Belum ada data transaksi. Mulai catat pemasukan dan pengeluaran Anda di menu sebelah kiri!")
        return

    # ── Charts Row ──
    col_left, col_right = st.columns(2)

    with col_left:
        # Pie Chart - Pengeluaran per Kategori
        per_kat = fm.pengeluaran_per_kategori()
        if per_kat:
            st.subheader("🍩 Distribusi Pengeluaran")
            df_pie = pd.DataFrame({
                "Kategori": list(per_kat.keys()),
                "Jumlah": list(per_kat.values())
            })
            fig_pie = px.pie(
                df_pie,
                values="Jumlah",
                names="Kategori",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(
                textposition="inside",
                textinfo="percent+label",
                textfont_size=11
            )
            fig_pie.update_layout(
                showlegend=False,
                margin=dict(t=20, b=20, l=20, r=20),
                height=380
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Belum ada data pengeluaran.")

    with col_right:
        # Pie Chart - Pemasukan per Sumber
        per_src = fm.pemasukan_per_sumber()
        if per_src:
            st.subheader("💵 Sumber Pemasukan")
            df_src = pd.DataFrame({
                "Sumber": list(per_src.keys()),
                "Jumlah": list(per_src.values())
            })
            fig_src = px.pie(
                df_src,
                values="Jumlah",
                names="Sumber",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_src.update_traces(
                textposition="inside",
                textinfo="percent+label",
                textfont_size=11
            )
            fig_src.update_layout(
                showlegend=False,
                margin=dict(t=20, b=20, l=20, r=20),
                height=380
            )
            st.plotly_chart(fig_src, use_container_width=True)
        else:
            st.info("Belum ada data pemasukan.")

    # ── Tren Bulanan ──
    tren = fm.tren_bulanan()
    if not tren.empty:
        st.subheader("📈 Tren Bulanan")
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=tren["Bulan"],
            y=tren["Pemasukan"],
            name="Pemasukan",
            marker_color="#2ecc71"
        ))
        fig_bar.add_trace(go.Bar(
            x=tren["Bulan"],
            y=tren["Pengeluaran"],
            name="Pengeluaran",
            marker_color="#e74c3c"
        ))
        fig_bar.update_layout(
            barmode="group",
            xaxis_title="Bulan",
            yaxis_title="Jumlah (Rp)",
            height=400,
            margin=dict(t=20, b=40, l=40, r=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── Health Indicator ──
    st.subheader("🏥 Indikator Kesehatan Keuangan")

    if rasio <= 50:
        status = "🟢 Sangat Sehat"
        msg = "Excellent! Anda menggunakan kurang dari 50% pemasukan. Terus pertahankan!"
        color = "green"
    elif rasio <= 70:
        status = "🟡 Sehat"
        msg = "Bagus! Pengeluaran Anda masih dalam batas wajar. Coba tingkatkan tabungan."
        color = "orange"
    elif rasio <= 90:
        status = "🟠 Perlu Perhatian"
        msg = "Hati-hati! Pengeluaran Anda cukup tinggi. Pertimbangkan untuk mengurangi pengeluaran non-esensial."
        color = "orange"
    else:
        status = "🔴 Kritis"
        msg = "Peringatan! Pengeluaran melebihi atau hampir sama dengan pemasukan. Perlu evaluasi segera."
        color = "red"

    st.markdown(f"""
    <div style="padding: 1rem; border-radius: 0.5rem; border-left: 4px solid {color}; background-color: rgba(0,0,0,0.05);">
        <h3 style="margin:0">{status}</h3>
        <p style="margin:0.5rem 0 0 0">{msg}</p>
    </div>
    """, unsafe_allow_html=True)


show()
