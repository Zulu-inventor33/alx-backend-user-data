#!/usr/bin/env python3
"""
Moduile for filtering logs, formatting log entries, and connecting to a secure database.
"""

import logging
import re
import os
import mysql.connector
from bcrypt import hashpw, gensalt
from typing import List, Tuple


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates specific fields in a log message using regular expressions.

    Args:
        fields (List[str]): List of field names to obfuscate.
        redaction (str): The string to replace field values with.
        message (str): The log message to filter.
        separator (str): The separator between fields in the message.

    Returns:
        str: The filtered log message with obfuscated fields.
    """
    for field in fields:
        message = re.sub(
            rf"({field}=[^;]+)",
            rf"\1{separator}{redaction}",
            message
        )
    return message


class RedactingFormatter(logging.Formatter):
    """
    Formatta that redacts PII fields in log messages.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Tuple[str, ...]) -> None:
        """
        Initializes the RedactingFormatter with the fields to be redacted.

        Args:
            fields (Tuple[str, ...]): The fields to be redacted in the log message.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record, redacting specified fields.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message with redacted fields.
        """
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)


PII_FIELDS: Tuple[str, ...] = (
    "email", "ssn", "password", "name", "phone"
)


def get_logger() -> logging.Logger:
    """
    Creates and returns a logger configured with RedactingFormatter.

    Returns:
        logging.Logger: A logger with a RedactingFormatter.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establishes a connection to the MySQL database using environment variables.

    Returns:
        mysql.connector.connection.MySQLConnection:
        The MySQL connection object.
    """
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )
    return connection
