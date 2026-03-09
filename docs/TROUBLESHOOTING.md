# Nyaysetu - Troubleshooting Guide

This guide helps you resolve common issues with the Nyaysetu Case Management System.

## Table of Contents

1. [Backend Issues](#backend-issues)
2. [Frontend Issues](#frontend-issues)
3. [Database Issues](#database-issues)
4. [Authentication Issues](#authentication-issues)
5. [API Issues](#api-issues)
6. [Performance Issues](#performance-issues)

---

## Backend Issues

### Backend Won't Start

**Symptom**: `uvicorn app.main:app --reload` fails

**Solutions**:

1. **Check Python version**:
   ```bash
   python --version  # Should be 3.10+
   ```

2. **Verify virtual environment is activated**:
   ```bash
   # Windows
   .\venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Check .env file exists**:
   ```bash
   # Copy from example if missing
   copy .env.example .env
   ```

### Import Errors

**Symptom**: `ModuleNotFoundError` or `ImportError`

**Solutions**:

1. Ensure virtual environment is activated
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check Python path: `which python` (should point to venv)

### Port Already in Use

**Symptom**: `Address already in use` error on port 8000

**Solutions**:

1. **Find process using port**:
   ```bash
   # Windows
   netstat -ano | findstr :8000
   
   # Linux/Mac
   lsof -i :8000
   ```

2. **Kill the process** or use a different port:
   ```bash
   uvicorn app.main:app --reload --port 8001
   ```

---

## Frontend Issues

### Frontend Won't Start

**Symptom**: `npm run dev` fails

**Solutions**:

1. **Check Node.js version**:
   ```bash
   node --version  # Should be 18+
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Clear cache and reinstall**:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **Check .env file**:
   ```bash
   # Should contain:
   VITE_API_BASE_URL=http://localhost:8000/api
   ```

### Build Errors

**Symptom**: TypeScript errors during build

**Solutions**:

1. **Check TypeScript version**: `npx tsc --version`
2. **Clear TypeScript cache**: `rm -rf node_modules/.vite`
3. **Rebuild**: `npm run build`

### Page Not Loading

**Symptom**: Blank page or "Cannot GET /" error

**Solutions**:

1. Check browser console for errors (F12)
2. Verify dev server is running on port 3000
3. Clear browser cache (Ctrl+Shift+Delete)
4. Try incognito/private mode

---

## Database Issues

### Cannot Connect to Database

**Symptom**: `could not connect to server` or `connection refused`

**Solutions**:

1. **Check PostgreSQL is running**:
   ```bash
   # Windows
   Get-Service postgresql*
   
   # Linux
   sudo systemctl status postgresql
   ```

2. **Start PostgreSQL**:
   ```bash
   # Windows
   Start-Service postgresql-x64-17
   
   # Linux
   sudo systemctl start postgresql
   ```

3. **Verify DATABASE_URL in .env**:
   ```
   DATABASE_URL=postgresql://nyaysetu_user:nyaysetu_pass@localhost:5432/nyaysetu
   ```

4. **Test connection**:
   ```bash
   python test_db_connection.py
   ```

### Database Does Not Exist

**Symptom**: `database "nyaysetu" does not exist`

**Solutions**:

1. **Run database setup script**:
   ```bash
   cd backend/scripts
   ./setup_database.bat  # Windows
   ```

2. **Or create manually**:
   ```bash
   psql -U postgres -f scripts/init_db.sql
   ```

### Migration Errors

**Symptom**: Alembic migration fails

**Solutions**:

1. **Check current migration**:
   ```bash
   alembic current
   ```

2. **Rollback and retry**:
   ```bash
   alembic downgrade -1
   alembic upgrade head
   ```

3. **Reset database** (development only):
   ```bash
   alembic downgrade base
   alembic upgrade head
   ```

### Tables Not Found

**Symptom**: `relation "users" does not exist`

**Solutions**:

1. **Run migrations**:
   ```bash
   alembic upgrade head
   ```

2. **Verify migration status**:
   ```bash
   alembic current  # Should show: 32710815cf6d (head)
   ```

---

## Authentication Issues

### Cannot Login

**Symptom**: "Invalid credentials" error

**Solutions**:

1. **Verify email and password are correct**
2. **Check user exists in database**:
   ```python
   from app.database import SessionLocal
   from models.user import User
   db = SessionLocal()
   user = db.query(User).filter(User.email == "your@email.com").first()
   print(user)
   ```

3. **Reset password** (contact admin)

### Token Expired

**Symptom**: Redirected to login unexpectedly

**Solutions**:

1. **Login again** (tokens expire after 24 hours)
2. **Check JWT_EXPIRATION_HOURS in .env**
3. **Clear browser localStorage and login again**

### Unauthorized Access

**Symptom**: 403 Forbidden error

**Solutions**:

1. **Verify your role** (citizen vs judge)
2. **Check you're accessing the correct portal**
3. **Ensure token is valid** (try logging out and back in)

### Session Lost on Refresh

**Symptom**: Logged out when refreshing page

**Solutions**:

1. **Check browser allows localStorage**
2. **Disable browser extensions** that block storage
3. **Try incognito mode** to test
4. **Verify initializeAuth is called** in App.tsx

---

## API Issues

### CORS Errors

**Symptom**: "CORS policy" error in browser console

**Solutions**:

1. **Check CORS_ORIGINS in backend .env**:
   ```
   CORS_ORIGINS=http://localhost:3000
   ```

2. **Verify frontend URL matches**:
   ```
   VITE_API_BASE_URL=http://localhost:8000/api
   ```

3. **Restart backend** after changing CORS settings

### 404 Not Found

**Symptom**: API endpoint returns 404

**Solutions**:

1. **Check API base URL** in frontend .env
2. **Verify endpoint path** (should start with /api)
3. **Check backend logs** for routing errors
4. **Visit** http://localhost:8000/docs to see available endpoints

### 500 Internal Server Error

**Symptom**: API returns 500 error

**Solutions**:

1. **Check backend logs** for stack trace
2. **Verify database connection**
3. **Check all required fields** are provided
4. **Restart backend server**

### Network Timeout

**Symptom**: Request times out

**Solutions**:

1. **Check backend is running**: Visit http://localhost:8000/health
2. **Verify firewall settings**
3. **Check network connection**
4. **Increase timeout** in API client if needed

---

## Performance Issues

### Slow API Responses

**Symptom**: Requests take >5 seconds

**Solutions**:

1. **Check database indexes**:
   ```sql
   SELECT * FROM pg_indexes WHERE tablename IN ('users', 'cases');
   ```

2. **Monitor database connections**:
   ```python
   # Check pool status
   from app.database import engine
   print(engine.pool.status())
   ```

3. **Optimize queries** (add indexes if needed)
4. **Increase connection pool size** in database.py

### High Memory Usage

**Symptom**: System running out of memory

**Solutions**:

1. **Reduce pagination limit** (default: 10 items)
2. **Close unused database connections**
3. **Restart backend server**
4. **Check for memory leaks** in long-running processes

### Slow Frontend Loading

**Symptom**: Pages take long to load

**Solutions**:

1. **Clear browser cache**
2. **Check network tab** in DevTools for slow requests
3. **Optimize bundle size**: `npm run build` and check dist/ size
4. **Disable browser extensions**

---

## Common Error Messages

### "DATABASE_URL environment variable is not set"

**Solution**: Create `.env` file in backend/ with DATABASE_URL

### "JWT_SECRET environment variable is not set"

**Solution**: Add JWT_SECRET to backend/.env file

### "Cannot access 'X' before initialization"

**Solution**: Check for circular imports or hoisting issues in tests

### "Role 'nyaysetu_user' does not exist"

**Solution**: Run database setup script: `./scripts/setup_database.bat`

### "Permission denied for table X"

**Solution**: Grant permissions to nyaysetu_user:
```sql
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO nyaysetu_user;
```

---

## Testing Issues

### Tests Failing

**Symptom**: pytest or vitest tests fail

**Solutions**:

1. **Backend tests**:
   ```bash
   # Ensure test database exists
   pytest -v
   ```

2. **Frontend tests**:
   ```bash
   # Using WSL
   npm run test:run
   ```

3. **Check test database** is separate from development database
4. **Clear test cache**: `rm -rf .pytest_cache` or `rm -rf node_modules/.vitest`

### Mock Initialization Errors

**Symptom**: "Cannot access before initialization" in vitest

**Solution**: Use `vi.hoisted()` for mock functions:
```typescript
const mockFn = vi.hoisted(() => vi.fn())
vi.mock('module', () => ({ fn: mockFn }))
```

---

## Getting Help

### Check Logs

1. **Backend logs**: Terminal where uvicorn is running
2. **Frontend logs**: Browser console (F12)
3. **Database logs**: PostgreSQL log files

### Debug Mode

1. **Backend**: Set `echo=True` in database.py for SQL logging
2. **Frontend**: Check Network tab in DevTools

### Contact Support

If issues persist:
- Email: support@nyaysetu.com
- Include: Error message, steps to reproduce, system info

---

## Quick Fixes Checklist

Before seeking help, try these:

- [ ] Restart backend server
- [ ] Restart frontend dev server
- [ ] Restart PostgreSQL service
- [ ] Clear browser cache and localStorage
- [ ] Check all .env files are configured
- [ ] Verify all services are running
- [ ] Check firewall/antivirus settings
- [ ] Review recent code changes
- [ ] Check database migrations are up to date
- [ ] Verify network connectivity

---

**Last Updated**: March 2026
**Version**: 1.0.0 (MVP)
