import boto3

def get_audio(text):
    client = boto3.client(service_name="polly", region_name="us-east-1")
    response = client.synthesize_speech(VoiceId='Joanna',
                    OutputFormat='mp3', 
                    Text = text,
                    Engine = 'neural')
    file = open('results/speech.mp3', 'wb')
    file.write(response['AudioStream'].read())
    file.close()
    return 'results/speech.mp3'