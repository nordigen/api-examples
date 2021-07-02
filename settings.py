"""Base settings used in models.py."""
import os

# Nordigen Base api URL
BASE_URL = 'https://ob.nordigen.com'

# Redirect URL (flask result route)
REDIRECT_URL = 'http://localhost:8081/results'

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
