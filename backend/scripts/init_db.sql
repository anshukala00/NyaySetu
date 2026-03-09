-- Nyaysetu Database Initialization Script
-- This script creates the database, user, and grants necessary permissions
-- Run this script as the postgres superuser

-- Create the database
CREATE DATABASE nyaysetu
    WITH 
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TEMPLATE = template0;

-- Create the application user
CREATE USER nyaysetu_user WITH PASSWORD 'nyaysetu_pass';

-- Grant database-level privileges
GRANT ALL PRIVILEGES ON DATABASE nyaysetu TO nyaysetu_user;

-- Connect to the nyaysetu database
\c nyaysetu

-- Grant schema-level privileges
GRANT ALL ON SCHEMA public TO nyaysetu_user;

-- Grant privileges on all current and future tables
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO nyaysetu_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO nyaysetu_user;

-- Grant default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO nyaysetu_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO nyaysetu_user;

-- Display success message
\echo 'Database setup completed successfully!'
\echo 'Database: nyaysetu'
\echo 'User: nyaysetu_user'
\echo 'Connection string: postgresql://nyaysetu_user:nyaysetu_pass@localhost:5432/nyaysetu'
