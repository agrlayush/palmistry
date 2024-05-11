import streamlit as st
import boto3
import subprocess
import os
from datetime import datetime

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: red;'>AI Astrologer</h1>", unsafe_allow_html=True)

sample_fortune_text = "A significant milestone in your career is on the horizon. Within the next three years, you will achieve professional recognition and success beyond your wildest dreams. Your hard work and dedication will pave the way for advancement and prosperity"
if 'audio_video' not in st.session_state:
    st.session_state.audio_video = 'false'

def save_uploadedfile(uploadedfile, filename):
    with open(filename, "wb") as f:
        f.write(uploadedfile.getbuffer())

def generate_fortunetext():
    st.session_state.fortune_text = sample_fortune_text

def get_audio_duration(audio_file):
    audio_duration = subprocess.check_output(["ffprobe", "-i", "eng.mp3", "-show_entries", "format=duration"]).decode().split("=")[1]
    st.session_state.audio_duration = audio_duration.replace('\n[/FORMAT]\n','')

def generate_video():
    ip_image = "avatar.jpeg"
    audio_duration = st.session_state.audio_duration
    h = 360
    w = 360
    # Define the FFmpeg command
    ffmpeg_command = [
        'ffmpeg',
        '-y',
        '-loop', '1',
        '-framerate', '25',
        '-i', ip_image,
        '-t', str(audio_duration),
        '-vf', f'scale={h}:{w}',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        'output_video.mp4'
    ]

    # Run the FFmpeg command
    try:
        subprocess.run(ffmpeg_command, check=True)
        print("FFmpeg command executed successfully")
        video_file = open('output_video.mp4', 'rb')
        os.system('cd ../../Wav2Lip && python inference.py --checkpoint_path checkpoints/wav2lip_gan.pth --face "../palmistry/code//output_video.mp4" --audio "../palmistry/code/eng.mp3"')
        video_file = open('../../Wav2Lip/results/result_voice.mp4', 'rb')
        video_bytes = video_file.read()
        #if 'is_video_placeholder' in st.session_state:
        st.session_state.video_field.video(video_bytes)
    except subprocess.CalledProcessError as e:
        print("Error executing FFmpeg command:", e)

def generate_audio():
    fortune_txt = st.session_state.fortune_text
    polly_client = boto3.Session().client('polly')
    voiceid = "Gregory"
    engine = "neural"
    response = polly_client.synthesize_speech(VoiceId=voiceid,
                                              LanguageCode='en-IN',
                                              OutputFormat='mp3',
                                              Text = fortune_txt,
                                              Engine = engine)
    print(response)
    eng_file = open('eng.mp3', 'wb')
    eng_bytes = response['AudioStream'].read()
    eng_file.write(eng_bytes)
    st.session_state.audio_field.audio(eng_bytes, format='audio/mp3')
    eng_file.close()

def generate_audio_video():
    generate_audio()
    get_audio_duration('eng.mp3')
    start_time = datetime.now()
    print("start time ", start_time)
    generate_video()
    end_time = datetime.now()
    print("end time " , end_time)
    print("Total time in seconds " , (end_time - start_time).total_seconds())
    #st.session_state.audio_field.text_input("Audio", "")
    #st.session_state.video_field.text_input("Video", "")
    st.session_state.audio_video = 'true'

def main():
    palm_panel , avatar_panel  = st.columns(2)
    palm_panel.subheader("Capture your Palm to know your fortune")
    avatar_panel.subheader("Fortune Teller Avatar")
    with avatar_panel:
        if 'fortune_text' not in st.session_state:
            st.session_state.fortune_text = "your fortune is here!!"
        fortune_field = st.text_area(" ", value=st.session_state.fortune_text, height=150)
        st.session_state.fortune_text = sample_fortune_text
        if fortune_field != "your fortune is here!!":
            st.button("Generate Audio and Video", on_click=generate_audio_video)

        if st.session_state.audio_video == 'false':
            audio = st.empty()
            video = st.empty()
            st.session_state.audio_field = audio
            st.session_state.video_field = video
    with palm_panel:
        input_image = st.camera_input(" ")

        if input_image:
            st.image(input_image)
            save_uploadedfile(input_image,"palm.jpeg")
            st.button("Generate fortune Text", on_click=generate_fortunetext)

if __name__ == "__main__":
    main()


