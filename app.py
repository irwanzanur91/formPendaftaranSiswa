import io
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# --- KONFIGURASI ---
FOLDER_ID = "1O6t17zbKHETumlBsNE9jW5n958P23Ntd"


def upload_ke_google_drive(file_buffer, nama_file, mime_type):
    credentials_info = dict(st.secrets["gcp_service_account"])

    # Menggunakan scope penuh agar bisa mengakses folder yang dibagikan
    creds = service_account.Credentials.from_service_account_info(
        credentials_info, scopes=["https://www.googleapis.com/auth/drive"]
    )
    service = build("drive", "v3", credentials=creds)

    file_metadata = {"name": nama_file, "parents": [FOLDER_ID]}

    media = MediaIoBaseUpload(
        io.BytesIO(file_buffer.read()), mimetype=mime_type, resumable=True
    )

    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )

    return file.get("id")


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
