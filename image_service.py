import streamlit as st 

from PIL import Image


import openai

client = openai




def image_generator(prompt:str)->str:
    response = client.images.generate(
        prompt=prompt,
        model="dall-e-2",
        size='1024x1024',
        quality='hd',
        n=1
    ) 

    image_url = response.data[0].url
    print(image_url)
    return image_url    
   

#this function is edit image using open ai api 
def image_edit(original,mask,prompt):
    original_bytes = open(original,'rb')
    mask_bytes = open(mask,'rb')
    response = client.images.edit(
        image=original_bytes,
        mask=mask_bytes,
        prompt=prompt,
        model='dall-e-2',
        n=1,
        size="1024x1024"
    )
    image_url = response.data[0].url
    return image_url
    



#this funtion is converte any type imang in png format and then save
def image_converter(image_path,image_name):
    if image_path:
        with open(image_path.name,'wb') as f:
            f.write(image_path.getbuffer())
            img = Image.open(image_path.name)
            converted_image = img.convert("RGBA")
            converted_image.save(f"{image_name}.png")
        

def image_variation(image_name):
    with open(image_name,'rb') as img_file:
        response = client.images.create_variation(
            image=img_file,
            n=1,
            model="dall-e-2",
            size="1024x1024"
        )
        image_url = response.data[0].url
        return image_url