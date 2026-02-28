# Farmbook (Django)

Mobile-first progressive web app style project for strawberry farm management.

## Features
- Issues module (diseases, pests, deficiencies) with image field and recommendations
- Plant protection and fertilizer catalog
- Irrigation log
- Spray log with tank mix items
- Django admin enabled
- SQLite database

## Data model
Implemented models:
- Crop
- Field
- Category
- Product
- Issue
- IssueRecommendation
- DosageRule
- IrrigationLog
- SprayLog
- SprayMixItem

Seed data migration adds:
- Crop: Strawberry
- Fields: Strawberry Greenhouse (22 sotka), Strawberry Open Field (40 sotka)
- Category groups: protection, fertilizer

## Setup
1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install django pillow
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Create admin user:
   ```bash
   python manage.py createsuperuser
   ```
5. Start server:
   ```bash
   python manage.py runserver
   ```

Open:
- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
