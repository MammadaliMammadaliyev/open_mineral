# Open Mineral - Business Confirmation System

A comprehensive Django-based business confirmation system for mineral trading deals, featuring AI-powered suggestions, automated processing, and real-time task monitoring.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Docker Deployment](#docker-deployment)
- [API Documentation](#api-documentation)
- [Database Models](#database-models)
- [Scripts & Management](#scripts--management)
- [Logging & Monitoring](#logging--monitoring)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

Open Mineral is a sophisticated business confirmation system designed for mineral trading operations. It provides a complete workflow for creating, managing, and processing business confirmation deals with integrated AI suggestions and automated task processing.

### Key Capabilities

- **Deal Management**: Create and manage business confirmation deals
- **AI Integration**: Smart suggestions for deal optimization
- **Automated Processing**: Background task processing with Celery
- **Real-time Monitoring**: Task status tracking and progress updates
- **Comprehensive API**: RESTful API with Swagger documentation
- **Multi-tenant Support**: User-based deal management

## 🏗️ Project Structure

```
open_mineral/
├── bc/                                    # Django project root
│   ├── bc/                               # Main Django settings
│   │   ├── __init__.py
│   │   ├── settings.py                   # Django configuration
│   │   ├── urls.py                       # Main URL routing
│   │   ├── wsgi.py                       # WSGI configuration
│   │   ├── asgi.py                       # ASGI configuration
│   │   └── celery.py                     # Celery configuration
│   ├── deals/                            # Main application
│   │   ├── models/                       # Database models
│   │   │   ├── bc_deal.py               # Main deal model
│   │   │   ├── commercial_terms.py      # Commercial terms model
│   │   │   ├── payment_terms.py         # Payment terms model
│   │   │   ├── dropdown.py              # Dropdown options model
│   │   │   ├── new_business_confirmation.py
│   │   │   └── task_status.py           # Task status tracking
│   │   ├── views/                        # API views
│   │   │   ├── bc_deal_views.py         # Deal management views
│   │   │   ├── commercial_terms_views.py
│   │   │   ├── payment_terms_views.py
│   │   │   ├── dropdown_views.py
│   │   │   ├── ai_suggestions_views.py  # AI integration
│   │   │   ├── submit_views.py          # Deal submission
│   │   │   └── new_business_confirmation_views.py
│   │   ├── serializers.py               # API serializers
│   │   ├── urls.py                      # API URL routing
│   │   ├── services/                    # Business logic
│   │   │   └── ai_suggestions.py       # AI service
│   │   ├── tasks/                       # Celery tasks
│   │   │   └── processing_tasks.py     # Background tasks
│   │   ├── management/                  # Django management commands
│   │   │   └── commands/               # Custom commands
│   │   ├── migrations/                  # Database migrations
│   │   └── tests/                       # Test suite
│   ├── logs/                            # Application logs
│   ├── staticfiles/                     # Static files
│   ├── assay_files/                     # File uploads
│   ├── manage.py                        # Django management script
│   └── db.sqlite3                       # SQLite database (dev)
├── scripts/                             # Utility scripts
│   ├── build.sh                        # Docker build script
│   ├── runlocal.sh                     # Local development
│   ├── makemigrations.sh               # Migration script
│   ├── createsuperuser.sh              # User creation
│   └── env.sh                          # Environment setup
├── requirements.txt                     # Python dependencies
├── Dockerfile                          # Docker configuration
├── docker-compose.yml                  # Multi-service orchestration
├── .env.example                        # Environment template
├── .dockerignore                       # Docker ignore rules
├── docker-start.sh                     # Docker startup script
├── docker-stop.sh                      # Docker shutdown script
└── DOCKER_README.md                    # Docker-specific documentation
```

## ✨ Features

### Core Features
- **Business Confirmation Deals**: Complete deal lifecycle management
- **Commercial Terms**: Detailed commercial terms configuration
- **Payment Terms**: Flexible payment structure setup
- **Dropdown Options**: Dynamic form field options with caching
- **AI Suggestions**: Intelligent recommendations for deal optimization
- **Task Processing**: Asynchronous background task processing
- **Real-time Status**: Live task status monitoring

### Technical Features
- **RESTful API**: Comprehensive API with Swagger documentation
- **Authentication**: User-based access control
- **Caching**: Redis-based intelligent caching
- **Logging**: Comprehensive logging system
- **File Uploads**: Secure file handling for assay documents
- **Database Migrations**: Automated schema management
- **Docker Support**: Complete containerization

## 🛠️ Technology Stack

### Backend
- **Django 5.2.6**: Web framework
- **Django REST Framework**: API framework
- **Celery 5.5.3**: Task queue
- **Redis 7**: Cache and message broker
- **PostgreSQL 15**: Primary database
- **SQLite**: Development database

### Frontend & Documentation
- **Swagger UI**: API documentation
- **ReDoc**: Alternative API documentation
- **Django Admin**: Administrative interface

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-service orchestration
- **Gunicorn**: WSGI server
- **Flower**: Celery monitoring

## 📋 Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git

## 🚀 Installation & Setup

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd open_mineral
   ```

2. **Start all services**
   ```bash
   ./docker-start.sh
   ```

3. **Access the application**
   - Web Application: http://localhost:8000
   - API Documentation: http://localhost:8000/swagger/
   - Celery Monitoring: http://localhost:5555
   - Admin Interface: http://localhost:8000/admin/

### Option 2: Local Development

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run migrations**
   ```bash
   ./scripts/makemigrations.sh
   ```

5. **Start development server**
   ```bash
   ./scripts/runlocal.sh
   ```

## 🐳 Docker Deployment

### Services Overview

| Service | Port | Description |
|---------|------|-------------|
| web | 8000 | Django web application |
| db | 5432 | PostgreSQL database |
| redis | 6379 | Redis cache & message broker |
| flower | 5555 | Celery monitoring dashboard |

### Quick Commands

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop all services
docker compose down

# Rebuild and restart
docker compose up --build

# Access specific service
docker compose exec web python manage.py shell
docker compose exec db psql -U postgres -d open_mineral
```

### Environment Configuration

Create `.env` file from template:
```bash
cp .env.example .env
```

Key environment variables:
```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Settings
DB_NAME=open_mineral
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Redis Settings
REDIS_URL=redis://redis:6379/0

# Celery Settings
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Authentication
All endpoints require authentication. Use Django's built-in authentication system.

### Main Endpoints

#### Business Confirmation Deals
- `GET /api/business-confirmation-deals/` - List all deals
- `POST /api/business-confirmation-deals/` - Create new deal

#### Commercial Terms
- `GET /api/commercial-terms/` - List commercial terms
- `POST /api/commercial-terms/` - Create commercial terms

#### Payment Terms
- `GET /api/payment-terms/` - List payment terms
- `POST /api/payment-terms/` - Create payment terms

#### Dropdown Options
- `GET /api/dropdowns/` - Get all dropdown options (cached)

#### AI Suggestions
- `POST /api/ai-suggestions/` - Get AI-powered suggestions

#### Deal Submission
- `POST /api/deals/{deal_id}/submit/` - Submit deal for processing

#### Task Status
- `GET /api/task-status/{task_id}/` - Get task processing status

### API Documentation
- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **Schema JSON**: http://localhost:8000/swagger.json

## 🗄️ Database Models

### Core Models

#### BusinessConfirmationDeal
Main deal entity with status tracking:
- `id`: UUID primary key
- `user`: Foreign key to User
- `status`: Deal status (draft, submitted, processing, completed, cancelled)
- `created_at`, `updated_at`: Timestamps

#### NewBusinessConfirmation
Basic deal information:
- `seller`, `buyer`: Company names
- `material`: Material type
- `quantity`: Quantity with validation
- `created_at`, `updated_at`: Timestamps

#### CommercialTerms
Commercial terms configuration:
- Delivery terms (delivery_term, delivery_point, packaging)
- Transport details (transport_mode, inland_freight_buyer)
- Shipment periods (shipment_start_date, shipment_end_date)
- Pricing (treatment_charge, refining_charge, etc.)

#### PaymentTerms
Payment structure:
- Payment stages and percentages
- Currency and payment methods
- Credit terms and guarantees

#### TaskStatus
Background task tracking:
- `task_id`: Celery task identifier
- `deal`: Related deal
- `status`: Task status (pending, processing, completed, failed)
- `message`: Status details or error information

#### DropdownOption
Dynamic form options:
- `field_name`: Form field identifier
- `option_values`: JSON field with display options
- `display_order`: Sorting order
- `tooltip_text`: Help text
- `is_active`: Active status

## 🔧 Scripts & Management

### Available Scripts

#### Docker Scripts
- `./docker-start.sh` - Start all services with setup
- `./docker-stop.sh` - Stop all services

#### Development Scripts
- `./scripts/runlocal.sh` - Start local development server
- `./scripts/makemigrations.sh` - Run database migrations
- `./scripts/build.sh` - Build and start Docker services
- `./scripts/createsuperuser.sh` - Create admin user
- `./scripts/env.sh` - Environment setup

### Django Management Commands

#### Available Commands
```bash
# Database operations
python manage.py makemigrations
python manage.py migrate
python manage.py migrate --fake-initial

# User management
python manage.py createsuperuser
python manage.py changepassword <username>

# Static files
python manage.py collectstatic --noinput

# Development
python manage.py runserver
python manage.py shell
python manage.py dbshell

# Custom commands
python manage.py populate_all
python manage.py populate_bc_deals
python manage.py populate_commercial_terms
python manage.py populate_dropdown_options
python manage.py populate_payment_terms
python manage.py populate_additional_clauses
python manage.py populate_new_business_confirmations
```

## 📊 Logging & Monitoring

### Logging Configuration

Logs are written to:
- **Console**: Real-time output
- **File**: `logs/business_confirmation.log`

### Log Levels
- **INFO**: General application flow
- **DEBUG**: Detailed debugging information
- **WARNING**: Potential issues
- **ERROR**: Error conditions

### Monitoring

#### Celery Monitoring
- **Flower Dashboard**: http://localhost:5555
- Monitor task queues, workers, and task execution
- View task details and results

#### Database Monitoring
```bash
# PostgreSQL logs
docker compose logs db

# Database shell access
docker compose exec db psql -U postgres -d open_mineral
```

#### Application Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f web
docker compose logs -f celery
```

## 🛠️ Development

### Code Structure

#### Models
Located in `bc/deals/models/`:
- Each model in separate file
- Comprehensive field validation
- Proper relationships and constraints

#### Views
Located in `bc/deals/views/`:
- Class-based views
- Swagger documentation
- Proper error handling
- Logging integration

#### Serializers
Located in `bc/deals/serializers.py`:
- DRF serializers for API
- Validation and transformation
- Nested relationships

#### Services
Located in `bc/deals/services/`:
- Business logic separation
- AI integration services
- Reusable components

### Adding New Features

1. **Create Model**
   ```bash
   # Add model to appropriate file in models/
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create Serializer**
   ```python
   # Add to serializers.py
   class NewModelSerializer(serializers.ModelSerializer):
       class Meta:
           model = NewModel
           fields = '__all__'
   ```

3. **Create View**
   ```python
   # Add to appropriate views file
   class NewModelView(APIView):
       permission_classes = [IsAuthenticated]
       # Implement get, post methods
   ```

4. **Add URL**
   ```python
   # Add to urls.py
   path('new-model/', NewModelView.as_view(), name='new-model')
   ```

### Testing

```bash
# Run tests
python manage.py test

# Run specific test
python manage.py test deals.tests.test_models

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🐛 Troubleshooting

### Common Issues

#### Docker Issues
```bash
# Clean up Docker
docker compose down -v
docker system prune -a

# Rebuild from scratch
docker compose build --no-cache
docker compose up
```

#### Database Issues
```bash
# Reset migrations
rm bc/deals/migrations/0*.py
python manage.py makemigrations
python manage.py migrate

# Reset database
rm db.sqlite3
python manage.py migrate
```

#### Celery Issues
```bash
# Check Celery status
docker compose exec celery celery -A bc status

# Restart Celery
docker compose restart celery
```

#### Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
chmod +x *.sh scripts/*.sh
```

### Debug Mode

Enable debug mode in `.env`:
```env
DEBUG=True
```

View detailed logs:
```bash
docker compose logs -f web
```

### Performance Issues

1. **Check Redis connection**
2. **Monitor Celery workers**
3. **Review database queries**
4. **Check memory usage**

## 📞 Support

For issues and questions:
1. Check the logs: `docker compose logs -f`
2. Review this documentation
3. Check API documentation: http://localhost:8000/swagger/
4. Monitor Celery tasks: http://localhost:5555

## 📄 License

[Add your license information here]

---

**Happy Trading! 🚀**
