import sklearn
import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity

# Daftar harga yang diset
harga_list = [10000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 
              21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 
              31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000, 
              41000, 42000, 43000, 44000, 45000, 47000, 48000, 49000, 50000, 51000, 
              52000, 55000, 56000, 57000, 58000, 59000, 60000, 62000, 64000, 66000, 
              67000, 68000, 69000, 70000, 73000, 75000, 76000, 77000, 80000, 82000, 
              85000, 87000, 88000, 92000, 100000, 103000, 107000, 108000, 111000, 
              119000, 120000, 132000, 330000]

# Load dataset
data = pd.read_excel('ds.xlsx')  # Ganti dengan path file dataset

# 1. Label Encoding untuk Preferensi Makanan dan Jenis Suasana
label_encoder = LabelEncoder()
data['Preferensi Makanan'] = label_encoder.fit_transform(data['Preferensi Makanan'])
data['Jenis Suasana'] = label_encoder.fit_transform(data['Jenis Suasana'])

# 2. Menghapus satuan 'km' pada Lokasi Restoran
data['Lokasi Restoran'] = data['Lokasi Restoran'].str.replace(' km', '').astype(float)

# 3. Kolom Harga Rata-Rata Makanan dan Rating Toko sudah numerik, jadi tidak perlu diubah
data = data[['Nama Restoran', 'Preferensi Makanan', 'Lokasi Restoran', 'Harga Rata-Rata Makanan di Toko (Rp)', 'Rating Toko', 'Jenis Suasana']]

# Menghitung cosine similarity berdasarkan fitur-fitur
features = data[['Preferensi Makanan', 'Lokasi Restoran', 'Harga Rata-Rata Makanan di Toko (Rp)', 'Rating Toko', 'Jenis Suasana']]
similarity_matrix = cosine_similarity(features)

# Streamlit UI
st.title("Rekomendasi Restoran")

# Tampilkan dataset dengan encoding
st.subheader("Dataset dengan Encoding")
st.write(data)

# Pilih rating dan harga dari daftar harga yang sudah ditentukan
rating_filter = st.slider('Pilih Rating Restoran', min_value=3.4, max_value=4.9, value=4.9, step=0.1)
price_filter = st.selectbox('Pilih Harga Maksimal (Rp)', harga_list)

# Menampilkan restoran yang sesuai dengan rating dan harga
filtered_data = data[(data['Rating Toko'] == rating_filter) & (data['Harga Rata-Rata Makanan di Toko (Rp)'] <= price_filter)]

# Menampilkan hasil rekomendasi
st.subheader("Restoran yang Disarankan:")
st.write(filtered_data[['Nama Restoran', 'Harga Rata-Rata Makanan di Toko (Rp)', 'Rating Toko']])

# Pilih restoran untuk melihat restoran terdekat (jika ada data yang lolos filter)
if not filtered_data.empty:
    restoran_terpilih = st.selectbox("Pilih Restoran untuk Melihat Rekomendasi Terdekat", filtered_data['Nama Restoran'])

    # Mendapatkan indeks restoran yang dipilih
    index_restoran = filtered_data[filtered_data['Nama Restoran'] == restoran_terpilih].index[0]

    # Menghitung cosine similarity untuk restoran terpilih
    similar_restaurants = list(enumerate(similarity_matrix[index_restoran]))

    # Mengurutkan berdasarkan similarity dan memilih 5 teratas
    similar_restaurants = sorted(similar_restaurants, key=lambda x: x[1], reverse=True)[1:6]

    # Filter hasil rekomendasi berdasarkan rating yang dipilih
    similar_filtered_data = [
        data.iloc[i[0]]
        for i in similar_restaurants
        if data.iloc[i[0]]['Rating Toko'] == rating_filter
    ]

    # Menampilkan restoran yang mirip
    st.subheader("Restoran Mirip dengan yang Anda Pilih:")
    if similar_filtered_data:
        for row in similar_filtered_data:
            st.write(f"- {row['Nama Restoran']} (Rating: {row['Rating Toko']}, Harga: Rp{row['Harga Rata-Rata Makanan di Toko (Rp)']})")
    else:
        st.write("Tidak ada restoran lain yang memenuhi kriteria berdasarkan rating yang dipilih.")
else:
    st.write("Tidak ada restoran yang memenuhi kriteria filter Anda.")
