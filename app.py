import base64
import requests
import streamlit as st

# --- URL WEB APP GOOGLE APPS SCRIPT ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw9IfH7nD--uVDV13MT2hYboS2jZX89HreIJf1hozpFWvKptY57y95JlHPS4__Xo7C8Sw/exec"


def upload_ke_google_drive(file_buffer, nama_file, mime_type):
    # Mengubah file gambar menjadi format Base64
    file_bytes = file_buffer.read()
    encoded_file = base64.b64encode(file_bytes).decode("utf-8")

    # Data yang dikirim ke Google Apps Script
    payload = {
        "fileName": nama_file,
        "mimeType": mime_type,
        "fileData": encoded_file,
    }

    # Mengirim file melalui HTTP POST
    response = requests.post(WEB_APP_URL, json=payload)

    if response.status_code == 200:
        result = response.json()
        if result.get("status") == "success":
            return result.get("fileId")
        else:
            raise Exception(
                result.get("message", "Terjadi kesalahan pada Google Apps Script.")
            )
    else:
        raise Exception(
            f"Gagal terhubung ke Google Apps Script (HTTP {response.status_code})"
        )


# --- TAMPILAN FORM SISWA ---
st.set_page_config(page_title="Form Pendaftaran Siswa", page_icon="📝")

st.title("📝 Form Pendaftaran Siswa Baru")
st.write("Silakan isi data diri dan unggah pasfoto Anda di bawah ini.")

with st.form("form_pendaftaran", clear_on_submit=True):
    nama_lengkap = st.text_input("Nama Lengkap Siswa")
    nisn = st.text_input("NISN / Nomor Induk")
    foto = st.file_uploader(
        "Unggah Pasfoto (Format: JPG/PNG)", type=["jpg", "jpeg", "png"]
    )

    tombol_submit = st.form_submit_button("Kirim Pendaftaran")

if tombol_submit:
    if not nama_lengkap or not foto:
        st.warning("⚠️ Harap lengkapi Nama dan unggah Foto terlebih dahulu!")
    else:
        try:
            with st.spinner("Mengunggah foto ke Google Drive..."):
                ekstensi = foto.name.split(".")[-1]
                nama_file_baru = (
                    f"Foto_{nama_lengkap.replace(' ', '_')}_{nisn}.{ekstensi}"
                )

                file_id = upload_ke_google_drive(
                    foto, nama_file_baru, foto.type
                )

            st.success(
                f"✅ Pendaftaran berhasil! Foto **{nama_file_baru}** telah tersimpan di Google Drive."
            )
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan saat mengunggah: {e}")
