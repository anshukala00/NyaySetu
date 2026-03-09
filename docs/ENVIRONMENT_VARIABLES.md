# Environment Variables Documentation

This document describes all environment variables used in the Nyaysetu Case Management System.

## Backend Environment Variables

### Required Variables

#### DATABASE_URL
- **Description**: PostgreSQL database connection string
- **Format**: `postgresql://username:password@host:port/database`
- **Example**: `postgresql://nyaysetu_user:nyaysetu_pass@localhost:5432/nyaysetu`
- **Required**: Yes
- **Notes**: 
  - Use strong passwords in production
  - Consider using connection pooling for production deployments
  - Ensure the database exists before starting the application

#### JWT_SECRET
- **Description**: Secret key used for signing JWT tokens
- **Format**: String (recommended: 32+ characters, URL-safe base64)
- **Example**: `Z37fPkoMXIxmbkJrQcNjNRttxImEm1_9Ccir5VKuKzY`
- **Required**: Yes
- **Security**: 
  - MUST be changed from default in production
  - Keep this secret secure and never commit to version control
  - Generate using: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
  - Changing this will invalidate all existing JWT tokens

#### JWT_ALGORITHM
- **Description**: Algorithm used for JWT token signing
- **Format**: String
- **Default**: `HS256`
- **Allowed Values**: `HS256`, `HS384`, `HS512`
- **Required**: Yes
- **Notes**: HS256 is recommended for most use cases

#### JWT_EXPIRATION_HOURS
- **Description**: JWT token expiration time in hours
- **Format**: Integer
- **Default**: `24`
- **Example**: `24` (tokens expire after 24 hours)
- **Required**: Yes
- **Notes**: Balance security (shorter expiration) with user experience (longer expiration)

#### CORS_ORIGINS
- **Description**: Allowed origins for Cross-Origin Resource Sharing (CORS)
- **Format**: Comma-separated list of URLs
- **Example**: `http://localhost:3000` (development)
- **Example**: `https://yourdomain.com,https://www.yourdomain.com` (production)
- **Required**: Yes
- **Security**: 
  - Only include trusted frontend domains
  - Never use `*` (wildcard) in production
  - Include protocol (http/https) and port if non-standard

### Optional Variables

#### ENVIRONMENT
- **Description**: Application environment mode
- **Format**: String
- **Default**: `development`
- **Allowed Values**: `development`, `staging`, `production`
- **Required**: No
- **Notes**: Affects logging verbosity and error detail exposure

#### HOST
- **Description**: Host address for the API server
- **Format**: IP address or hostname
- **Default**: `0.0.0.0` (all interfaces)
- **Example**: `127.0.0.1` (localhost only)
- **Required**: No

#### PORT
- **Description**: Port number for the API server
- **Format**: Integer (1-65535)
- **Default**: `8000`
- **Required**: No
- **Notes**: Ensure the port is not already in use

#### LOG_LEVEL
- **Description**: Logging verbosity level
- **Format**: String
- **Default**: `INFO`
- **Allowed Values**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Required**: No
- **Notes**: Use `DEBUG` for development, `INFO` or `WARNING` for production

## Frontend Environment Variables

### Required Variables

#### VITE_API_BASE_URL
- **Description**: Base URL for backend API requests
- **Format**: URL string (must include protocol and path)
- **Example**: `http://localhost:8000/api` (development)
- **Example**: `https://api.yourdomain.com/api` (production)
- **Required**: Yes
- **Notes**: 
  - Must include `/api` path suffix
  - For WSL1 development, use your machine's IP: `http://192.168.x.x:8000/api`
  - Ensure CORS is configured on backend to allow this origin

### Optional Variables

#### VITE_APP_ENV
- **Description**: Application environment identifier
- **Format**: String
- **Default**: `development`
- **Allowed Values**: `development`, `staging`, `production`
- **Required**: No
- **Notes**: Can be used for environment-specific feature flags

#### VITE_DEBUG
- **Description**: Enable debug mode for additional logging
- **Format**: Boolean string
- **Default**: `false`
- **Allowed Values**: `true`, `false`
- **Required**: No
- **Notes**: Should be `false` in production

## Setup Instructions

### Backend Setup

1. Copy the example file:
   ```bash
   cd backend
   cp .env.example .env
   ```

2. Edit `.env` and update the following:
   - `DATABASE_URL`: Update with your PostgreSQL credentials
   - `JWT_SECRET`: Generate a new secret key (see command above)
   - `CORS_ORIGINS`: Update with your frontend URL

3. Verify the configuration:
   ```bash
   python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('DATABASE_URL:', os.getenv('DATABASE_URL'))"
   ```

### Frontend Setup

1. Copy the example file:
   ```bash
   cd frontend
   cp .env.example .env
   ```

2. Edit `.env` and update:
   - `VITE_API_BASE_URL`: Update with your backend API URL

3. Restart the development server after changing environment variables

## Security Best Practices

1. **Never commit `.env` files** to version control
   - `.env` files are in `.gitignore` by default
   - Only commit `.env.example` files with placeholder values

2. **Use strong secrets in production**
   - Generate cryptographically secure random values
   - Rotate secrets periodically
   - Use different secrets for different environments

3. **Restrict CORS origins**
   - Only allow trusted domains
   - Never use wildcard (`*`) in production
   - Include specific protocols and ports

4. **Use HTTPS in production**
   - All production URLs should use `https://`
   - Configure SSL/TLS certificates properly
   - Enable HSTS (HTTP Strict Transport Security)

5. **Protect environment variables**
   - Use secret management services in production (AWS Secrets Manager, Azure Key Vault, etc.)
   - Limit access to environment variables
   - Audit access to sensitive configuration

## Troubleshooting

### Backend Issues

**Problem**: `DATABASE_URL` connection fails
- **Solution**: Verify PostgreSQL is running and credentials are correct
- **Check**: `psql -U nyaysetu_user -d nyaysetu -h localhost`

**Problem**: JWT tokens not working
- **Solution**: Ensure `JWT_SECRET` is set and hasn't changed
- **Check**: Verify the secret is at least 32 characters long

**Problem**: CORS errors in browser
- **Solution**: Verify `CORS_ORIGINS` includes the frontend URL with correct protocol and port
- **Check**: Browser console for specific CORS error messages

### Frontend Issues

**Problem**: API requests fail with network error
- **Solution**: Verify `VITE_API_BASE_URL` is correct and backend is running
- **Check**: Test the API URL directly in browser: `http://localhost:8000/api/docs`

**Problem**: Environment variables not updating
- **Solution**: Restart the Vite development server after changing `.env`
- **Note**: Vite only reads `.env` files at startup

**Problem**: WSL1 connection issues
- **Solution**: Use your Windows machine's IP address instead of `localhost`
- **Find IP**: Run `ipconfig` in Windows Command Prompt, look for IPv4 Address
