from fastapi import FastAPI,File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated

import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model=tf.keras.models.load_model('models/Potato Disease Classification.h5')

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

@app.post("/predict/")
async def predict(file: UploadFile=File(...)):
    content=await file.read()
    image = Image.open(io.BytesIO(content)).convert("RGB")
    image = image.resize((128,128),Image.Resampling.LANCZOS)
    image_array =np.array(image)/255.0
    if image_array.shape[-1] == 4:
       image_array = image_array[..., :3]
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
    
    
    prediction = model.predict(image_array)
    class_index = np.argmax(prediction[0])  # get index of highest probability
    confidence = float(np.max(prediction[0]))

    labels = ['Pepper__bell___Bacterial_spot',
              'Pepper__bell___healthy',
              'Potato___Early_blight',
              'Potato___Late_blight',
              'Potato___healthy',
              'Tomato_Bacterial_spot',
              'Tomato_Early_blight',
              'Tomato_Late_blight',
              'Tomato_Leaf_Mold',
              'Tomato_Septoria_leaf_spot',
              'Tomato_Spider_mites_Two_spotted_spider_mite',
              'Tomato__Target_Spot',
              'Tomato__Tomato_YellowLeaf__Curl_Virus',
              'Tomato__Tomato_mosaic_virus',
              'Tomato_healthy']
    result = labels[class_index]

    return {
        "filename": file.filename,
        "prediction": result,
        "confidence": round(confidence, 2)
    }

@app.get("/")
async def serve_index():
    return FileResponse("frontend/index.html", media_type="text/html")