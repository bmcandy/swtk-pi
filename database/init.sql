-- SQL script to create a user and assign permissions using environment variables

-- Replace the placeholders with the actual values from the .env file
CREATE USER '${DB_USER}'@'%' IDENTIFIED BY '${DB_PASSWORD}';

-- Grant CREATE, UPDATE, and SELECT permissions on the database
GRANT CREATE, UPDATE, SELECT, INSERT ON ${DB_NAME}.* TO '${DB_USER}'@'%';

-- Apply the changes
FLUSH PRIVILEGES;