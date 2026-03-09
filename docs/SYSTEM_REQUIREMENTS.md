# Nyaysetu - System Requirements

## Overview

This document outlines the system requirements for running the Nyaysetu Case Management System.

## Backend Requirements

### Software Requirements

- **Python**: 3.10 or higher
- **PostgreSQL**: 15 or higher
- **Operating System**: Windows 10/11, Linux, or macOS

### Python Dependencies

All dependencies are listed in `backend/requirements.txt`:

- FastAPI 0.104.1
- Uvicorn 0.24.0
- SQLAlchemy 2.0.23
- Alembic 1.12.1
- Psycopg2-binary 2.9.9
- PyJWT 2.8.0
- Bcrypt 4.1.1
- Python-dotenv 1.0.0
- Pydantic 2.5.0
- Pydantic[email] 2.5.0
- Pytest 7.4.3
- Hypothesis 6.92.1

### Hardware Requirements (Minimum)

- **CPU**: 2 cores
- **RAM**: 4 GB
- **Storage**: 10 GB free space
- **Network**: Stable internet connection

### Hardware Requirements (Recommended)

- **CPU**: 4+ cores
- **RAM**: 8 GB
- **Storage**: 20 GB free space (SSD preferred)
- **Network**: High-speed internet connection

## Frontend Requirements

### Software Requirements

- **Node.js**: 18.0 or higher
- **npm**: 9.0 or higher
- **Modern Web Browser**:
  - Chrome 90+
  - Firefox 88+
  - Safari 14+
  - Edge 90+

### Node Dependencies

All dependencies are listed in `frontend/package.json`:

- React 18.2.0
- React Router DOM 6.20.0
- Axios 1.6.2
- Zustand 4.4.7
- React Hook Form 7.48.2
- Tailwind CSS 3.3.5
- Lucide React 0.294.0
- Vitest 1.0.4
- React Testing Library 14.1.2

### Browser Requirements

- **JavaScript**: Must be enabled
- **Cookies**: Must be enabled for authentication
- **LocalStorage**: Must be enabled for session persistence
- **Screen Resolution**: Minimum 1024x768 (responsive design supports mobile)

## Database Requirements

### PostgreSQL Configuration

- **Version**: PostgreSQL 15 or higher
- **Database**: nyaysetu
- **User**: nyaysetu_user (or custom)
- **Encoding**: UTF-8
- **Timezone**: UTC

### Database Resources

- **Storage**: Minimum 1 GB for MVP
- **Connections**: Pool size of 5, max overflow of 10
- **Memory**: Minimum 512 MB allocated to PostgreSQL

## Network Requirements

### Ports

- **Backend API**: 8000 (default, configurable)
- **Frontend Dev Server**: 3000 (default, configurable)
- **PostgreSQL**: 5432 (default)

### Firewall Rules

Ensure the following ports are open:
- Port 8000 for backend API
- Port 3000 for frontend (development)
- Port 5432 for PostgreSQL (if remote)

## Development Environment

### Required Tools

- **Code Editor**: VS Code, PyCharm, or similar
- **Terminal**: PowerShell (Windows), Bash (Linux/Mac)
- **Git**: For version control
- **Postman/Insomnia**: For API testing (optional)

### Optional Tools

- **pgAdmin**: PostgreSQL GUI management tool
- **Docker**: For containerized deployment
- **WSL**: Windows Subsystem for Linux (for Windows users)

## Production Environment (Future)

### Recommended Specifications

- **CPU**: 8+ cores
- **RAM**: 16 GB
- **Storage**: 100 GB SSD
- **Database**: Managed PostgreSQL service (AWS RDS, Azure Database, etc.)
- **Load Balancer**: For high availability
- **CDN**: For static asset delivery
- **SSL Certificate**: For HTTPS

### Scalability Targets

- **Concurrent Users**: 1000+
- **API Response Time**: <200ms (p95)
- **Database Connections**: 50+ concurrent
- **Storage Growth**: Plan for 10 GB/month

## Performance Benchmarks

### Expected Performance (MVP)

- **Login**: <500ms
- **Case Creation**: <1s
- **Case List Load**: <1s
- **AI Triage**: <2s
- **AI Summary**: <3s
- **Precedent Search**: <2s

### Database Performance

- **Query Response**: <100ms for indexed queries
- **Connection Pool**: 5 connections, max 10 overflow
- **Connection Timeout**: 30 seconds

## Browser Compatibility

### Fully Supported

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Partially Supported

- Older browsers may have limited functionality
- Mobile browsers (iOS Safari, Chrome Mobile)

### Not Supported

- Internet Explorer (all versions)
- Browsers with JavaScript disabled

## Accessibility

- **WCAG 2.1**: Targeting Level AA compliance
- **Screen Readers**: Compatible with NVDA, JAWS, VoiceOver
- **Keyboard Navigation**: Full keyboard support
- **Color Contrast**: Meets WCAG AA standards

## Security Requirements

### Authentication

- JWT tokens with 24-hour expiration
- Bcrypt password hashing (cost factor 12)
- Secure session management

### Network Security

- HTTPS required in production
- CORS configured for allowed origins
- SQL injection prevention via parameterized queries

### Data Protection

- Password minimum length: 8 characters
- Email validation
- Input sanitization
- Role-based access control

## Monitoring and Logging

### Application Logs

- FastAPI access logs
- Error logs with stack traces
- Database query logs (optional, for debugging)

### Health Checks

- `/health` endpoint for monitoring
- Database connection verification
- API availability checks

## Backup Requirements

### Database Backups

- **Frequency**: Daily (minimum)
- **Retention**: 30 days (minimum)
- **Type**: Full database backup
- **Storage**: Off-site or cloud storage

### Configuration Backups

- Environment variables
- Database connection strings
- JWT secrets

## Upgrade Path

### Version Updates

- **Python**: Follow semantic versioning
- **Node.js**: LTS versions recommended
- **PostgreSQL**: Minor version updates safe
- **Dependencies**: Regular security updates

### Migration Strategy

- Test migrations in staging environment
- Backup database before migrations
- Use Alembic for database schema changes
- Document breaking changes

---

**Last Updated**: March 2026
**Version**: 1.0.0 (MVP)
