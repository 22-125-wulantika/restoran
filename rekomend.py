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

# Pilih rating dan harga
rating_filter = st.slider('Pilih Rating Restoran', min_value=3.4, max_value=4.9, value=4.9, step=0.1)
price_filter = st.slider('Pilih Harga Maksimal (Rp)', min_value=0, max_value=330000, value=50000, step=1000)

# Menampilkan restoran yang sesuai dengan rating dan harga
filtered_data = data[(data['Rating Toko'] <= price_filter) & (data['Harga Rata-Rata Makanan di Toko (Rp)'] <= price_filter)]

# Menampilkan hasil rekomendasi
st.subheader("Restoran yang Disarankan:")
st.write(filtered_data[['Nama Restoran', 'Harga Rata-Rata Makanan di Toko (Rp)', 'Rating Toko']])

# Pilih restoran untuk melihat restoran terdekat
restoran_terpilih = st.selectbox("Pilih Restoran untuk Melihat Rekomendasi Terdekat", filtered_data['Nama Restoran'])

# Mendapatkan indeks restoran yang dipilih
index_restoran = filtered_data[filtered_data['Nama Restoran'] == restoran_terpilih].index[0]

# Menghitung cosine similarity untuk restoran terpilih
similar_restaurants = list(enumerate(similarity_matrix[index_restoran]))

# Mengurutkan berdasarkan similarity dan memilih 5 teratas
similar_restaurants = sorted(similar_restaurants, key=lambda x: x[1], reverse=True)[1:6]

# Menampilkan restoran yang mirip
st.subheader("Restoran Mirip dengan yang Anda Pilih:")
for i in similar_restaurants:
    restaurant_index = i[0]
    restaurant_name = data.iloc[restaurant_index]['Nama Restoran']
    st.write(f"- {restaurant_name}")
