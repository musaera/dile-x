import streamlit as st
import pandas as pd

def show_history(data):
    if not data:
        st.warning("Belum ada data.")
        return
    
    df = pd.DataFrame(data)
    # Mengonversi timestamp menjadi format datetime yang lebih mudah dibaca
    df['timestamp'] = pd.to_datetime(df['timestamp'].apply(lambda t: t.get('$date', '')))
    
    df['jam'] = df['timestamp'].dt.hour
    opsi_jam = ['All'] + sorted(df['jam'].unique().tolist())
    jam_terpilih = st.selectbox("Pilih jam untuk ditampilkan:", opsi_jam)
    if jam_terpilih != 'All':
        df = df[df['jam'] == jam_terpilih]
    
    df['timestamp'] = df['timestamp'].dt.strftime('%d-%m-%Y %H:%M:%S')

    st.subheader("📋 History Data")
    st.dataframe(df[['jumlah_orang', 'latitude', 'longitude', 'timestamp']])
