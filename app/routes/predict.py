from fastapi import APIRouter, File, UploadFile
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import app.routes.explain as explain  # expects explain.disease_info

router = APIRouter()

# Load model once
model = tf.keras.models.load_model('models/Potato Disease Classification2.0.h5')

labels = [
  'Pepper__bell___Bacterial_spot',
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
  'Tomato_healthy'
]

@router.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        content = await file.read()
        image = Image.open(io.BytesIO(content)).convert("RGB")
        image = image.resize((128, 128), Image.Resampling.LANCZOS)
        image_array = np.array(image) / 255.0
        if image_array.shape[-1] == 4:
            image_array = image_array[..., :3]
        image_array = np.expand_dims(image_array, axis=0)

        prediction = model.predict(image_array)
        class_index = int(np.argmax(prediction[0]))
        confidence = float(np.max(prediction[0]))

        result = labels[class_index]
        explanation = explain.disease_info.get(result, "No explanation available.")

        return {
            "filename": file.filename,
            "prediction": result,
            "confidence": round(confidence, 2),
            "explanation": explanation
        }
    except Exception as e:
        return {"error": str(e)}