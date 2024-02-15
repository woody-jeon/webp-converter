import os
from PIL import Image
import streamlit as st
from io import BytesIO
import zipfile

def convert_to_webp(filename, quality, path="images/"):
    fname, extension = os.path.splitext(filename)
    extension = extension.replace(".", "")
    img = Image.open(path + filename)
    
    if extension == "png":
        img.save((path+fname+".webp"), "webp", lossless=True, quality=quality)
    elif extension == "jpg" or extension == "jpeg":
        img.save((path+fname+".webp"), "webp", quality=quality)
        
    return path+fname+".webp"

def compress_and_download(file_paths):
    zip_buffer = BytesIO()
    zip_len = 0
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_path in file_paths:
            _, extension = os.path.splitext(file_path)
            if extension == ".webp":
                with open(file_path, "rb") as f:
                    image_bytes = f.read()
            
                zip_file.writestr(os.path.basename(file_path), image_bytes)
                zip_len += 1
    st.success("변환이 완료되었습니다.")
    # Download the zip file
    zip_buffer.seek(0)
    if st.download_button(
        label="압축파일 다운로드",
        data=zip_buffer.getvalue(),
        file_name=file_paths[0] + "외_" + str(zip_len-1) + "건.zip",
        mime="application/zip",
        on_click=_delete_files(file_paths)
    ):
        st.write("'<script>location.reload(true);</script>'", unsafe_allow_html=True)

def _delete_files(file_paths):
    """Delete files after downloading"""
    for file_path in file_paths:
        os.remove(file_path)


def main() :
    st.title('Webp Converter')
    upload_files = st.file_uploader('이미지 파일 선택', type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)
    quality = st.slider("Pick a img Quality", 0, 100)
    save_folder = "images/"
    file_paths = []
    if upload_files and quality:
        if st.button("파일 변환하기"):
            st.success("변환을 시작합니다.")
            for upload_file in upload_files:
                file_path = os.path.join(save_folder, upload_file.name)
                with open(file_path, 'wb') as f :
                    f.write(upload_file.getbuffer())
                    convert_file_path = convert_to_webp(upload_file.name, quality, save_folder)
                    file_paths.append(convert_file_path)
                    file_paths.append(file_path)
            
            if file_paths:
                compress_and_download(file_paths)

if __name__ == "__main__":
    main()
