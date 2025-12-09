#!/bin/bash

# Run the hairdresser version
export BUSINESS_TYPE="hairdresser"
export BUSINESS_NAME="Luxe Hair Studio"
export PROVIDER_TITLE="Hairdresser"
export PROVIDER_TITLE_PLURAL="Hairdressers"
export DEBUG="True"

echo "🎨 Starting Hairdresser App..."
echo "Visit: http://127.0.0.1:8000"
echo ""

source venv/bin/activate
python manage.py runserver
