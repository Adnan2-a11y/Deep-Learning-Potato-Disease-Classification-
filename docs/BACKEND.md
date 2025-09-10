## Backend Overview

This backend exposes a simple ML-powered image classification API (potato/tomato/pepper disease classes) and a lightweight FAQ-style chatbot. It is built with FastAPI and serves a static frontend.

### Tech stack and why
- **FastAPI**: Modern, fast Python web framework with automatic OpenAPI docs and Pydantic-based validation. Chosen for speed, developer experience, and async support.
- **Uvicorn**: ASGI server used to run FastAPI apps. Lightweight and performant.
- **TensorFlow/Keras**: Loads and executes the pre-trained CNN model (`.h5`) for disease classification.
- **NumPy**: Numerical manipulation of image tensors before inference.
- **Pillow (PIL)**: Image decoding, conversion to RGB, resizing.
- **CORS Middleware**: Enables requests from the frontend (served from the same server or different origin during development).


## Project structure (backend)

```
app/
  main.py                  # App entrypoint: FastAPI instance, CORS, routers, index serving
  routes/
    predict.py             # /predict endpoint and model loading
    chatbot.py             # /api/chatbot endpoint
    explain.py             # Disease info dictionary used for explanations
models/
  Potato Disease Classification2.0.h5    # TensorFlow/Keras model file
frontend/
  index.html               # Static frontend served from root route
```


## Application wiring

- `app/main.py`
  - Creates `FastAPI()` instance
  - Adds `CORSMiddleware` allowing all origins (development-friendly)
  - Includes routers:
    - `app.routes.chatbot` mounted at prefix `/api`
    - `app.routes.predict` mounted at root (no prefix)
  - Serves `frontend/index.html` at `GET /`

- `app/routes/predict.py`
  - Defines `router = APIRouter()` and `@router.post("/predict/")`
  - Loads the Keras model once at import time for performance
  - Preprocesses incoming image and returns prediction, confidence, and explanation

- `app/routes/chatbot.py`
  - Defines `router = APIRouter()` and `@router.get("/chatbot")` under the `/api` prefix
  - Provides very simple keyword-based responses using `explain.py`


## Endpoints

### GET /
- **Purpose**: Serve the static frontend page
- **Response**: `text/html` (contents of `frontend/index.html`)

### POST /predict/
- **Purpose**: Run disease classification on an uploaded image
- **Form field**: `file` (image/*)
- **Response**: JSON
  - `filename`: string
  - `prediction`: string (class label)
  - `confidence`: number (0..1, rounded to 2 decimals)
  - `explanation`: string (short description)

Example curl:
```bash
curl -X POST \
  -F "file=@/path/to/leaf.jpg" \
  http://127.0.0.1:8000/predict/
```

Example response:
```json
{
  "filename": "leaf.jpg",
  "prediction": "Potato___Late_blight",
  "confidence": 0.97,
  "explanation": "Late blight is caused by Phytophthora infestans..."
}
```

### GET /api/chatbot?query=...
- **Purpose**: Return a simple text answer about a disease if found
- **Query**: `query` (string)
- **Response**: `{ "answer": string }`

Example curl:
```bash
curl "http://127.0.0.1:8000/api/chatbot?query=What is late blight?"
```


## Model loading and inference

- The TensorFlow model is loaded once at module import in `predict.py`:
  - Minimizes per-request overhead
  - Ensures thread-safe reuse under FastAPI's async execution model
- Preprocessing pipeline (performed per request):
  - Decode image via Pillow
  - Convert to RGB; resize to 128x128 (LANCZOS)
  - Normalize to 0..1 (divide by 255)
  - Remove alpha channel if present
  - Add batch dimension and call `model.predict`


## CORS and security

- `CORSMiddleware` is configured to allow any origin, credentials, methods, and headers for development convenience.
- For production, consider tightening:
  - `allow_origins=["https://yourdomain.com"]`
  - Restrict methods/headers as needed


## Running locally

Assuming the virtual environment and dependencies are already installed:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open the app at `http://127.0.0.1:8000/`.


## Dependencies in requirements.txt (high level)

- fastapi: Web framework and routing
- uvicorn: ASGI server
- tensorflow / keras: Model loading and inference
- pillow: Image decoding and resizing
- numpy: Tensor manipulation
- python-multipart: Form-data parsing for file uploads
- starlette: Underlying ASGI toolkit used by FastAPI (transitive)


## Error handling

- Prediction route wraps inference in a `try/except` and returns `{ "error": str(e) }` on failure.
- Consider returning proper HTTP status codes (e.g., 400/422 for bad input, 500 for server errors) and structured error models in production.


## Notes and future improvements

- Move constants like `labels` and input size into a config module.
- Validate uploaded file type and size before processing.
- Add health and readiness endpoints (e.g., `/healthz`).
- Cache model warmup or add a startup event to pre-warm the model.
- Replace the simple chatbot with a more robust retrieval or LLM-backed endpoint.


