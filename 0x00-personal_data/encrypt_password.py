#!/usr/bin/env python3
"""
Module for hashing and validating passwords using bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt and returns the salted hash.

    Args:
        password (str): The plain-text password to haash.

    Returns:
        bytes: The hashed password.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates a password against a hashed password.

    Args:
        hashed_password (bytes): The hashed password to checkk.
        password (str): The plain-text password to compare.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
