import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Kalkulator Dagang Multi-Produk", layout="wide")

st.title("📊 Mode Excel: Multi-Produk & Biaya Rinci")
st.markdown("Isi kedua tabel di bawah ini. Semua hitungan akan otomatis terupdate!")

# --- 1. TABEL DAFTAR PRODUK ---
st.subheader("📦 1. Daftar Produk")
st.caption("Masukkan semua barang daganganmu di sini. Klik (+) untuk tambah barang baru.")

# Inisialisasi template tabel produk
if 'df_produk' not in st.session_state:
    st.session_state.df_produk = pd.DataFrame([
        {"Nama Barang": "Produk A", "Stok": 10, "Harga Beli Total": 100000},
        {"Nama Barang": "Produk B", "Stok": 5, "Harga Beli Total": 50000}
    ])

edited_produk = st.data_editor(
    st.session_state.df_produk,
    num_rows="dynamic",
    use_container_width=True,
    key="produk_editor"
)

st.markdown("---")

# --- 2. TABEL BIAYA OPERASIONAL ---
st.subheader("🛠️ 2. Rincian Biaya Operasional Umum")
st.caption("Biaya ini adalah total biaya operasional (misal: ongkir total, total plastik) yang akan dibagi rata ke semua stok barang di atas.")

if 'df_ops' not in st.session_state:
    st.session_state.df_ops = pd.DataFrame([
        {"Komponen Biaya": "Ongkir Masuk", "Nominal (Rp)": 15000},
        {"Komponen Biaya": "Packing & Lakban", "Nominal (Rp)": 5000}
    ])

edited_ops = st.data_editor(
    st.session_state.df_ops,
    num_rows="dynamic",
    use_container_width=True,
    key="ops_editor"
)

# --- 3. KALKULASI OTOMATIS ---
total_stok_semua = edited_produk["Stok"].sum()
total_biaya_ops = edited_ops["Nominal (Rp)"].sum()

# Hitung biaya ops per 1 unit barang (dibagi rata ke semua stok)
ops_per_unit = total_biaya_ops / total_stok_semua if total_stok_semua > 0 else 0

# Tambahkan kolom perhitungan ke tabel produk
df_hasil = edited_produk.copy()
df_hasil["HPP Satuan"] = (df_hasil["Harga Beli Total"] / df_hasil["Stok"]) + ops_per_unit

st.markdown("---")

# --- 4. TARGET UNTUNG & HASIL AKHIR ---
st.subheader("💰 3. Analisis Harga Jual & Cuan")
margin = st.slider("Target Margin Untung (%)", 0, 100, 30)

df_hasil["Harga Jual"] = df_hasil["HPP Satuan"] * (1 + margin/100)
df_hasil["Total Laba"] = (df_hasil["Harga Jual"] - df_hasil["HPP Satuan"]) * df_hasil["Stok"]

# Tampilkan Tabel Hasil Akhir
st.dataframe(
    df_hasil.style.format({
        "Harga Beli Total": "Rp {:,.0f}",
        "HPP Satuan": "Rp {:,.0f}",
        "Harga Jual": "Rp {:,.0f}",
        "Total Laba": "Rp {:,.0f}"
    }),
    use_container_width=True
)

# Ringkasan Total
col1, col2 = st.columns(2)
col1.metric("Total Modal Keseluruhan", f"Rp {df_hasil['Harga Beli Total'].sum() + total_biaya_ops:,.0f}")
col2.metric("Total Potensi Laba Bersih", f"Rp {df_hasil['Total Laba'].sum():,.0f}", delta="Cuan!")

# --- 5. DOWNLOAD EXCEL ---
st.markdown("---")
output = BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df_hasil.to_excel(writer, index=False, sheet_name='Data_Produk_Cuan')
    edited_ops.to_excel(writer, index=False, sheet_name='Rincian_Operasional')
    writer.close()

st.download_button(
    label="🟢 Download Laporan Produk ke Excel (.xlsx)",
    data=output.getvalue(),
    file_name="Laporan_Dagang_Lengkap.xlsx",
    mime="application/vnd.ms-excel"
)
