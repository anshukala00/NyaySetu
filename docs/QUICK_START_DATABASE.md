# Quick Start: Database Setup

This guide will get your PostgreSQL database up and running in under 10 minutes.

## Prerequisites Checklist

- [ ] Windows 10 or 11
- [ ] Administrator access
- [ ] 1GB free disk space
- [ ] Internet connection

## Step-by-Step Setup

### 1. Install PostgreSQL (5 minutes)

1. **Download**: Visit https://www.postgresql.org/download/windows/
2. **Run installer** as Administrator
3. **Set password** for postgres user (remember this!)
4. **Keep defaults**: Port 5432, default locale
5. **Finish** installation

### 2. Initialize Database (2 minutes)

**Option A: Automated (Recommended)**

Open Command Prompt as Administrator and run:

```cmd
cd path\to\nyaysetu\backend\scripts
psql -U postgres -f init_db.sql
```

Enter your postgres password when prompted.

**Option B: Manual**

```cmd
psql -U postgres
```

Then run:

```sql
CREATE DATABASE nyaysetu;
CREATE USER nyaysetu_user WITH PASSWORD 'nyaysetu_pass';
GRANT ALL PRIVILEGES ON DATABASE nyaysetu TO nyaysetu_user;
\c nyaysetu
GRANT ALL ON SCHEMA public TO nyaysetu_user;
\q
```

### 3. Configure Backend (1 minute)

Edit `backend/.env`:

```env
DATABASE_URL=postgresql://nyaysetu_user:nyaysetu_pass@localhost:5432/nyaysetu
JWT_SECRET=your-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
CORS_ORIGINS=http://localhost:3000
```

### 4. Test Connection (1 minute)

```cmd
cd backend
python test_db_connection.py
```

You should see: ✅ Connection successful!

## Verification

Run these commands to verify everything is working:

```cmd
# Check PostgreSQL is running
psql -U postgres -c "SELECT version();"

# Check database exists
psql -U postgres -c "\l" | findstr nyaysetu

# Test user connection
psql -U nyaysetu_user -d nyaysetu -c "SELECT current_user;"
```

## What Was Created?

- ✅ Database: `nyaysetu`
- ✅ User: `nyaysetu_user` (password: `nyaysetu_pass`)
- ✅ Permissions: Full access to nyaysetu database
- ✅ Connection: Ready for SQLAlchemy

## Next Steps

Now that your database is ready:

1. **Install Python dependencies**:
   ```cmd
   cd backend
   pip install -r requirements.txt
   ```

2. **Run database migrations** (creates tables):
   ```cmd
   alembic upgrade head
   ```

3. **Start the backend server**:
   ```cmd
   uvicorn app.main:app --reload
   ```

4. **Test the API**: Open http://localhost:8000/docs

## Troubleshooting

### "psql: command not found"

Add to PATH: `C:\Program Files\PostgreSQL\15\bin`

1. Search "Environment Variables" in Windows
2. Edit "Path" in System Variables
3. Add the PostgreSQL bin directory
4. Restart Command Prompt

### "password authentication failed"

- Double-check your postgres password
- Verify user was created: `psql -U postgres -c "\du"`

### "database does not exist"

Run the init script again:
```cmd
psql -U postgres -f backend/scripts/init_db.sql
```

### Connection test fails

1. Check PostgreSQL service is running:
   - Open Services (services.msc)
   - Look for "postgresql-x64-15"
   - Ensure it's "Running"

2. Verify .env file has correct DATABASE_URL

3. Check firewall isn't blocking port 5432

## Security Reminder

⚠️ The default password `nyaysetu_pass` is for **development only**.

For production:
- Use strong, unique passwords
- Store in environment variables
- Never commit to Git
- Enable SSL connections

## Need More Help?

- Full guide: `docs/database-setup-windows.md`
- Scripts README: `backend/scripts/README.md`
- PostgreSQL docs: https://www.postgresql.org/docs/

## Summary

You've successfully:
- ✅ Installed PostgreSQL 15+
- ✅ Created the nyaysetu database
- ✅ Set up database user with permissions
- ✅ Configured backend connection
- ✅ Verified everything works

**Time to build! 🚀**
