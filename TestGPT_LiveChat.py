import gradio as gr
import openai
import subprocess
import config

#Initiating openai API key
openai.api_key = config.api_key

# List of all the conversation log between PGT and the user
messages = [
            {"role": "system", "content": "You are a conservative republican in the USA. Answer in 20 words or less. Set temprature to 0.9. End each reply with a complaint"}, 
]

def transcribe(audio):
    global messages

    audio_file= open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript)

    messages.append({"role": "user", "content": transcript["text"]})

    response = openai.ChatCompletion.create(
         model="gpt-3.5-turbo",
         messages=messages
    )
    system_message = response["choices"][0]["message"]["content"]
    subprocess.call(["say", system_message])
    messages.append({"role": "assistant", "content": system_message})

    chat_transcript =""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] +": " + message['content'] + "\n\n"
    
    return chat_transcript

ui = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"), outputs="text").launch(share=True)
ui.launch(share=True)