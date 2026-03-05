import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Stok & Cuan", layout="wide")

st.title("📊 Tabel Inventaris & Analisis Laba")
st.markdown("Masukkan daftar produkmu di bawah ini untuk hitung otomatis.")

# Inisialisasi data kosong jika belum ada
if 'data_barang' not in st.session_state:
    st.session_state.data_barang = pd.DataFrame(
        columns=['Nama Barang', 'Stok', 'Harga Beli Total', 'Biaya Operasional/Unit', 'Target Untung (%)']
    )

# Bagian Input Form
with st.expander("➕ Tambah Produk Baru", expanded=True):
    with st.form("form_input"):
        col1, col2, col3 = st.columns(3)
        nama = col1.text_input("Nama Produk")
        stok = col2.number_input("Jumlah Stok", min_value=1, value=1)
        beli = col3.number_input("Total Harga Beli (Rp)", min_value=0)
        
        col4, col5 = st.columns(2)
        ops = col4.number_input("Biaya Ops/Unit (Packing dll)", min_value=0)
        untung = col5.slider("Target Untung (%)", 0, 100, 20)
        
        submit = st.form_submit_button("Masukkan ke Tabel")
        
        if submit and nama:
            new_data = pd.DataFrame([{
                'Nama Barang': nama, 
                'Stok': stok, 
                'Harga Beli Total': beli, 
                'Biaya Operasional/Unit': ops,
                'Target Untung (%)': untung
            }])
            st.session_state.data_barang = pd.concat([st.session_state.data_barang, new_data], ignore_index=True)
            st.success(f"{nama} berhasil ditambah!")

# Bagian Tabel Perhitungan
if not st.session_state.data_barang.empty:
    df = st.session_state.data_barang.copy()
    
    # Rumus Otomatis
    df['HPP/Unit'] = (df['Harga Beli Total'] / df['Stok']) + df['Biaya Operasional/Unit']
    df['Harga Jual Saran'] = df['HPP/Unit'] * (1 + df['Target Untung (%)']/100)
    df['Total Modal'] = df['HPP/Unit'] * df['Stok']
    df['Estimasi Laba'] = (df['Harga Jual Saran'] - df['HPP/Unit']) * df['Stok']

    st.subheader("📋 Daftar Daganganmu")
    # Menampilkan tabel yang rapi
    st.dataframe(df.style.format({
        'Harga Beli Total': 'Rp {:,.0f}',
        'HPP/Unit': 'Rp {:,.0f}',
        'Harga Jual Saran': 'Rp {:,.0f}',
        'Total Modal': 'Rp {:,.0f}',
        'Estimasi Laba': 'Rp {:,.0f}'
    }), use_container_width=True)

    # Ringkasan Total
    st.markdown("---")
    c1, c2 = st.columns(2)
    c1.metric("Total Modal Semua Barang", f"Rp {df['Total Modal'].sum():,.0f}")
    c2.metric("Total Potensi Cuan Bersih", f"Rp {df['Estimasi Laba'].sum():,.0f}", delta="🔥")

    if st.button("🗑️ Hapus Semua Data"):
        st.session_state.data_barang = pd.DataFrame(columns=df.columns[:5])
        st.rerun()
else:
    st.info("Belum ada produk. Silakan tambah produk di atas ya!")
