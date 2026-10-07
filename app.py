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
        audio_file = "models/generated_music.wav"

        # FluidSynth path
        fluidsynth_path = r"C:\Users\aksha\Downloads\fluidsynth-v2.6.1-win10-x64-cpp11\fluidsynth-v2.6.1-win10-x64-cpp11\bin\fluidsynth.exe"

        # SoundFont path
        soundfont_path = r"venv\Lib\site-packages\pretty_midi\TimGM6mb.sf2"

        if os.path.exists(output_file):

            # Convert MIDI to WAV using FluidSynth
            with st.spinner("Preparing audio..."):

                audio_result = subprocess.run(
                    [
                        fluidsynth_path,
                        "-ni",
                        "-g",
                        "2.0",
                        "-F",
                        audio_file,
                        "-T",
                        "wav",
                        "-r",
                        "44100",
                        soundfont_path,
                        output_file
                    ],
                    capture_output=True,
                    text=True
                )

            if audio_result.returncode == 0 and os.path.exists(audio_file):

                st.subheader("🎧 Listen to Your Music")

                # Normalize audio volume
                try:
                    from pydub import AudioSegment
                    from pydub.effects import normalize

                    audio = AudioSegment.from_wav(audio_file)

                    normalized_audio = normalize(audio)

                    normalized_audio.export(
                        audio_file,
                        format="wav"
                    )

                    st.success("Audio volume optimized! 🔊")

                except Exception as e:

                    st.warning("Audio normalization could not be completed.")
                    st.code(str(e))

                # Play audio
                with open(audio_file, "rb") as audio:

                    st.audio(
                        audio.read(),
                        format="audio/wav"
                    )

                st.success("Audio is ready! 🎵")

            else:

                st.error("Audio conversion failed.")

                if audio_result.stderr:
                    st.code(audio_result.stderr)

            # Download MIDI
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

