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

        # Filter berdasarkan rating dan harga
        st.subheader("Filter Restoran")
        rating_filter = st.slider('Pilih Rating Minimum', min_value=0.0, max_value=5.0, value=4.5, step=0.1)
        price_filter = st.slider('Pilih Harga Maksimal (Rp)', min_value=0, max_value=1000000, value=100000, step=1000)

        # Filter data
        filtered_data = data[(data['Rating Toko'] >= rating_filter) &
                             (data['Harga Rata-Rata Makanan di Toko (Rp)'] <= price_filter)]

        # Menampilkan hasil filter
        st.subheader("Restoran yang Direkomendasikan:")
        if filtered_data.empty:
            st.write("Tidak ada restoran yang memenuhi kriteria. Silakan ubah filter Anda.")
        else:
            st.write(filtered_data[['Nama Restoran', 'Harga Rata-Rata Makanan di Toko (Rp)', 'Rating Toko']])

            # Menghitung cosine similarity hanya untuk data yang difilter
            filtered_features = filtered_data[['Preferensi Makanan', 'Lokasi Restoran',
                                               'Harga Rata-Rata Makanan di Toko (Rp)', 'Rating Toko', 'Jenis Suasana']]
            similarity_matrix = cosine_similarity(filtered_features)

            # Pilih restoran dari data yang difilter
            restoran_terpilih = st.selectbox("Pilih Restoran untuk Melihat Rekomendasi Terdekat",
                                             filtered_data['Nama Restoran'])

            # Mendapatkan indeks restoran yang dipilih dalam filtered data
            index_restoran = filtered_data[filtered_data['Nama Restoran'] == restoran_terpilih].index[0]

            # Menampilkan restoran mirip dari data yang difilter
            similar_restaurants = sorted(enumerate(similarity_matrix[index_restoran]), key=lambda x: x[1], reverse=True)[1:6]
            st.subheader("Restoran Mirip dengan yang Anda Pilih:")
            for i in similar_restaurants:
                restaurant_index = i[0]  # Indeks dalam filtered data
                restaurant_name = filtered_data.iloc[restaurant_index]['Nama Restoran']
                st.write(f"- {restaurant_name}")
except FileNotFoundError:
    st.error("File 'ds.xlsx' tidak ditemukan. Pastikan file ada di direktori yang sama dengan aplikasi.")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
