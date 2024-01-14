#!/usr/bin/env python3
import bcrypt


def hash_password(password):
    """ function that generate a random salt and hash the password"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


def is_valid(hashed_password, password):
    """Function that checks if the pass is valid"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
