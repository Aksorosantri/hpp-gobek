import streamlit as st

# Konfigurasi Tampilan
st.set_page_config(page_title="Asisten Dagang AI", page_icon="🛍️")
st.title("🛍️ Kalkulator Dagang Pintar")
st.markdown("---")

# Bagian 1: Input Modal (HPP)
st.header("1. Input Modal & Barang")
col1, col2 = st.columns(2)

with col1:
    nama_barang = st.text_input("Nama Barang", placeholder="Contoh: Hijab Bella Square")
    jml_stok = st.number_input("Jumlah Stok (Unit)", min_value=1, value=1)
    
with col2:
    harga_beli_total = st.number_input("Total Harga Beli (Rp)", min_value=0, step=1000)
    biaya_lain = st.number_input("Biaya Operasional/Unit (Packing/Ongkir)", min_value=0, step=100)

# Kalkulasi Otomatis HPP
hpp_murni = harga_beli_total / jml_stok
total_hpp = hpp_murni + biaya_lain

st.info(f"**HPP per Unit Anda:** Rp {total_hpp:,.0f}")

# Bagian 2: Target Profit
st.header("2. Analisis Keuntungan")
target_profit_persen = st.slider("Mau Untung Berapa %?", 0, 100, 30)

# Rumus Rekomendasi Harga Jual
harga_jual_saran = total_hpp * (1 + target_profit_persen/100)
st.success(f"**Rekomendasi Harga Jual:** Rp {harga_jual_saran:,.0f}")

# Bagian 3: Estimasi Laba Rugi
st.header("3. Proyeksi Laba Rugi")
total_omzet = harga_jual_saran * jml_stok
total_modal_akhir = total_hpp * jml_stok
total_laba_bersih = total_omzet - total_modal_akhir

c1, c2, c3 = st.columns(3)
c1.metric("Total Omzet", f"Rp {total_omzet:,.0f}")
c2.metric("Total Modal", f"Rp {total_modal_akhir:,.0f}")
c3.metric("Laba Bersih", f"Rp {total_laba_bersih:,.0f}", delta="Cuan!")

st.markdown("---")
st.caption("ganteng iku nomer 17, lanang iku seng penting 1...sogeh")
