# gunicorn_config.py

# Bind to all interfaces on port 8000
bind = '0.0.0.0:5000'

# Use 2 workers for handling requests (adjust based on your server's CPU count)
workers = 2

# Set the logging level
loglevel = 'info'

# Set the application name for easier identification
proc_name = 'flask_app'
