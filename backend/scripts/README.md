# Database Scripts

This directory contains scripts for database initialization and management.

## Files

### `init_db.sql`
SQL script to initialize the PostgreSQL database for Nyaysetu.

**What it does:**
- Creates the `nyaysetu` database
- Creates the `nyaysetu_user` database user
- Grants all necessary permissions

**How to run:**
```cmd
psql -U postgres -f backend/scripts/init_db.sql
```

You'll be prompted for the postgres superuser password.

## Quick Setup Commands

### Windows Command Prompt

1. **Install PostgreSQL** (if not already installed):
   - Download from: https://www.postgresql.org/download/windows/
   - Follow the installation wizard
   - Remember the postgres superuser password

2. **Initialize the database**:
   ```cmd
   cd backend/scripts
   psql -U postgres -f init_db.sql
   ```

3. **Test the connection**:
   ```cmd
   cd ..
   python test_db_connection.py
   ```

### Manual Setup (Alternative)

If you prefer to run commands manually:

```sql
-- Connect as postgres superuser
psql -U postgres

-- Create database
CREATE DATABASE nyaysetu;

-- Create user
CREATE USER nyaysetu_user WITH PASSWORD 'nyaysetu_pass';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE nyaysetu TO nyaysetu_user;

-- Connect to database
\c nyaysetu

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO nyaysetu_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO nyaysetu_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO nyaysetu_user;

-- Exit
\q
```

## Connection Details

After setup, use these connection details:

- **Database**: nyaysetu
- **User**: nyaysetu_user
- **Password**: nyaysetu_pass (change in production!)
- **Host**: localhost
- **Port**: 5432

**Connection String**:
```
postgresql://nyaysetu_user:nyaysetu_pass@localhost:5432/nyaysetu
```

Add this to your `backend/.env` file:
```env
DATABASE_URL=postgresql://nyaysetu_user:nyaysetu_pass@localhost:5432/nyaysetu
```

## Security Notes

⚠️ **For Development Only**

The default password `nyaysetu_pass` is for development purposes only.

**For Production:**
- Use strong, unique passwords
- Store credentials in environment variables
- Never commit passwords to version control
- Enable SSL connections
- Restrict database access by IP

## Troubleshooting

### "psql: command not found"
Add PostgreSQL to your PATH:
- `C:\Program Files\PostgreSQL\15\bin`

### "password authentication failed"
- Verify the postgres password
- Check if the user was created: `\du` in psql

### "database does not exist"
- Run the init_db.sql script
- Or create manually: `CREATE DATABASE nyaysetu;`

### Permission errors
```sql
GRANT ALL ON SCHEMA public TO nyaysetu_user;
```

## Next Steps

After database setup:
1. ✅ Run migrations: `alembic upgrade head`
2. ✅ Start backend: `uvicorn app.main:app --reload`
3. ✅ Test API: http://localhost:8000/docs
