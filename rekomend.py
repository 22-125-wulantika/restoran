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
        data = data[['Nama Restoran', 'Preferensi Makanan', 'Lokasi Restoran',
                     'Harga Rata-Rata Makanan di Toko (Rp)', 'Rating Toko', 'Jenis Suasana']]

        # Harga dan Rating dari data sebelumnya
        available_prices = [10000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000,
                            21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000,
                            31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000,
                            41000, 42000, 43000, 44000, 45000, 47000, 48000, 49000, 50000, 51000,
                            52000, 55000, 56000, 57000, 58000, 59000, 60000, 62000, 64000, 66000,
                            67000, 68000, 69000, 70000, 73000, 75000, 76000, 77000, 80000, 82000,
                            85000, 87000, 88000, 92000, 100000, 103000, 107000, 108000, 111000,
                            119000, 120000, 132000, 330000]
        available_ratings = [3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3,
                             4.4, 4.5, 4.6, 4.7, 4.8, 4.9]

        # Dropdown untuk memilih harga dan rating
        st.subheader("Pilih Kriteria Restoran:")
        selected_price = st.selectbox("Pilih Harga Maksimal (Rp)", options=available_prices)
        selected_rating = st.selectbox("Pilih Rating Minimum", options=available_ratings)

        # Filter data berdasarkan pilihan pengguna
        filtered_data = data[(data['Harga Rata-Rata Makanan di Toko (Rp)'] <= selected_price) &
                             (data['Rating Toko'] >= selected_rating)]

        # Menampilkan hasil filter
        st.subheader("Restoran yang Direkomendasikan:")
        if filtered_data.empty:
            st.write("Tidak ada restoran yang memenuhi kriteria.")
        else:
            st.write(filtered_data[['Nama Restoran', 'Harga Rata-Rata Makanan di Toko (Rp)', 'Rating Toko']])
except FileNotFoundError:
    st.error("File 'ds.xlsx' tidak ditemukan. Pastikan file ada di direktori yang sama dengan aplikasi.")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
