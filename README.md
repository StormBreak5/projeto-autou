# Full Stack Application

This project contains both frontend and backend components for a complete web application.

## Project Structure

```
├── backend/          # Python backend (Flask/FastAPI)
│   ├── main.py
│   ├── requirements.txt
│   └── venv/
└── frontend/         # Angular frontend
    ├── src/
    ├── package.json
    └── angular.json
```

## Getting Started

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python main.py
```

### Frontend Setup

```bash
cd frontend
npm install
ng serve
```

## Development

- Backend runs on: http://localhost:5000 (or configured port)
- Frontend runs on: http://localhost:4200

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
