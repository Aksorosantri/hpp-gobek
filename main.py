import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Excel Kalkulator Dagang", layout="wide")

st.title("📊 Mode Excel: Kalkulator HPP & Biaya Rinci")
st.markdown("Isi tabel di bawah ini untuk menghitung modal dan keuntungan secara mendalam.")

# --- BAGIAN 1: DATA UTAMA ---
st.subheader("📦 1. Data Barang")
col1, col2, col3 = st.columns(3)
with col1:
    nama_produk = st.text_input("Nama Produk", "Produk Baru")
with col2:
    stok = st.number_input("Jumlah Stok (Unit)", min_value=1, value=1)
with col3:
    harga_barang = st.number_input("Harga Beli Total Barang (Rp)", min_value=0, step=1000)

st.markdown("---")

# --- BAGIAN 2: TABEL EXCEL BIAYA OPERASIONAL ---
st.subheader("📝 2. Rincian Biaya Operasional (Tabel Excel)")
st.caption("Klik sel untuk mengubah nama biaya atau angkanya. Klik (+) di bawah tabel untuk tambah baris baru.")

# Inisialisasi template tabel biaya
if 'df_excel' not in st.session_state:
    st.session_state.df_excel = pd.DataFrame([
        {"Komponen Biaya": "Packing (Plastik/Bubble)", "Nominal (Rp)": 0},
        {"Komponen Biaya": "Ongkir Masuk", "Nominal (Rp)": 0},
        {"Komponen Biaya": "Lakban/Label", "Nominal (Rp)": 0},
        {"Komponen Biaya": "Admin Marketplace", "Nominal (Rp)": 0}
    ])

# Tampilan Editor Tabel ala Excel
edited_df = st.data_editor(
    st.session_state.df_excel,
    num_rows="dynamic",
    use_container_width=True,
    key="excel_editor"
)

# --- BAGIAN 3: KALKULASI AUTOMATIS ---
total_operasional = edited_df["Nominal (Rp)"].sum()
hpp_per_unit = (harga_barang + total_operasional) / stok

st.markdown("---")

# --- BAGIAN 4: TARGET & HASIL ---
st.subheader("💰 3. Target Untung & Harga Jual")
margin = st.slider("Mau ambil margin berapa %?", 0, 100, 20)

harga_jual = hpp_per_unit * (1 + margin/100)
laba_bersih = (harga_jual - hpp_per_unit) * stok

# Ringkasan Cantik
c1, c2, c3 = st.columns(3)
c1.metric("Total Modal (HPP)", f"Rp {harga_barang + total_operasional:,.0f}")
c2.metric("Harga Jual / Unit", f"Rp {harga_jual:,.0f}")
c3.metric("Total Laba Bersih", f"Rp {laba_bersih:,.0f}")

# --- BAGIAN 5: DOWNLOAD EXCEL ---
st.markdown("---")
# Membuat file Excel sungguhan di memori
output = BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    # Gabungkan data untuk laporan
    df_laporan = pd.concat([
        pd.DataFrame([{"Keterangan": "Nama Produk", "Nilai": nama_produk}, {"Keterangan": "Stok", "Nilai": stok}]),
        edited_df.rename(columns={"Komponen Biaya": "Keterangan", "Nominal (Rp)": "Nilai"}),
        pd.DataFrame([
            {"Keterangan": "HPP per Unit", "Nilai": hpp_per_unit},
            {"Keterangan": "Harga Jual", "Nilai": harga_jual},
            {"Keterangan": "Total Laba", "Nilai": laba_bersih}
        ])
    ])
    df_laporan.to_excel(writer, index=False, sheet_name='Laporan_Cuan')
    writer.close()

st.download_button(
    label="🟢 Download Hasil ke File Excel (.xlsx)",
    data=output.getvalue(),
    file_name=f"Laporan_{nama_produk}.xlsx",
    mime="application/vnd.ms-excel"
)
