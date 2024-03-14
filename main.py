import streamlit as st
import time 
from image_service import image_generator,image_converter,image_edit,image_variation,openai
from audio_service import file_to_chunks,text_to_speech,openai
import os




with st.sidebar:
    st.subheader("configuration:")
    api_key = st.text_input('enter api key',type='password')
    openai.api_key = api_key
    selectboxvalue = st.selectbox('select model',['image model','audio model'])
    # st.markdown(selectboxvalue)
    


if selectboxvalue == "image model":
    with st.sidebar:
        selectimagevalue = st.selectbox('select images',['image generator','image editor','image variation'])

    if selectimagevalue == "image generator": #image create logic
        if prompt:=st.chat_input("enter prompt for image generator"):
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.spinner('waiting image generate'):
                response_url = image_generator(prompt)
                with st.chat_message('assistant'):
                    st.image(response_url)


    elif selectimagevalue == "image editor": #image edit logic
        col1,col2 = st.columns(2)
        with col1:
            upload_image_1 = st.file_uploader('Upload Original Image',key='234234')
            if upload_image_1:
                st.image(upload_image_1)
                image_converter(upload_image_1,'original')
        with col2:
            upload_image_2 = st.file_uploader('Upload Fake Image',key='s34343')
            if upload_image_2:
                st.image(upload_image_2)
                image_converter(upload_image_2,'mask')

        if upload_image_1 and upload_image_2:
            if prompt:=st.chat_input("edit image"):
                with st.spinner('please wait image editing...'):
                    response_url=image_edit('original.png','mask.png',prompt)
                    st.image(response_url)
                # os.remove('mask.png')
                # os.remove('original.png')
                    os.remove(upload_image_1.name)
                    os.remove(upload_image_2.name)
        
            
    elif selectimagevalue == "image variation": #image variation logic
        col1,col2 = st.columns(2)
        with col1:
            upload_image = st.file_uploader('Upload Original Image',)
            if upload_image:
                st.image(upload_image)
                image_converter(upload_image,'variation')
        
        with col2:
            if upload_image:
                st.markdown("<p style='padding-top:20px'></p>", unsafe_allow_html=True)
                if st.button("image variation editing"):
                    st.markdown("<p style='padding-top:70px'></p>", unsafe_allow_html=True)

                    with st.spinner("please wait image created..."):

                        response_url=image_variation('variation.png')
                        st.image(response_url)
                        os.remove(upload_image.name)
                        os.remove('variation.png')

        
            
        
            
            
        
elif selectboxvalue == "audio model":
    select_audio_value = st.sidebar.selectbox('label select audio',['speech to text','text to speech'])
    if select_audio_value == "speech to text":
        st.title('Speech To Text')
        audio_file = st.file_uploader('upload audio file')
        if audio_file:
            if st.button("convert audio to text"):
                response_text = file_to_chunks(audio_file) 
                if response_text:
                    st.subheader('speech text')
                    st.markdown(response_text)
                    
    if select_audio_value == "text to speech":
        st.title('Text to Speech')
        user_input = st.text_area('enter a text')
        voice_type = st.selectbox("select voice",['alloy'])
        if st.button('converte text to audio'):
            speech_file_path = text_to_speech(user_input,voice_type)  
            with open(speech_file_path,'rb') as audio_file: 
                audio_byte = audio_file.read()
                st.audio(audio_byte,format='audio/mp3')



