#!/bin/bash

# Run the nail salon version
export BUSINESS_TYPE="nail"
export BUSINESS_NAME="You Nailed It Nail Salon"
export PROVIDER_TITLE="Nail Technician"
export PROVIDER_TITLE_PLURAL="Nail Technicians"
export DEBUG="True"

echo "💅 Starting Nail Salon App..."
echo "Visit: http://127.0.0.1:8000"
echo ""

source venv/bin/activate
python manage.py runserver
