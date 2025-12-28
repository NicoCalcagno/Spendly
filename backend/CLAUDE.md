# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Spendly is an AI-powered expense tracking application that uses Claude AI to automatically categorize expenses. This is the backend API service built with FastAPI, providing endpoints for the React Native mobile app.

## Development Commands

### Environment Setup
```bash
# Create virtual environment with uv (recommended - much faster)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies with uv
uv pip install -r requirements.txt

# Alternatively, use standard Python tools
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup environment variables
cp ../.env.example ../.env
# Edit ../.env and add your ANTHROPIC_API_KEY (optional for migrations)
```

### Running the Application
```bash
# Start PostgreSQL database (from project root)
cd ..
docker compose up -d

# Run the development server (from backend directory)
cd backend
uvicorn app.main:app --reload

# Access the API
# API: http://localhost:8000
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### Database Management
```bash
# Check PostgreSQL status
docker compose ps

# Create a new migration after model changes
alembic revision --autogenerate -m "Description of changes"

# Apply migrations to database
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# View migration history
alembic history

# Stop database
docker compose down

# Reset database (removes all data)
docker compose down -v
docker compose up -d
alembic upgrade head  # Reapply migrations
```

## Architecture

### Application Structure

The backend follows a layered architecture pattern:
- **models/** - SQLAlchemy ORM models (User, Category, Expense implemented)
- **schemas/** - Pydantic schemas for request/response validation
- **controllers/** - FastAPI route handlers (endpoints)
- **services/** - Business logic layer
- **repositories/** - Database access layer

### Database Schema

**User** (users table)
- id: UUID, primary key
- email: String, unique, indexed
- hashed_password: String
- full_name: String
- created_at, updated_at: DateTime

**Category** (categories table)
- id: UUID, primary key
- user_id: UUID, foreign key to users (nullable for default categories)
- name, description: String
- color: String (hex color for UI)
- icon: String (icon name for UI)
- is_default: Boolean (system vs user-created categories)
- created_at: DateTime

**Expense** (expenses table)
- id: UUID, primary key
- user_id: UUID, foreign key to users
- amount: Decimal(10, 2)
- description: String
- category_id: UUID, foreign key to categories
- expense_date: Date
- payment_method: String
- notes: Text (nullable)
- ai_suggested_category_id: UUID, foreign key to categories (nullable)
- ai_confidence_score: Float (nullable)
- created_at, updated_at: DateTime

### Core Components

**app/config.py** - Centralized configuration using Pydantic Settings
- Loads environment variables from `.env` file in project root
- Database connection string
- Anthropic API key for Claude integration
- App settings (name, debug mode)

**app/database.py** - Database connection and session management
- SQLAlchemy engine and session factory
- `get_db()` dependency for FastAPI routes
- Base class for ORM models

**app/main.py** - FastAPI application entry point
- CORS middleware configured for React Native app
- Basic health check endpoints
- Ready for route registration

### Technology Stack

- **FastAPI** - Web framework with automatic API documentation
- **SQLAlchemy 2.0** - ORM for PostgreSQL
- **Pydantic** - Data validation and settings management
- **Anthropic Claude** - AI integration for expense categorization
- **Alembic** - Database migrations (configured and active)
- **PostgreSQL** - Primary database (runs in Docker)

## Important Notes

### Environment Configuration
- The `.env` file is located in the **project root** (parent directory), not in `backend/`
- Environment variables: `ANTHROPIC_API_KEY` (optional), `DATABASE_URL` (has default)
- Database credentials default to: user=spendly, password=spendly, db=spendly
- `ANTHROPIC_API_KEY` is optional for running migrations, required for AI features

### Database Connection
- The application expects PostgreSQL running on `localhost:5432`
- Use `docker compose up -d` from project root to start the database
- Connection is managed through SQLAlchemy engine in `app/database.py`

### CORS Configuration
- Currently allows all origins (`allow_origins=["*"]`) for development
- Should be restricted to specific origins in production

### Code Organization Principles
When implementing new features:
1. Define database models in `app/models/`
2. Create Pydantic schemas in `app/schemas/` for validation
3. Implement data access in `app/repositories/`
4. Write business logic in `app/services/`
5. Add API endpoints in `app/controllers/`
6. Register routes in `app/main.py`

### Claude AI Integration
- The Anthropic SDK is installed for AI-powered expense categorization
- API key is configured via `ANTHROPIC_API_KEY` environment variable
- Integration code should go in `app/services/` when implemented
