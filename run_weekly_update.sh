#!/bin/bash
# This script runs daily at 17:00 UTC on PythonAnywhere.
# It checks if the current UTC day is Sunday (day 7), which corresponds to Monday GMT+7.

if [ $(date -u +%u) -eq 7 ]; then
    # IMPORTANT: Replace "your_username" with your actual PythonAnywhere username!
    # And replace "your_virtualenv" with the name of your virtual environment folder if you have one.
    
    cd /home/syndoria/EloServer
    
    # If using a virtual environment, uncomment the line below and change the path:
    # source /home/your_username/.virtualenvs/your_virtualenv/bin/activate
    
    python manage.py update_weekly_ranking
    
    echo "Weekly ranking updated!"
else
    echo "Not Sunday UTC (Monday GMT+7) yet, skipping."
fi
