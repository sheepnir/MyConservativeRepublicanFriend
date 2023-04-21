import gradio as gr
import openai

#Initiating openai API key
openai.api_key = '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'

# Function to transcribe audio and communicate with ChatGPT
def converse_with_chatgpt(audio, history):
    # Transcribe audio
    transcribed_text = openai.Speech.transcribe_file(audio.name)
    input_text = transcribed_text["data"]["text"]

    # Define a context for ChatGPT
    context = f"A medical doctor who answers all the questions in less than 20 words.\n{history}\nUser: {input_text}\nDoctor:"

    # Generate response using OpenAI Chat API
    response = openai.ChatCompletion.create(
        model="text-davinci-002",
        messages=[
            {"role": "system", "content": "You are a medical doctor who answers all the questions in less than 20 words."},
            {"role": "user", "content": input_text},
        ],
        max_tokens=20,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Extract the generated response
    reply = response.choices[0].message['content'].strip()
    updated_history = f"{history}\nUser: {input_text}\nDoctor: {reply}"

    return reply, updated_history

# Gradio interface
iface = gr.Interface(
    converse_with_chatgpt,
    inputs=[gr.inputs.Audio(source="microphone"), "text"],
    outputs=["text", "text"],
    examples=[],
)

iface.launch()

