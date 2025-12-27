# Spendly

<p align="center">
  <img src="logo.png" alt="Spendly Logo" width="200"/>
</p>

<p align="center">
  <strong>Smart expense tracking powered by AI</strong>
</p>

<p align="center">
  An intelligent money tracker that learns from your spending habits and automatically categorizes expenses using AI.
</p>

## Features

- AI-Powered Categorization - Automatically categorize expenses using Claude AI
- Smart Analytics - Beautiful insights into your spending patterns
- Native iOS Experience - Built with React Native and Expo
- Privacy First - Your financial data stays secure
- Beautiful UI/UX - Intuitive and modern design
- Open Source - MIT licensed, contributions welcome

## Project Structure
```
spendly/
├── mobile/          # React Native + Expo app
├── backend/         # FastAPI Python backend
├── docker-compose.yml
└── logo.png
```

## Getting Started

### Prerequisites

- Node.js 20+
- Python 3.11+
- Docker Desktop
- Expo Go app on your iPhone
- Claude API key from https://console.anthropic.com

### Backend Setup

1. Create virtual environment:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

4. Start PostgreSQL:
```bash
cd ..
docker compose up -d
```

5. Run the backend:
```bash
cd backend
uvicorn app.main:app --reload
```

Backend API: http://localhost:8000

API docs: http://localhost:8000/docs

### Mobile Setup

1. Install dependencies:
```bash
cd mobile
npm install
```

2. Start Expo development server:
```bash
npm start
```

3. Run on your iPhone:
    - Open Expo Go app on your iPhone
    - Scan the QR code displayed in the terminal
    - Make sure your iPhone and Mac are on the same WiFi network

## Tech Stack

### Mobile
- React Native - Cross-platform mobile framework
- Expo - Development platform for React Native
- TypeScript - Type-safe JavaScript

### Backend
- FastAPI - Modern Python web framework
- SQLAlchemy - SQL toolkit and ORM
- PostgreSQL - Relational database
- Anthropic Claude - AI for expense categorization

### Infrastructure
- Docker - Containerization
- Docker Compose - Multi-container orchestration

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Contributing

Contributions are welcome! This is an open-source project.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Author

Nicolò Calcagno - AI Engineer & Software Engineer

## Acknowledgments

- Powered by Anthropic Claude for AI categorization
- Built with Expo and FastAPI