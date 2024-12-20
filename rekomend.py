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

        # Input fitur yang dipilih pengguna
        st.subheader("Pilih Fitur yang Digunakan untuk Rekomendasi:")
        fitur_terpilih = st.multiselect(
            "Pilih Fitur:",
            options=['Preferensi Makanan', 'Lokasi Restoran', 'Harga Rata-Rata Makanan di Toko (Rp)',
                     'Rating Toko', 'Jenis Suasana'],
            default=['Preferensi Makanan', 'Lokasi Restoran', 'Rating Toko']
        )

        # Memastikan hanya kolom yang dipilih digunakan
        if len(fitur_terpilih) == 0:
            st.error("Harap pilih minimal satu fitur untuk melakukan rekomendasi.")
        else:
            # Data subset berdasarkan fitur yang dipilih
            features = data[fitur_terpilih]

            # Menghitung cosine similarity berdasarkan fitur yang dipilih
            similarity_matrix = cosine_similarity(features)

            # Input dari pengguna untuk setiap fitur yang dipilih
            st.subheader("Masukkan Kriteria Restoran:")
            input_values = {}
            for fitur in fitur_terpilih:
                if fitur == 'Lokasi Restoran':
                    input_values[fitur] = st.number_input(f"Lokasi Restoran (km):", min_value=float(features[fitur].min()),
                                                         max_value=float(features[fitur].max()),
                                                         value=float(features[fitur].mean()), step=0.1)
                elif fitur == 'Harga Rata-Rata Makanan di Toko (Rp)':
                    input_values[fitur] = st.number_input(f"Harga Rata-Rata Makanan (Rp):", min_value=int(features[fitur].min()),
                                                         max_value=int(features[fitur].max()),
                                                         value=int(features[fitur].mean()), step=500)
                elif fitur == 'Rating Toko':
                    input_values[fitur] = st.number_input(f"Rating Minimum:", min_value=0.0, max_value=5.0,
                                                         value=4.5, step=0.1)
                else:
                    input_values[fitur] = st.number_input(f"{fitur} (numerik):", min_value=int(features[fitur].min()),
                                                         max_value=int(features[fitur].max()),
                                                         value=int(features[fitur].mean()))

            # Membuat input vektor
            input_vector = [[input_values[fitur] for fitur in fitur_terpilih]]

            # Menghitung similarity antara input pengguna dengan data
            similarity_scores = cosine_similarity(input_vector, features)[0]

            # Menambahkan skor similarity ke dalam dataset
            data['Similarity'] = similarity_scores

            # Filter dan urutkan berdasarkan similarity
            recommended_restaurants = data.sort_values(by='Similarity', ascending=False).head(5)

            # Menampilkan hasil rekomendasi berdasarkan fitur yang dipilih
            st.subheader("Restoran yang Direkomendasikan Berdasarkan Fitur yang Dipilih:")
            if recommended_restaurants.empty:
                st.write("Tidak ada restoran yang sesuai dengan kriteria Anda.")
            else:
                st.write(f"Menampilkan rekomendasi berdasarkan fitur: {', '.join(fitur_terpilih)}")
                
                # Menampilkan kolom yang relevan berdasarkan fitur yang dipilih
                columns_to_display = ['Nama Restoran', 'Similarity']  # Kolom dasar yang selalu tampil
                if 'Preferensi Makanan' in fitur_terpilih:
                    columns_to_display.append('Preferensi Makanan')
                if 'Rating Toko' in fitur_terpilih:
                    columns_to_display.append('Rating Toko')
                if 'Harga Rata-Rata Makanan di Toko (Rp)' in fitur_terpilih:
                    columns_to_display.append('Harga Rata-Rata Makanan di Toko (Rp)')
                if 'Jenis Suasana' in fitur_terpilih:
                    columns_to_display.append('Jenis Suasana')
                if 'Lokasi Restoran' in fitur_terpilih:
                    columns_to_display.append('Lokasi Restoran')

                # Menampilkan data rekomendasi dengan kolom yang relevan
                st.write(recommended_restaurants[columns_to_display])

except FileNotFoundError:
    st.error("File 'ds.xlsx' tidak ditemukan. Pastikan file ada di direktori yang sama dengan aplikasi.")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
