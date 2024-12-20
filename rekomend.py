import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity

# Judul aplikasi
st.title("Rekomendasi Restoran Berdasarkan Fitur")

# Membaca file dataset
@st.cache_data
def load_data():
    return pd.read_excel('ds.xlsx')

try:
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

        # Preprocessing Data
        label_encoder = LabelEncoder()
        data['Preferensi Makanan'] = label_encoder.fit_transform(data['Preferensi Makanan'])
        data['Jenis Suasana'] = label_encoder.fit_transform(data['Jenis Suasana'])
        data['Lokasi Restoran'] = data['Lokasi Restoran'].str.replace(' km', '').astype(float)

        # Memastikan hanya kolom yang diperlukan untuk perhitungan
        features = data[['Preferensi Makanan', 'Lokasi Restoran',
                         'Harga Rata-Rata Makanan di Toko (Rp)', 'Rating Toko', 'Jenis Suasana']]

        # Menghitung cosine similarity berdasarkan fitur-fitur
        similarity_matrix = cosine_similarity(features)

        # Input dari pengguna
        st.subheader("Pilih Kriteria Restoran:")
        preferensi_makanan = st.selectbox("Preferensi Makanan:", data['Preferensi Makanan'].unique())
        jenis_suasana = st.selectbox("Jenis Suasana:", data['Jenis Suasana'].unique())
        lokasi = st.slider("Lokasi Restoran (km):", min_value=float(data['Lokasi Restoran'].min()),
                           max_value=float(data['Lokasi Restoran'].max()), value=float(data['Lokasi Restoran'].mean()))
        harga = st.slider("Harga Rata-Rata Makanan (Rp):", min_value=int(data['Harga Rata-Rata Makanan di Toko (Rp)'].min()),
                          max_value=int(data['Harga Rata-Rata Makanan di Toko (Rp)'].max()),
                          value=int(data['Harga Rata-Rata Makanan di Toko (Rp)'].mean()), step=1000)
        rating = st.slider("Rating Minimum:", min_value=0.0, max_value=5.0, value=4.5, step=0.1)

        # Membuat input kriteria sebagai vektor
        input_vector = [[preferensi_makanan, lokasi, harga, rating, jenis_suasana]]

        # Menghitung similarity antara input pengguna dengan data
        similarity_scores = cosine_similarity(input_vector, features)[0]

        # Menambahkan skor similarity ke dalam dataset
        data['Similarity'] = similarity_scores

        # Filter berdasarkan rating dan harga, kemudian urutkan berdasarkan similarity
        filtered_data = data[(data['Rating Toko'] >= rating) &
                             (data['Harga Rata-Rata Makanan di Toko (Rp)'] <= harga)]
        recommended_restaurants = filtered_data.sort_values(by='Similarity', ascending=False).head(5)

        # Menampilkan hasil rekomendasi
        st.subheader("Restoran yang Direkomendasikan:")
        if recommended_restaurants.empty:
            st.write("Tidak ada restoran yang sesuai dengan kriteria Anda.")
        else:
            st.write(recommended_restaurants[['Nama Restoran', 'Harga Rata-Rata Makanan di Toko (Rp)',
                                              'Rating Toko', 'Similarity']])

except FileNotFoundError:
    st.error("File 'ds.xlsx' tidak ditemukan. Pastikan file ada di direktori yang sama dengan aplikasi.")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
