# Betting Application

A comprehensive betting application built with Flutter (frontend) and Python FastAPI (backend) as per the MOU specifications.

## Features

### User Features
- **User Authentication and Authorization**: Registration, login, and secure authentication
- **Game Interface**: Interactive gameplay with real-time updates
- **Betting Functionalities**: Place bets, view odds, and manage betting history
- **Wallet Management**: Secure deposits and withdrawals
- **Notification System**: Real-time updates for game results and promotions

### Admin Features
- **Super Admin Panel**: Full control over application, user management, and revenue tracking
- **Admin Panel**: Limited permissions for daily operations management
- **Game Management**: Create, update, and manage games
- **User Management**: View and manage user accounts
- **Transaction Monitoring**: Track all financial transactions

### Technical Features
- **Payment Integration**: Secure payment gateway integration
- **Cross-platform Compatibility**: Web and mobile support
- **Scalable Infrastructure**: Built for high availability
- **Security**: JWT authentication, encrypted data storage

## Technologies Used

### Backend
- **Python FastAPI**: High-performance web framework
- **PostgreSQL**: Primary database
- **Redis**: Caching and session management
- **SQLAlchemy**: ORM for database operations
- **Alembic**: Database migrations
- **JWT**: Authentication tokens
- **Stripe**: Payment processing

### Frontend
- **Flutter**: Cross-platform mobile/web development
- **Bloc**: State management
- **Dio**: HTTP client
- **Hive**: Local storage
- **Go Router**: Navigation
- **Firebase**: Push notifications

## Project Structure

```
betting_app/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── security.py
│   │   │   └── deps.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── game.py
│   │   │   ├── bet.py
│   │   │   ├── transaction.py
│   │   │   └── notification.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   └── betting.py
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   └── games.py
│   │   └── services/
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── lib/
│   │   ├── core/
│   │   │   ├── constants/
│   │   │   ├── network/
│   │   │   └── storage/
│   │   ├── features/
│   │   │   ├── auth/
│   │   │   ├── games/
│   │   │   ├── betting/
│   │   │   ├── wallet/
│   │   │   └── profile/
│   │   └── shared/
│   │       ├── widgets/
│   │       ├── models/
│   │       └── themes/
│   ├── pubspec.yaml
│   └── main.dart
└── docs/
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Flutter SDK 3.0+
- PostgreSQL 12+
- Redis
- Node.js (for additional tools)

### Backend Setup

1. **Clone the repository and navigate to backend directory**
   ```bash
   cd betting_app/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Set up database**
   ```bash
   # Create PostgreSQL database
   createdb betting_db
   
   # Run migrations
   alembic upgrade head
   ```

6. **Run the application**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd betting_app/frontend
   ```

2. **Install dependencies**
   ```bash
   flutter pub get
   ```

3. **Run the application**
   ```bash
   # For mobile
   flutter run
   
   # For web
   flutter run -d web-server --web-hostname 0.0.0.0 --web-port 8080
   ```

## Environment Variables

### Backend (.env)
```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/betting_db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Payment Gateway
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key

# Redis
REDIS_URL=redis://localhost:6379

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## API Documentation

Once the backend is running, you can access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Database Schema

### Users Table
- Authentication and user management
- Role-based access control
- Profile information

### Games Table
- Game definitions and configurations
- Game types and settings
- Status management

### Bets Table
- Betting history and current bets
- Odds and payouts
- Bet status tracking

### Transactions Table
- Financial transaction history
- Deposits and withdrawals
- Wallet balance tracking

### Notifications Table
- User notifications
- Push notification management
- Notification status

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: BCrypt for password security
- **Input Validation**: Comprehensive request validation
- **CORS Configuration**: Cross-origin resource sharing
- **Rate Limiting**: API rate limiting for security
- **Data Encryption**: Sensitive data encryption

## Payment Integration

The application supports payment gateway integration:
- **Stripe**: Credit/debit card processing
- **Webhook Handling**: Real-time payment notifications
- **Secure Transactions**: PCI compliance
- **Multiple Currencies**: Support for various currencies

## Development Guidelines

### Code Style
- **Backend**: Follow PEP 8 guidelines
- **Frontend**: Follow Flutter/Dart conventions
- **Git**: Use conventional commits

### Testing
- **Backend**: pytest for unit and integration tests
- **Frontend**: flutter test for widget and unit tests
- **API**: Postman collections for API testing

### Deployment
- **Backend**: Docker containerization
- **Frontend**: Web deployment to CDN
- **Database**: Production PostgreSQL setup
- **Monitoring**: Application monitoring and logging

## Support and Maintenance

### Documentation
- API documentation in `/docs`
- User manuals for end users
- Admin guides for administrators

### Monitoring
- Application performance monitoring
- Error tracking and logging
- User activity analytics

### Updates
- Regular security updates
- Feature enhancements
- Bug fixes and improvements

## License

This project is proprietary software developed as per the MOU specifications.

## Contact

For technical support and inquiries, please contact the development team.
