import sklearn
import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
data = pd.read_excel('ds.xlsx')  # Ganti dengan path file dataset

# 1. Label Encoding untuk Preferensi Makanan dan Jenis Suasana
label_encoder = LabelEncoder()
data['Preferensi Makanan'] = label_encoder.fit_transform(data['Preferensi Makanan'])
data['Jenis Suasana'] = label_encoder.fit_transform(data['Jenis Suasana'])

data = data[['Nama Restoran', 'Preferensi Makanan', 'Harga Rata-Rata Makanan di Toko (Rp)', 'Rating Toko', 'Jenis Suasana']]

# Menghitung cosine similarity berdasarkan fitur-fitur yang ada
features = data[['Preferensi Makanan', 'Harga Rata-Rata Makanan di Toko (Rp)', 'Rating Toko', 'Jenis Suasana']]
similarity_matrix = cosine_similarity(features)

# Menampilkan dataset setelah encoding
st.subheader("Dataset dengan Encoding")
st.write(data)

# Mapping untuk Preferensi Makanan
preferensi_mapping = {
    0: '0 : Chinese',
    1: '1 : Indonesia',
    2: '2 : Japanese',
    3: '3 : Middle Eastern',
    4: '4 : Western'
}

# Mapping untuk Jenis Suasana
suasana_mapping = {
    0: '0 : Santai',
    1: '1 : Formal'
}

# Pilihan filter untuk Preferensi Makanan, Lokasi Restoran, Jenis Suasana, Harga, dan Rating
preferensi_filter = st.checkbox("Filter Preferensi Makanan")
harga_filter = st.checkbox("Filter Harga")
rating_filter = st.checkbox("Filter Rating")
jenis_suasana_filter = st.checkbox("Filter Jenis Suasana")

# Input untuk filter
if any([preferensi_filter, harga_filter, rating_filter,jenis_suasana_filter]):
    data_filtered = data.copy()
    columns_to_display = ['Nama Restoran']
    
    if preferensi_filter:
        # Dropdown untuk Preferensi Makanan
        preferensi_value = st.selectbox("Pilih Preferensi Makanan", options=list(preferensi_mapping.values()))
        # Mengambil nilai encoded dari pilihan dropdown
        preferensi_encoded = list(preferensi_mapping.keys())[list(preferensi_mapping.values()).index(preferensi_value)]
        data_filtered = data_filtered[data_filtered['Preferensi Makanan'] == preferensi_encoded]
        columns_to_display.append('Preferensi Makanan')
    
    if harga_filter:
        price_max = st.number_input("Masukkan Harga Maksimal (Rp)", min_value=0, value=50000, step=1000)
        data_filtered = data_filtered[data_filtered['Harga Rata-Rata Makanan di Toko (Rp)'] <= price_max]
        columns_to_display.append('Harga Rata-Rata Makanan di Toko (Rp)')
    
    if rating_filter:
        rating_value = st.slider("Pilih Rating Restoran", min_value=0.0, max_value=5.0, value=0.0, step=0.1)
        data_filtered = data_filtered[data_filtered['Rating Toko'] == rating_value]
        columns_to_display.append('Rating Toko')

    if jenis_suasana_filter:
        # Dropdown untuk Jenis Suasana
        suasana_value = st.selectbox("Pilih Jenis Suasana", options=list(suasana_mapping.values()))
        # Mengambil nilai encoded dari pilihan dropdown
        suasana_encoded = list(suasana_mapping.keys())[list(suasana_mapping.values()).index(suasana_value)]
        data_filtered = data_filtered[data_filtered['Jenis Suasana'] == suasana_encoded]
        columns_to_display.append('Jenis Suasana')

    # Menampilkan hasil filter
    st.subheader("Hasil Filter:")
    if not data_filtered.empty:
        st.write(data_filtered[columns_to_display])
    else:
        st.write("Tidak ada data yang memenuhi kriteria filter.")
else:
    st.write("Silakan pilih setidaknya satu filter untuk melihat hasil.")
