import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity

# Judul aplikasi
st.title("Sistem Rekomendasi Restoran")

# Membaca file dataset
try:
    # Membaca file Excel ds.xlsx
    data = pd.read_excel('ds.xlsx')

    # Validasi kolom
    required_columns = ['Nama Restoran', 'Preferensi Makanan', 'Lokasi Restoran',
                        'Harga Rata-Rata Makanan di Toko (Rp)', 'Rating Toko', 'Jenis Suasana']
    if not all(col in data.columns for col in required_columns):
        st.error("Dataset harus memiliki kolom berikut: " + ", ".join(required_columns))
    else:
        # Pratinjau data
        st.subheader("Pratinjau Dataset:")
        st.write(data.head())

        # 1. Label Encoding untuk Preferensi Makanan dan Jenis Suasana
        label_encoder = LabelEncoder()
        data['Preferensi Makanan'] = label_encoder.fit_transform(data['Preferensi Makanan'])
        data['Jenis Suasana'] = label_encoder.fit_transform(data['Jenis Suasana'])

        # 2. Menghapus satuan 'km' pada Lokasi Restoran
        data['Lokasi Restoran'] = data['Lokasi Restoran'].str.replace(' km', '').astype(float)

        # 3. Memastikan hanya kolom yang diperlukan
        features = data[['Preferensi Makanan', 'Lokasi Restoran',
                         'Harga Rata-Rata Makanan di Toko (Rp)', 'Rating Toko', 'Jenis Suasana']]

        # Menghitung cosine similarity berdasarkan fitur-fitur
        similarity_matrix = cosine_similarity(features)

        # Input manual untuk fitur
        st.subheader("Masukkan Kriteria Restoran yang Diinginkan:")
        preferensi_makanan = st.number_input("Preferensi Makanan (0-1 untuk encoding)", min_value=0, max_value=1)
        lokasi_restoran = st.number_input("Lokasi Restoran (dalam km)", min_value=0.0, step=0.1)
        harga_rata_rata = st.number_input("Harga Rata-Rata Makanan (Rp)", min_value=0, step=1000)
        rating_toko = st.slider("Rating Toko", min_value=0.0, max_value=5.0, step=0.1)
        jenis_suasana = st.number_input("Jenis Suasana (0-1 untuk encoding)", min_value=0, max_value=1)

        # Membuat fitur input user
        input_user = [[preferensi_makanan, lokasi_restoran, harga_rata_rata, rating_toko, jenis_suasana]]

        # Menghitung similarity dengan input user
        user_similarity = cosine_similarity(input_user, features)[0]

        # Mengurutkan restoran berdasarkan similarity
        sorted_indices = user_similarity.argsort()[::-1]

        # Menampilkan restoran yang sesuai
        st.subheader("Rekomendasi Restoran Berdasarkan Input Anda:")
        recommended_restaurants = data.iloc[sorted_indices].head(5)
        for idx, row in recommended_restaurants.iterrows():
            st.write(f"- {row['Nama Restoran']} (Rating: {row['Rating Toko']}, Harga: Rp{row['Harga Rata-Rata Makanan di Toko (Rp)']})")

except FileNotFoundError:
    st.error("File 'ds.xlsx' tidak ditemukan. Pastikan file ada di direktori yang sama dengan aplikasi.")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
