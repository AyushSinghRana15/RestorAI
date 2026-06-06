# RestorAI – AI-Powered Image Restoration & Enhancement Framework

RestorAI is a deep learning-based web application designed to restore and enhance old, damaged, and low-quality photographs. The platform combines multiple state-of-the-art computer vision models to repair scratches, recover missing details, restore facial features, colorize black-and-white images, and upscale image resolution.

## Features

- 🖼️ Old photo restoration
- 👤 Face enhancement with identity preservation
- 🎨 Black-and-white image colorization
- 🔧 Scratch and damage removal
- 🚀 AI-powered super-resolution upscaling
- 📊 Before/After comparison interface
- ☁️ Cloud-based deployment and processing

## Tech Stack

- **Frontend:** React, Vite, Tailwind CSS
- **Backend:** FastAPI, Python
- **AI Models:** GFPGAN, Real-ESRGAN, LaMa, DeOldify
- **Deployment:** Vercel, Hugging Face Spaces
- **Storage:** Cloudinary

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+

### Backend Setup (Virtual Environment)

```bash
# Create and activate virtual environment (if not already done)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the backend
python -m backend.run
```

The API will be available at `http://localhost:8000`.

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

The frontend will be available at `http://localhost:5173`.

### Build for Production

```bash
# Backend
# (ensure venv is activated)
python -m backend.run

# Frontend
cd frontend && npm run build
```

## Objective

To provide an accessible AI-powered solution for restoring and preserving old photographs, enabling users to recover valuable memories with minimal manual intervention.
