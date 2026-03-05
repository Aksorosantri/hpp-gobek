import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Kalkulator Dagang Pro", layout="wide")

st.title("NEW GOBEK😎")
st.markdown("Ganteng iku nomer 17, dadi wong lanang pokok siji...SOGEH")

# --- 1. TABEL DAFTAR PRODUK ---
st.subheader("📦 1. Daftar Produk")
st.caption("Klik (+) untuk tambah barang baru. Isi 'Stok' dan 'Harga Beli Total'.")

if 'df_produk' not in st.session_state:
    st.session_state.df_produk = pd.DataFrame([
        {"Nama Barang": "Produk A", "Stok": 10, "Harga Beli Total": 100000}
    ])

edited_produk = st.data_editor(
    st.session_state.df_produk,
    num_rows="dynamic",
    use_container_width=True,
    key="produk_editor"
)

# --- 2. TABEL BIAYA OPERASIONAL ---
st.subheader("🛠️ 2. Rincian Biaya Operasional Umum")
st.caption("Contoh: Ongkir total, Listrik, atau Packing.")

if 'df_ops' not in st.session_state:
    st.session_state.df_ops = pd.DataFrame([
        {"Komponen Biaya": "Biaya Lain-lain", "Nominal (Rp)": 0}
    ])

edited_ops = st.data_editor(
    st.session_state.df_ops,
    num_rows="dynamic",
    use_container_width=True,
    key="ops_editor"
)

# --- 3. KALKULASI AMAN ---
# Kita pastikan angka tidak kosong supaya tidak error
total_stok = edited_produk["Stok"].replace(0, 1).sum() 
total_biaya_ops = edited_ops["Nominal (Rp)"].sum()
ops_per_unit = total_biaya_ops / total_stok if total_stok > 0 else 0

# Gabungkan data
df_hasil = edited_produk.copy()
# Pastikan kolom angka adalah tipe numerik agar tidak TypeError
df_hasil["Stok"] = pd.to_numeric(df_hasil["Stok"], errors='coerce').fillna(0)
df_hasil["Harga Beli Total"] = pd.to_numeric(df_hasil["Harga Beli Total"], errors='coerce').fillna(0)

df_hasil["HPP Satuan"] = (df_hasil["Harga Beli Total"] / df_hasil["Stok"].replace(0, 1)) + ops_per_unit

st.markdown("---")

# --- 4. TARGET UNTUNG ---
st.subheader("💰 3. Analisis Harga Jual & Cuan")
margin = st.slider("Target Margin Untung (%)", 0, 100, 30)

df_hasil["Harga Jual"] = df_hasil["HPP Satuan"] * (1 + margin/100)
df_hasil["Total Laba"] = (df_hasil["Harga Jual"] - df_hasil["HPP Satuan"]) * df_hasil["Stok"]

# Tampilan Tabel Hasil (Tanpa Format Ribuan yang bikin Error)
st.write("### 📋 Hasil Perhitungan")
st.dataframe(df_hasil, use_container_width=True)

# Ringkasan Total
st.markdown("---")
c1, c2 = st.columns(2)
total_modal = df_hasil["Harga Beli Total"].sum() + total_biaya_ops
total_cuan = df_hasil["Total Laba"].sum()

c1.metric("Total Modal Keseluruhan", f"Rp {total_modal:,.0f}")
c2.metric("Total Potensi Laba Bersih", f"Rp {total_cuan:,.0f}")

# --- 5. DOWNLOAD EXCEL ---
output = BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df_hasil.to_excel(writer, index=False, sheet_name='Data_Cuan')
    edited_ops.to_excel(writer, index=False, sheet_name='Biaya_Ops')
    writer.close()

st.download_button(
    label="🟢 Download Laporan ke Excel",
    data=output.getvalue(),
    file_name="Laporan_Dagang.xlsx",
    mime="application/vnd.ms-excel"
)
