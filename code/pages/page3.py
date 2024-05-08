import streamlit as st
from read_palm import main
import bedrock
from PIL import Image
import boto3
import polly

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

# st. set_page_config(layout="wide")
with st.container():
	

        # //call bedrock
        # get predictions
        # generate audio
        # generate Video
        # redirect to next page
        # st.page_link("pages/page2.py", See Pre)

	col1, col2 = st.columns([2, 3])

	image = Image.open('results/result.jpg')
	col1.image(image, caption='', use_column_width=None)

	video_file = open('video.mp4', 'rb')
	video_bytes = video_file.read()
	col2.video(video_bytes)
	
	# st.audio(audio, format="audio/mp3", loop=False)
	
	
	st.write(prediction)
      
	# if st.button("Restart", type="primary"):
	st.page_link("app.py")

	st.write("* Note: This program is just for fun! Please take the result with a light heart.")

