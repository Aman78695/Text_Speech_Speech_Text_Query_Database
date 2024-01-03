from openai import OpenAI
import os
#from dotenv import load_dotenv
import base64
import streamlit as st
import pandas as pd
#load_dotenv()
#api_key = os.getenv("openai_api_key")
api_key = "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"

client = OpenAI(api_key=api_key)

def get_answer(messages,file):
    pd.set_option('display.max_columns',None)
    pd.set_option('display.max_rows',None)
    df=pd.read_csv(file)
    #print(df)
    system_message = [{"role": "system", "content": f"""You are an AI assistant that answers questions by extracting insights from dataframes. 
                       When I provide a dataframe and ask you a question about the data, you will analyze the data, perform any required calculations on it, and directly return the factual answer from the dataset itself. 
                       You should never describe procedural steps or give theoretical responses - instead, your answers should be exact excerpts from the dataframe to answer my question. 
                       If you cannot definitively determine the answer, be honest and state you do not know. Do not guess or infer anything not explicitly supported by the data. Provide explanations only when necessary to justify your response as the correct data backed answer. Otherwise, 
                       directly state the cell values from the dataframe that answer my question. The data is {df}"""}]
    messages = system_message + messages
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages
    )
    return response.choices[0].message.content

def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            response_format="text",
            file=audio_file
        )
    return transcript

def text_to_speech(input_text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=input_text
    )
    webm_file_path = "temp_audio_play.mp3"
    with open(webm_file_path, "wb") as f:
        response.stream_to_file(webm_file_path)
    return webm_file_path

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)