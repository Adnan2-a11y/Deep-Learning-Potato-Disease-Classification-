from fastapi import FastAPI,File,UploadFile
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np


app = FastAPI()

#model = load_model("models/best_dogcat.h5")
#print("Model loaded! 🐾 Ready for predictions")
#
#def prepare_image(file):
#    # Load the uploaded image into PIL format
#    img = image.load_img(file, target_size=(128,128))  # Resize to 128x128
#    img_array = image.img_to_array(img)                # Convert to NumPy array
#    img_array = img_array / 255.0                      # Normalize
#    img_array = np.expand_dims(img_array, axis=0)      # Add batch dimension
#    return img_array

def upload_image(file):
    img=image.load_img(file,target_size=(128,128))
    img_array=image.image_to_array(img)
    img_array=img_array/255.0
    img_array=np.expand
@app.get("/")
def home():
    return {"message": "Hello! Dog vs Cat API is awake 😺🐶"}
@app.get("predict")
def predict(file: UploadFile = File(...)):
    img = prepare_image(file.file)
    
    # Step 2: Predict
    pred = model.predict(img)[0][0]  # assuming binary classification output
    
    # Step 3: Convert prediction to label
    label = "Dog 🐶" if pred > 0.5 else "Cat 🐱"
    
    return {"filename": file.filename, "prediction": label, "confidence": float(pred)}
