# Personal Data - Backend Project

This project focuses on handling personal data securely, including encryption of passwords, redacting PII (Personally Identifiable Information) from logs, and connecting securely to a MySQL database using environment variables.

## Requirements

- Python 3.7+
- Libraries: `mysql-connector-python`, `bcrypt`, `logging`
- Environment Variables:
  - `PERSONAL_DATA_DB_USERNAME`: The database username (default: `root`).
  - `PERSONAL_DATA_DB_PASSWORD`: The database password (default: empty string).
  - `PERSONAL_DATA_DB_HOST`: The database host (default: `localhost`).
  - `PERSONAL_DATA_DB_NAME`: The database name to connect to.

## Tasks

### 0. Regex-ing
- The `filter_datum` function takes a list of fields, a redaction string, a log message, and a separator. It uses regex to obfuscate sensitive fields in the log message.

### 1. Log formatter
- The `RedactingFormatter` class customizes the log formatting to redact PII fields from log messages.

### 2. Create logger
- The `get_logger` function configures a logger to log messages with redacted PII fields.

### 3. Connect to secure database
- The `get_db` function connects securely to a MySQL database using credentials stored in environment variables.

### 4. Read and filter data
- The `main` function retrieves data from the database and prints filtered logs.

### 5. Encrypting passwords
- The `hash_password` function hashes passwords securely using bcrypt.

### 6. Check valid password
- The `is_valid` function verifies if the provided password matches the hashed password.

## Running the Code

1. Set up your environment variables:
   ```bash
   export PERSONAL_DATA_DB_USERNAME=root
   export PERSONAL_DATA_DB_PASSWORD=root
   export PERSONAL_DATA_DB_HOST=localhost
   export PERSONAL_DATA_DB_NAME=my_db

