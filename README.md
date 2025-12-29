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

- AI-Powered Categorization - Automatically categorize expenses using OpenAI GPT-4o-mini
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
- Docker Desktop
- Expo Go app on your iPhone
- OpenAI API key from https://platform.openai.com

### Quick Start with Docker (Recommended)

1. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

2. Start all services:
```bash
docker compose up -d --build
```

3. Run database migrations:
```bash
docker compose exec backend alembic upgrade head
```

4. Seed default categories:
```bash
docker compose exec backend python scripts/seed_categories.py
```

Backend API: http://localhost:8000

API docs: http://localhost:8000/docs

To view logs:
```bash
docker compose logs -f backend
```

To stop services:
```bash
docker compose down
```

### Alternative: Local Development Setup

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
cd ..
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

4. Start PostgreSQL only:
```bash
docker compose up -d postgres
```

5. Run database migrations:
```bash
cd backend
alembic upgrade head
```

6. Seed default categories:
```bash
python scripts/seed_categories.py
```

7. Run the backend:
```bash
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
- OpenAI GPT-4o-mini - AI for expense categorization

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

- Powered by OpenAI GPT-4o-mini for AI categorization
- Built with Expo and FastAPI