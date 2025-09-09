# Potato Disease Classification API

A FastAPI-based web service and lightweight frontend for image-based plant disease classification across 15 classes (pepper, potato, and tomato). The backend loads a TensorFlow/Keras `.h5` model and exposes a `/predict/` endpoint. A simple HTML frontend is served at `/` to upload an image and view predictions.

## Features
- FastAPI backend with async file uploads
- TensorFlow/Keras inference on images
- 128×128 image preprocessing, normalization, RGB handling
- 15-class label set for pepper, potato, and tomato diseases/health
- Simple in-repo frontend (`frontend/index.html`) served by the API
- CORS enabled for easy local development

## Tech Stack
- **Backend**: FastAPI, Starlette
- **Model**: TensorFlow/Keras
- **Image**: Pillow (PIL)
- **Runtime**: Python 3.13

## Model and Labels
Model path: `models/Potato Disease Classification.h5`

Labels (index-aligned with model output):
- Pepper__bell___Bacterial_spot
- Pepper__bell___healthy
- Potato___Early_blight
- Potato___Late_blight
- Potato___healthy
- Tomato_Bacterial_spot
- Tomato_Early_blight
- Tomato_Late_blight
- Tomato_Leaf_Mold
- Tomato_Septoria_leaf_spot
- Tomato_Spider_mites_Two_spotted_spider_mite
- Tomato__Target_Spot
- Tomato__Tomato_YellowLeaf__Curl_Virus
- Tomato__Tomato_mosaic_virus
- Tomato_healthy

## Project Structure
```
.
├── app/
│   ├── __init__.py
│   └── main.py
├── frontend/
│   └── index.html
├── models/
│   └── Potato Disease Classification.h5
├── env/  (Python virtual environment)
├── requirements.txt
└── README.md
```

## Getting Started
1) Clone and enter the project directory
```bash
git clone <your-repo-url>.git
cd dog_cat_Api
```

2) Create/activate virtual environment (Windows)
- If you already have `env/`, activate it:
```bash
env\Scripts\activate
```
- Otherwise, create a new venv with Python 3.13:
```bash
python -m venv env
env\Scripts\activate
```

3) Install dependencies
```bash
pip install -r requirements.txt
```

4) Place the model file
- Ensure `models/Potato Disease Classification.h5` exists. If not, add it or update the path in `app/main.py`.

## Run the API
From the project root:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- Open the frontend: `http://127.0.0.1:8000/`
- Interactive API docs: `http://127.0.0.1:8000/docs`

## API
- **GET** `/`
  - Serves `frontend/index.html`.
- **POST** `/predict/`
  - Form-data with key `file` (image file)
  - Returns JSON: `{ filename, prediction, confidence }`

Example using curl:
```bash
curl -X POST -F "file=@pic1.jpg" http://127.0.0.1:8000/predict/
```

Example response:
```json
{
  "filename": "pic1.jpg",
  "prediction": "Potato___Late_blight",
  "confidence": 0.97
}
```

## Frontend Usage
- Navigate to `http://127.0.0.1:8000/`
- Click the upload area, choose an image (JPG/PNG), then "Upload & Predict"
- The page shows a preview and the predicted class with confidence

## Preprocessing Details
- Images are loaded via Pillow and converted to RGB to avoid alpha-channel issues
- Resized to 128×128 using Lanczos resampling
- Normalized to `[0,1]`
- Batched to shape `(1, 128, 128, 3)` before model inference

## Troubleshooting
- Error: "Could not import module 'main'"
  - Run Uvicorn with module path `app.main:app` from the project root
  - Ensure `app/__init__.py` exists
- Error: "expected axis -1 of input shape to have value 3, got ... 4"
  - The input image likely has an alpha channel (RGBA). The code converts to RGB in `app/main.py`. Ensure you are on the latest version and that `.convert("RGB")` is applied before converting to NumPy
- Model not found / wrong path
  - Verify `models/Potato Disease Classification.h5` exists and the path in `app/main.py` matches
- CORS issues when opening `index.html` directly from disk
  - CORS is enabled broadly. Prefer visiting `http://127.0.0.1:8000/` so the HTML is served by the backend

## Development Notes
- Update labels only if the model output ordering changes
- If you switch models or input size, keep preprocessing in sync
- You can add static files (CSS/JS) to `frontend/` and reference them directly from `index.html`

## Deployment
- Production command (example):
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
```
- Behind a reverse proxy (e.g., Nginx), terminate TLS at the proxy and forward to Uvicorn/Gunicorn
- Set environment variables and model paths as needed for your infra

## Contributing
- Open an issue for bugs or feature requests
- Use a feature branch and submit a PR
- Follow existing code style and keep functions small and readable

## License
Add your chosen license (e.g., MIT) in a `LICENSE` file.

## Acknowledgements
- FastAPI team for the web framework
- TensorFlow/Keras for the deep learning stack
- Pillow for image utilities
