import streamlit as st
import pandas as pd
import altair as alt

def show_statistik(data):
    if not data:
        st.warning("Tidak ada data untuk dianalisis.")
        return

    df = pd.DataFrame(data)
    # Konversi timestamp kalau belum
    df['timestamp'] = pd.to_datetime(df['timestamp'].apply(lambda t: t.get('$date', '')))
    df['tanggal'] = df['timestamp'].dt.date
    df['jam'] = df['timestamp'].dt.hour

    st.subheader("📊 Statistik Deteksi")

    # 📌 Total deteksi per hari
    total_per_hari = df.groupby('tanggal')['jumlah_orang'].sum().reset_index()
    total_per_hari.columns = ['Tanggal', 'Total Deteksi']
    st.write("### Total Deteksi per Hari")
    st.dataframe(total_per_hari)

    # 📌 Rata-rata jumlah orang per jam (semua hari)
    jumlah_per_jam = df.groupby('jam')['jumlah_orang'].sum().reset_index()
    jumlah_per_jam.columns = ['Jam', 'Banyak Orang Terdeteksi']
    st.write(jumlah_per_jam)
    st.bar_chart(jumlah_per_jam.set_index('Jam'))

    # 📌 Tren harian (chart)
    st.write("### Grafik Tren Deteksi Harian")
    chart = alt.Chart(total_per_hari).mark_line(point=True).encode(
        x='Tanggal:T',
        y='Total Deteksi:Q'
    ).properties(width='container')
    st.altair_chart(chart, use_container_width=True)
