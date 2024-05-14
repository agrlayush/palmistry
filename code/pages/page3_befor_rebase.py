import streamlit as st
from read_palm import main
import bedrock
from PIL import Image
import boto3
import subprocess
import os
from datetime import datetime



st.set_page_config(initial_sidebar_state="collapsed")
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

filename = "hand.jpg"
length = main(filename, "streamlit")
heart_line = length[0]/10
head_line = length[1]/10
life_line = length[2]/10

# Each prediction can have a prediction on a positive life event and a warning on a separate life event, giving a balanced answer for each prediction.
# Example of Positive Life events: Buying a vehicle, Addition of a new member to the family, Major growth in career, Upcoming Opportunity for international travel.
# Example of Warning message: Be carefull when making major financial decisions, avoid travel etc.
# Make the prediction sound definitive with a duration in Years, for example: Major career growth in X years.

prompt = '''
You are a Palmist fortune teller and after looking at the human hand you have found the length of heart line as {heart_line} cm, length of head line as {head_line} cm and length of life line as {life_line} cm. You will generate prediction for the human hand similar to sample predictions.
Sample Predictions:
1. A significant milestone in your career is on the horizon. Within the next three years, you will achieve professional recognition and success beyond your wildest dreams. Your hard work and dedication will pave the way for advancement and prosperity. However, remain cautious in your personal relationships, ensuring open communication and understanding to navigate potential conflicts.
2. Your palm suggests the possibility of embarking on a new adventure in the realm of education or personal development. Embrace this opportunity for growth with enthusiasm and determination, as it will expand your horizons and unlock new potentials within you. However, exercise caution when it comes to financial matters, ensuring responsible budgeting and planning to support your aspirations.
3. I sense a warning regarding excessive travel in the near future. While exploration is enriching, be mindful of overextending yourself and neglecting responsibilities at home. Balance is key to maintaining harmony in all areas of your life. Meanwhile, remain open to unexpected opportunities for career advancement that may arise from networking and expanding your horizons.
4. Your palm reveals the potential for a period of emotional healing and renewal. Embrace this opportunity to release past traumas and embrace a brighter future with optimism and grace. However, exercise caution in your financial decisions, ensuring prudent budgeting and saving to support your long-term goals and aspirations.
5. A message of caution regarding health and well-being emerges from your palm. Pay attention to any signs or symptoms that may indicate imbalance or illness, and prioritize self-care practices to maintain vitality and resilience. Prevention is the key to long-term wellness. Meanwhile, remain open to unexpected opportunities for personal growth and transformation that may arise from introspection and self-discovery.

Generate the Prediction in 75 words. Skip the preamble. Do not provide the length in the response. Do not add xml templates \n\nAssistant:
'''.format(heart_line=heart_line, head_line=head_line, life_line=life_line)
# f"You are a Palmist fortune teller and after looking at the human hand you have found the length of heart line as {heart_line} cm, length of head line as {head_line} cm and length of life line as {life_line} cm. You will generate prediction for the human hand.
print("prompt", prompt)
response = bedrock.invoke_claude_3_with_text(prompt)
prediction = response["content"][0]["text"]

# audio = polly.get_audio(prediction)
st.markdown("<h2 style='text-align: center'>Your Fortune</h2>", unsafe_allow_html=True)
st.header('', divider='rainbow')

if 'pandit' not in st.session_state:
	st.session_state.pandit = 'false'
	st.session_state.audio_video = 'false'
	st.session_state.video_bytes = None

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
		os.system('cd ../../Wav2Lip && python inference.py --checkpoint_path checkpoints/wav2lip_gan.pth --face "../palmistry/code/output_video.mp4" --audio "../palmistry/code/eng.mp3"')
		video_file = open('../../Wav2Lip/results/result_voice.mp4', 'rb')
		video_bytes = video_file.read()
		#if 'is_video_placeholder' in st.session_state:
		st.session_state.video_bytes = video_bytes
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
	#st.session_state.audio_field.audio(eng_bytes, format='audio/mp3')
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

# st. set_page_config(layout="wide")
with st.container():

	st.session_state.fortune_text = prediction
	if st.session_state.audio_video == 'false':
		video_file = open('../../astro-placeholder.mov', 'rb')
		video_bytes = video_file.read()
		#if 'is_video_placeholder' in st.session_state:
		placeholder = st.empty()
		st.session_state.placeholder_video = placeholder
		st.session_state.placeholder_video.video(video_bytes, loop=True, autoplay=True)
		generate_audio_video()
		st.session_state.placeholder_video.empty()
		col1, col2 = st.columns(2)
		with col1:
			image = Image.open('results/result.jpg')
			col1.image(image, caption='', use_column_width=None)
		with col2:
			st.video(st.session_state.video_bytes)
		st.subheader(prediction)


	# if st.button("Restart", type="primary"):
	#col1, col2, col3 = st.columns([3, 1, 2])
	#if col2.button("Restart", type="primary"):
    #        st.switch_page("app.py")
    # st.page_link("app.py")
st.write("* Note: This program is just for fun! Please take the result with a light heart.")


