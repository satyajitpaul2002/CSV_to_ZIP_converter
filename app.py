import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import io
import zipfile

# Title
st.title("📊 CSV to Chunked JPG Converter")
st.write("Upload a dataset and get chunks of 5 rows as JPG images.")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Load file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Select only required columns (if they exist)
    required_cols = [
        "First Name", "Last Name", "Email", "Mobile No",
        "Highest qualification", "Work Experience",
        "Location", "Sub-Location", "State"
    ]
    df = df[[col for col in required_cols if col in df.columns]]

    # Create ZIP buffer to store images
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        # Process in chunks of 5
        for i in range(0, len(df), 5):
            chunk = df.iloc[i:i+5]

            fig, ax = plt.subplots(figsize=(20, 2 + 0.6*len(chunk)))
            ax.axis('off')

            table = ax.table(cellText=chunk.values,
                             colLabels=chunk.columns,
                             cellLoc='center',
                             loc='center')

            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1.2, 1.5)

            # Save image to buffer
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format="jpg", bbox_inches="tight", dpi=200)
            plt.close()
            img_buffer.seek(0)

            # Add to zip
            zf.writestr(f"chunk_{i//5 + 1}.jpg", img_buffer.read())

    # Download button for ZIP
    st.download_button(
        label="📥 Download All Chunks as ZIP",
        data=zip_buffer.getvalue(),
        file_name="chunks_images.zip",
        mime="application/zip"
    )
