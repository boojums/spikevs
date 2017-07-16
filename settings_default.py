# Copy this file to settings.py and change the values there.

# Sesnder's email server and account
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "yourusername@gmail.com"

# Use the single-app password provide by google if using gmail
EMAIL_HOST_PASSWORD = 'yourpassword'

# Who to send the updates to
EMAIL_RECIPIENT = "spike@spikesemail.com"

# Set the desired log level
import logging
LOG_LEVEL =logging.INFO