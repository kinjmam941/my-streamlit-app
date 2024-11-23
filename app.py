import streamlit as st
import yt_dlp
import os
from io import BytesIO

# Function to get the next available file name (vid1.mp4, vid2.mp4, etc.)
def get_next_filename():
    i = 1
    while True:
        filename = f"vid{i}.mp4"
        if not os.path.exists(filename):
            return filename
        i += 1

# Streamlit UI setup
st.title("YouTube Video Downloader")

# Prompt user for the YouTube video URL
video_url = st.text_input("Enter YouTube Video URL:")

# Create a button to trigger download
if st.button("Download Video") and video_url:
    try:
        # yt-dlp options with concurrent fragments set to 25
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'merge_output_format': 'mp4',
            'outtmpl': '%(title)s.%(ext)s',
            'concurrent_fragments': 25,
        }

        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)

        # Generate a unique filename (e.g., vid1.mp4, vid2.mp4, etc.)
        file_name = get_next_filename()

        # Get the name of the downloaded file from yt-dlp
        downloaded_file = f"{info_dict['title']}.mp4"

        # Rename the downloaded file to the unique filename
        os.rename(downloaded_file, file_name)

        # Provide download link to the user
        st.success("Download complete!")
        st.download_button(
            label="Download Video",
            data=open(file_name, "rb").read(),
            file_name=file_name,
            mime="video/mp4"
        )

    except Exception as e:
        st.error(f"Error: {str(e)}")
