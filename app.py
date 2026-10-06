import streamlit as st
import subprocess
import os
import sys

st.set_page_config(
    page_title="AI Music Generator",
    page_icon="🎵",
    layout="centered"
)

st.title("🎵 AI Music Generation")
st.write("Generate music using a trained LSTM model.")

st.subheader("Generate Music")

if st.button("🎶 Generate Music"):

    with st.spinner("Generating music..."):
        result = subprocess.run(
        [sys.executable, "generate_music.py"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:

        st.success("Music generated successfully! 🎉")

        output_file = "models/generated_music.mid"

        if os.path.exists(output_file):

            with open(output_file, "rb") as file:

                st.download_button(
                    label="⬇️ Download Generated MIDI",
                    data=file,
                    file_name="generated_music.mid",
                    mime="audio/midi"
                )

    else:

        st.error("Music generation failed.")

        st.code(result.stderr)