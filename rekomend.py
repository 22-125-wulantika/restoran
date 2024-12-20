import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity

# Judul aplikasi
st.title("Sistem Rekomendasi Restoran")

# Membaca file dataset
try:
    @st.cache_data
    def load_data():
        return pd.read_excel('ds.xlsx')

    data = load_data()

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
            st.write("Tidak ada restoran yang memenuhi kriteria.")
        else:
            st.write(filtered_data[['Nama Restoran', 'Harga Rata-Rata Makanan di Toko (Rp)', 'Rating Toko']])

            # Hitung cosine similarity ulang untuk data hasil filter
            features_filtered = filtered_data[['Preferensi Makanan', 'Lokasi Restoran',
                                               'Harga Rata-Rata Makanan di Toko (Rp)', 'Rating Toko', 'Jenis Suasana']]
            similarity_matrix_filtered = cosine_similarity(features_filtered)

            # Pilih restoran untuk melihat restoran terdekat
            restoran_terpilih = st.selectbox("Pilih Restoran untuk Melihat Rekomendasi Terdekat",
                                             filtered_data['Nama Restoran'].values)

            if restoran_terpilih:
                # Mendapatkan indeks restoran terpilih pada data hasil filter
                index_restoran_filtered = filtered_data[filtered_data['Nama Restoran'] == restoran_terpilih].index[0]

                # Mendapatkan rekomendasi restoran terdekat
                similar_restaurants = list(enumerate(similarity_matrix_filtered[index_restoran_filtered]))

                # Mengurutkan berdasarkan similarity dan memilih 5 teratas
                similar_restaurants = sorted(similar_restaurants, key=lambda x: x[1], reverse=True)[1:6]

                # Menampilkan restoran yang mirip
                st.subheader("Restoran Mirip dengan yang Anda Pilih:")
                for i in similar_restaurants:
                    restaurant_index_filtered = i[0]
                    restaurant_name_filtered = filtered_data.iloc[restaurant_index_filtered]['Nama Restoran']
                    st.write(f"- {restaurant_name_filtered}")
except FileNotFoundError:
    st.error("File 'ds.xlsx' tidak ditemukan. Pastikan file ada di direktori yang sama dengan aplikasi.")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
