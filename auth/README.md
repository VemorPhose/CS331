# Nexus Authentication System

A FastAPI-based authentication system for the Nexus Intelligent Chatbot platform, with JWT token support and SQLite database backend.

## Features

- **User Registration**: Create new user accounts with email and password
- **User Login**: Authenticate users and issue JWT tokens
- **Token-based Authorization**: OAuth2-compatible JWT token system
- **User Roles**: Support for GENERAL and ADMIN roles
- **Password Security**: Bcrypt hashing for secure password storage
- **SQLite Database**: File-based SQL database for fast prototyping
- **Pydantic Models**: Request/response validation
- **FastAPI Integration**: Modern async Python web framework

## Project Structure

```
auth/
├── main.py          # FastAPI application and routes
├── auth.py          # Authentication logic (JWT, password hashing)
├── models.py        # Pydantic models for validation
├── database.py      # SQLite database operations
├── config.py        # Configuration settings
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## Installation

1. **Navigate to the auth directory:**
   ```bash
   cd auth
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. **POST /register**
Register a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "strongpassword123"
}
```

**Response (201 Created):**
```json
{
  "email": "user@example.com",
  "is_active": true,
  "role": "GENERAL"
}
```

### 2. **POST /login**
Login with email and password to get an access token.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "strongpassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. **POST /token**
OAuth2-compatible token endpoint.

**Request (Form Data):**
- `username`: Email address
- `password`: Password

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 4. **GET /me**
Get current authenticated user information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "email": "user@example.com",
  "is_active": true,
  "role": "GENERAL"
}
```

### 5. **GET /**
Health check endpoint.

**Response (200 OK):**
```json
{
  "message": "Nexus Auth API is running",
  "endpoints": {
    "register": "POST /register",
    "login": "POST /login",
    "token": "POST /token",
    "me": "GET /me (requires auth)"
  }
}
```

## Configuration

Edit `config.py` to customize settings:

```python
SECRET_KEY = "your-secret-key-change-in-production-min-32-chars-"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_URL = "sqlite:///./auth_system.db"
```

**Important:** Change the `SECRET_KEY` in production to a strong, random value.

## Database

The system uses **SQLite** with a single `users` table:

```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  hashed_password TEXT NOT NULL,
  is_active BOOLEAN DEFAULT 1,
  role TEXT DEFAULT 'GENERAL',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

The database is automatically initialized on first import of the `database` module.

## Usage Examples

### Example 1: Register a new user

```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

### Example 2: Login to get a token

```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

### Example 3: Access protected endpoint with token

```bash
curl -X GET "http://localhost:8000/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Security Features

- **Password Hashing**: Uses bcrypt for secure password storage
- **JWT Tokens**: Time-limited access tokens with expiration
- **Email Validation**: Validates email format using `email-validator`
- **Dependency Injection**: FastAPI's dependency system for clean auth flow
- **Secure Headers**: Proper HTTP security headers in responses

## Database Operations

The `database.py` module provides helper functions:

- `create_user(email, password, role)`: Create a new user
- `get_user(email)`: Retrieve user by email
- `user_exists(email)`: Check if user exists
- `delete_user(email)`: Delete a user
- `get_all_users()`: Get all users
- `update_user_role(email, role)`: Update user's role

## Error Handling

The API returns appropriate HTTP status codes:

- **200**: Success (GET requests)
- **201**: Created (POST /register)
- **400**: Bad Request (invalid input, duplicate email)
- **401**: Unauthorized (invalid credentials, invalid token)
- **404**: Not Found (user not found)
- **500**: Internal Server Error

## Integration with Nexus Platform

This authentication system is designed to integrate with the Nexus Intelligent Chatbot platform:

- **User Management**: Supports both GENERAL users and ADMIN roles
- **Token System**: Provides secure authentication tokens for API requests
- **Extensible**: Can be extended with additional user attributes and permissions
- **Database Ready**: SQLite backend is suitable for prototyping and small deployments

## Testing

To test the API, you can use:

1. **FastAPI UI**: Navigate to `http://localhost:8000/docs` (Swagger UI)
2. **ReDoc**: Navigate to `http://localhost:8000/redoc` (ReDoc UI)
3. **cURL**: Command-line API testing
4. **Postman**: Import the API endpoints for testing

## Performance Notes

- **SQLite**: Suitable for prototyping and development. For production with multiple concurrent users, consider PostgreSQL or MySQL.
- **JWT Tokens**: Stateless authentication reduces database queries
- **In-Memory Settings**: Configuration is cached using `@lru_cache()` for performance

## Future Enhancements

- OAuth2 with external providers (Google, GitHub)
- Email verification
- Password reset functionality
- Multi-factor authentication (MFA)
- Rate limiting
- User profile customization
- Permission-based authorization (RBAC)
- Audit logging

## License

See LICENSE file in the project root.

## Project References

This authentication system is part of the Nexus Intelligent Chatbot System. See the project documentation:

- **1_SRS/**: Software Requirements Specification
- **2_UML/**: UML diagrams and specifications
- **3_DFD/**: Data Flow Diagrams
- **4_COMP/**: Component and Architecture documentation
