from fastapi import FastAPI
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import numpy as np
app = FastAPI()
import os
import requests
import json

from azure.storage.blob import BlobServiceClient

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from googletrans import Translator
translator = Translator()

@app.get("/hello")
def hello():
  return {"Hello world!"}

uri = "https://lilablobssc.blob.core.windows.net/snapshotserengeti-unzipped/"

df = pd.read_csv("animal_df_test_real.csv")

nombre_clases = ['baboon', 'buffalo', 'cheetah', 'dikdik', 'eland', 'elephant','gazellegrants','gazellethomsons','giraffe','guineafowl',
                'hartebeest','hippopotamus','hyenaspotted','impala','koribustard','lionfemale','ostrich','otherbird','reedbuck','topi','warthog','wildebeest','zebra']
name_clases = []
for name in nombre_clases:
    name_clases.append(translator.translate(name, dest='es').text.capitalize())
@app.get("/random")
def random():
    random_animal = df.sample()
    print(random_animal)
    print("xd")
    image_url = uri + random_animal["image_id"].values[0] + ".JPG"    
    img_data = requests.get(image_url).content
    with open('image_name.jpg', 'wb') as handler:
        handler.write(img_data)   
    print(image_url)    
    animal_category = translator.translate(random_animal["category_name"].values[0]  , dest='es').text.capitalize()
    animal_test_path = 'image_name.jpg'
    model = tf.keras.models.load_model('model_sinPCA.h5')
    img = tf.keras.utils.load_img(
        animal_test_path, target_size=(224, 224)
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    tabla_confianza=pd.DataFrame(columns=['animal','porcentaje_confianza'])

    tabla_confianza['animal']=name_clases
    tabla_confianza['porcentaje_confianza']=100*score
    tabla_confianza['porcentaje_confianza']=[round(num,3) for num in tabla_confianza['porcentaje_confianza']]
    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
        .format(name_clases[np.argmax(score)], 100 * np.max(score))
    )
    tabla_confianza = tabla_confianza.sort_values('porcentaje_confianza',ascending=False)
    table_dict = tabla_confianza.to_json(orient="records")
    parsed = json.loads(table_dict)
    json.dumps(parsed, indent=4) 
    return parsed, animal_category, image_url

@app.get("/random/")
def get_url_category(animal:str):
    animal = animal
    random_animal = df[df['category_name']==animal].sample()
    print(random_animal)
    print("xd")
    image_url = uri + random_animal["image_id"].values[0] + ".JPG"    
    img_data = requests.get(image_url).content
    with open('image_name.jpg', 'wb') as handler:
        handler.write(img_data)   
    return image_url

@app.get("/table")
def get_table(pca: str):
    animal_test_path = 'image_name.jpg'
    if(pca == 'SIN'):
        model = tf.keras.models.load_model('model_sinPCA.h5')
    else:
        model = tf.keras.models.load_model('model_conPCA.h5')  
    img = tf.keras.utils.load_img(
        animal_test_path, target_size=(224, 224)
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    tabla_confianza=pd.DataFrame(columns=['animal','porcentaje_confianza'])

    tabla_confianza['animal']=name_clases
    tabla_confianza['porcentaje_confianza']=100*score
    tabla_confianza['porcentaje_confianza']=[round(num,3) for num in tabla_confianza['porcentaje_confianza']]
    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
        .format(name_clases[np.argmax(score)], 100 * np.max(score))
    )
    tabla_confianza = tabla_confianza.sort_values('porcentaje_confianza',ascending=False)
    table_dict = tabla_confianza.to_json(orient="records")
    parsed = json.loads(table_dict)
    json.dumps(parsed, indent=4)     
    return parsed

    



