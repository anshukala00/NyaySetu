# PostgreSQL Database Setup Guide for Windows

This guide provides step-by-step instructions for installing PostgreSQL 15+ and setting up the Nyaysetu database on Windows.

## Prerequisites

- Windows 10 or Windows 11
- Administrator access to your computer
- At least 1GB of free disk space

## Step 1: Download PostgreSQL

1. Visit the official PostgreSQL download page: https://www.postgresql.org/download/windows/
2. Click on "Download the installer" link (this will take you to EnterpriseDB)
3. Download the latest PostgreSQL 15.x or 16.x installer for Windows (64-bit recommended)
   - File name will be something like: `postgresql-15.x-windows-x64.exe`

## Step 2: Install PostgreSQL

1. **Run the installer** as Administrator (right-click → "Run as administrator")

2. **Installation wizard steps:**
   - Click "Next" on the welcome screen
   - **Installation Directory**: Keep the default path (e.g., `C:\Program Files\PostgreSQL\15`)
   - **Select Components**: Ensure these are checked:
     - ✅ PostgreSQL Server
     - ✅ pgAdmin 4 (GUI management tool)
     - ✅ Command Line Tools
     - ✅ Stack Builder (optional)
   - Click "Next"

3. **Data Directory**: Keep the default (e.g., `C:\Program Files\PostgreSQL\15\data`)

4. **Set Password**:
   - Enter a strong password for the PostgreSQL superuser (postgres)
   - **IMPORTANT**: Remember this password! You'll need it later
   - Example: `postgres123` (use a stronger password in production)
   - Confirm the password

5. **Port**: Keep the default port `5432` (unless you have a conflict)

6. **Locale**: Select "Default locale" or your preferred locale

7. Click "Next" and then "Next" again to begin installation

8. Wait for the installation to complete (this may take a few minutes)

9. **Uncheck "Launch Stack Builder"** at the end (not needed for this project)

10. Click "Finish"

## Step 3: Verify Installation

1. **Open Command Prompt** (Win + R, type `cmd`, press Enter)

2. **Test PostgreSQL installation**:
   ```cmd
   psql --version
   ```
   You should see output like: `psql (PostgreSQL) 15.x`

   If you get an error, you may need to add PostgreSQL to your PATH:
   - Search for "Environment Variables" in Windows
   - Edit "Path" in System Variables
   - Add: `C:\Program Files\PostgreSQL\15\bin`
   - Restart Command Prompt

## Step 4: Create Nyaysetu Database

### Option A: Using pgAdmin 4 (GUI Method)

1. **Launch pgAdmin 4** from Start Menu

2. **Connect to PostgreSQL**:
   - Expand "Servers" in the left panel
   - Click on "PostgreSQL 15" (or your version)
   - Enter the password you set during installation

3. **Create Database**:
   - Right-click on "Databases"
   - Select "Create" → "Database..."
   - Enter database name: `nyaysetu`
   - Click "Save"

4. **Create Database User**:
   - Right-click on "Login/Group Roles"
   - Select "Create" → "Login/Group Role..."
   - In "General" tab, enter name: `nyaysetu_user`
   - In "Definition" tab, enter password: `nyaysetu_pass` (or your preferred password)
   - In "Privileges" tab, check:
     - ✅ Can login?
   - Click "Save"

5. **Grant Permissions**:
   - Right-click on the `nyaysetu` database
   - Select "Query Tool"
   - Run the following SQL:
   ```sql
   GRANT ALL PRIVILEGES ON DATABASE nyaysetu TO nyaysetu_user;
   GRANT ALL ON SCHEMA public TO nyaysetu_user;
   ```

### Option B: Using Command Line (Recommended for Automation)

1. **Open Command Prompt as Administrator**

2. **Connect to PostgreSQL**:
   ```cmd
   psql -U postgres
   ```
   Enter the password you set during installation

3. **Run the initialization script**:
   ```cmd
   psql -U postgres -f backend/scripts/init_db.sql
   ```

   Or manually execute these commands:
   ```sql
   -- Create database
   CREATE DATABASE nyaysetu;

   -- Create user
   CREATE USER nyaysetu_user WITH PASSWORD 'nyaysetu_pass';

   -- Grant privileges
   GRANT ALL PRIVILEGES ON DATABASE nyaysetu TO nyaysetu_user;

   -- Connect to the database
   \c nyaysetu

   -- Grant schema privileges
   GRANT ALL ON SCHEMA public TO nyaysetu_user;
   GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO nyaysetu_user;
   GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO nyaysetu_user;

   -- Exit
   \q
   ```

## Step 5: Verify Database Setup

1. **Test connection with the new user**:
   ```cmd
   psql -U nyaysetu_user -d nyaysetu -h localhost
   ```
   Enter password: `nyaysetu_pass`

2. **You should see the PostgreSQL prompt**:
   ```
   nyaysetu=>
   ```

3. **List databases** to confirm:
   ```sql
   \l
   ```
   You should see `nyaysetu` in the list

4. **Exit**:
   ```sql
   \q
   ```

## Step 6: Configure Backend Connection

1. **Navigate to the backend directory**:
   ```cmd
   cd backend
   ```

2. **Update the `.env` file** with your database credentials:
   ```env
   DATABASE_URL=postgresql://nyaysetu_user:nyaysetu_pass@localhost:5432/nyaysetu
   JWT_SECRET=your-secret-key-here-change-in-production
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION_HOURS=24
   CORS_ORIGINS=http://localhost:3000
   ```

3. **Test the connection** using the provided test script:
   ```cmd
   python test_db_connection.py
   ```

## Troubleshooting

### Issue: "psql: command not found"

**Solution**: Add PostgreSQL to your PATH:
1. Open System Properties → Environment Variables
2. Edit "Path" variable
3. Add: `C:\Program Files\PostgreSQL\15\bin`
4. Restart Command Prompt

### Issue: "password authentication failed"

**Solution**: 
- Verify you're using the correct password
- Check if the user was created successfully
- Try resetting the password:
  ```sql
  ALTER USER nyaysetu_user WITH PASSWORD 'new_password';
  ```

### Issue: "database does not exist"

**Solution**: Create the database manually:
```sql
psql -U postgres
CREATE DATABASE nyaysetu;
\q
```

### Issue: "permission denied for schema public"

**Solution**: Grant schema permissions:
```sql
psql -U postgres -d nyaysetu
GRANT ALL ON SCHEMA public TO nyaysetu_user;
\q
```

### Issue: Port 5432 already in use

**Solution**: 
- Check if another PostgreSQL instance is running
- Or change the port during installation and update your connection string

## Security Notes

⚠️ **Important for Production**:
- Change default passwords to strong, unique passwords
- Use environment variables for sensitive data (never commit passwords to Git)
- Consider using connection pooling for better performance
- Enable SSL connections in production
- Restrict database access to specific IP addresses

## Next Steps

After completing the database setup:
1. ✅ PostgreSQL is installed and running
2. ✅ `nyaysetu` database is created
3. ✅ `nyaysetu_user` has appropriate permissions
4. ✅ Backend `.env` file is configured

You can now proceed to:
- Run database migrations: `alembic upgrade head`
- Start the FastAPI backend: `uvicorn app.main:app --reload`

## Additional Resources

- PostgreSQL Documentation: https://www.postgresql.org/docs/
- pgAdmin Documentation: https://www.pgadmin.org/docs/
- FastAPI + PostgreSQL Guide: https://fastapi.tiangolo.com/tutorial/sql-databases/