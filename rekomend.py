import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Judul aplikasi
st.title("Rekomendasi Restoran Berdasarkan Harga dan Rating")

# Membaca file dataset
@st.cache_data
def load_data():
    return pd.read_excel('ds.xlsx')

try:
    data = load_data()

    # Validasi kolom
    required_columns = ['Nama Restoran', 'Harga Rata-Rata Makanan di Toko (Rp)', 'Rating Toko']
    if not all(col in data.columns for col in required_columns):
        st.error("Dataset harus memiliki kolom berikut: " + ", ".join(required_columns))
    else:
        # Pratinjau data
        st.subheader("Pratinjau Dataset:")
        st.write(data.head())

        # Preprocessing Data: memastikan kolom harga dan rating dalam format numerik
        data['Harga Rata-Rata Makanan di Toko (Rp)'] = pd.to_numeric(data['Harga Rata-Rata Makanan di Toko (Rp)'], errors='coerce')
        data['Rating Toko'] = pd.to_numeric(data['Rating Toko'], errors='coerce')

        # Input fitur harga dan rating
        st.subheader("Masukkan Kriteria Restoran (Harga dan Rating):")
        
        # Input harga dan rating oleh pengguna
        harga_input = st.number_input("Harga Rata-Rata Makanan (Rp):", min_value=int(data['Harga Rata-Rata Makanan di Toko (Rp)'].min()),
                                     max_value=int(data['Harga Rata-Rata Makanan di Toko (Rp)'].max()),
                                     value=int(data['Harga Rata-Rata Makanan di Toko (Rp)'].mean()), step=500)
        
        rating_input = st.slider("Rating Toko (0-5):", min_value=0, max_value=5, value=4, step=0.1)

        # Membuat input vektor
        input_vector = [[harga_input, rating_input]]

        # Menyaring data yang relevan berdasarkan harga dan rating
        filtered_data = data[(data['Harga Rata-Rata Makanan di Toko (Rp)'] >= harga_input - 500) & 
                             (data['Harga Rata-Rata Makanan di Toko (Rp)'] <= harga_input + 500) & 
                             (data['Rating Toko'] >= rating_input - 0.5) & 
                             (data['Rating Toko'] <= rating_input + 0.5)]

        # Menampilkan hasil rekomendasi berdasarkan harga dan rating
        st.subheader("Restoran yang Direkomendasikan:")
        if filtered_data.empty:
            st.write("Tidak ada restoran yang sesuai dengan kriteria Anda.")
        else:
            st.write(f"Menampilkan restoran dengan harga sekitar Rp {harga_input} dan rating sekitar {rating_input}.")
            st.write(filtered_data[['Nama Restoran', 'Harga Rata-Rata Makanan di Toko (Rp)', 'Rating Toko']])

except FileNotFoundError:
    st.error("File 'ds.xlsx' tidak ditemukan. Pastikan file ada di direktori yang sama dengan aplikasi.")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
