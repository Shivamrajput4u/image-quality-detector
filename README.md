# Image Quality & Defect Detection

Full-stack AI application that analyzes an uploaded image and evaluates its visual
quality — detecting blur, underexposure, overexposure, noise, corruption, and
potential visual defects — without relying on external AI/vision APIs.

## Status

Project scaffolding in progress. Setup, training, and deployment instructions
will be filled in as each part is built.

## Stack

- Backend: FastAPI (Python)
- AI/ML: PyTorch (autoencoder-based anomaly detection) + classical CV features (OpenCV)
- Database: SQLite via SQLAlchemy
- Frontend: React (Vite)
- Deployment: Docker Compose
