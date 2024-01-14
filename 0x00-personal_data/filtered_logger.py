#!/usr/bin/env python3

import logging
import re
import user_data.csv
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")
def filter_datum(fields, redaction, message, separator):
      """function that returns log message obfuscated"""
      return re.sub(r'(\b(?:' + '|'.join(fields) + r')' + re.escape(separator) + ')[^' + re.escape(separator) + r']+', r'\1' + redaction, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """our constructor"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """method that filters the incoming log records"""
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super().format(record)
    
def get_logger():
       """function that takes no arguments and returns a logger object"""
       logger = logging.getLogger(user_data.csv)
       logger.setLevel(logging.INFO)

       formatter = RedactingFormatter(fields=PII_FIELDS)

       stream_handler = logging.StreamHandler()
       stream_handler.setLevel(logging.INFO)
       stream_handler.setFormatter(formatter)

       logger.addHandler(stream_handler)
       logger.propagate = False

       return logger


def get_db():
       """Function that returns connector to a db"""
       username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
       password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
       host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
       database = os.getenv("PERSONAL_DATA_DB_NAME", "")

       connection = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=database
    )

       return connection
    
def main():
       """main function that takes no arguments andreturns nothing"""
       db = get_db()
       cursor = db.cursor(dictionary=True)

       formatter = RedactingFormatter(fields=PII_FIELDS)
       logger = logging.getLogger("user_data")
       logger.setLevel(logging.INFO)

       stream_handler = logging.StreamHandler()
       stream_handler.setLevel(logging.INFO)
       stream_handler.setFormatter(formatter)

       logger.addHandler(stream_handler)
       logger.propagate = False

       cursor.execute("SELECT * FROM users;")
       for row in cursor:
           formatted_row = "; ".join([f"{key}={row[key]}" for key in row])
           logger.info(formatted_row)

       cursor.close()
       db.close()


if __name__ == "__main__":
    
    message = "name=Bob;email=bob@dylan.com;ssn=000-123-0000;password=bobby2019;"
    log_record = logging.LogRecord("my_logger", logging.INFO, None, None, message, None, None)
    formatter = RedactingFormatter(fields=("email", "ssn", "password"))
    print(formatter.format(log_record))

    logger = get_logger()
    logger.info("This is a test log message with PII: name=John;email=john@example.com;phone=123-456-7890;ssn=123-45-6789;password=secret")

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM users;")

    for row in cursor:
        print(row[0])

    cursor.close()
    db.close()

    main()


    