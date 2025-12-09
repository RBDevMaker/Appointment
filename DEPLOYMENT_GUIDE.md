# Dual Deployment Guide: Hairdresser & Nail Salon Apps

## Overview

Your codebase is now configured to support **both** a hairdresser app and a nail salon app using the same code. You'll deploy it twice on AWS Amplify with different environment variables.

## How It Works

The app uses environment variables to customize:
- Business name and branding
- Provider titles (Hairdresser vs Nail Technician)
- Service types
- Each deployment has its own database

## Deployment Steps

### 1. Push Code to Git

Make sure your code is in a Git repository (GitHub recommended for easy Amplify integration).

### 2. Deploy Hairdresser App

**In AWS Amplify Console:**

1. Create new app → "Host web app"
2. Connect your Git repository
3. Name it: `hairdresser-appointments`
4. Add environment variables:

```
SECRET_KEY=<generate-new-secret-key>
DEBUG=False
BUSINESS_TYPE=hairdresser
BUSINESS_NAME=Hair Salon Appointments
PROVIDER_TITLE=Hairdresser
PROVIDER_TITLE_PLURAL=Hairdressers
```

5. Deploy!

### 3. Deploy Nail Salon App

**In AWS Amplify Console:**

1. Create **another** new app → "Host web app"
2. Connect the **same** Git repository
3. Name it: `nail-salon-appointments`
4. Add environment variables:

```
SECRET_KEY=<generate-different-secret-key>
DEBUG=False
BUSINESS_TYPE=nail
BUSINESS_NAME=You Nailed It Nail Salon
PROVIDER_TITLE=Nail Technician
PROVIDER_TITLE_PLURAL=Nail Technicians
```

5. Deploy!

## Generate Secret Keys

Run this command twice to generate two different secret keys:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Customizing Services

After deployment, you'll need to populate each app with appropriate services:

**For Hairdresser App:**
- Access Django admin: `https://your-hairdresser-app.amplifyapp.com/admin`
- Add services: Haircut, Color, Highlights, etc.
- Add hairdressers

**For Nail Salon App:**
- Access Django admin: `https://your-nail-app.amplifyapp.com/admin`
- Add services: Manicure, Pedicure, Gel Nails, Acrylic, etc.
- Add nail technicians

## Database Setup

**Option 1: SQLite (Simple start)**
- Each deployment has its own SQLite database
- Data resets on redeployment
- Good for testing

**Option 2: Aurora Serverless v2 (Recommended)**
- Create **two separate** Aurora Serverless v2 databases
- Add these environment variables to each app:

```
DATABASE_HOST=<your-rds-endpoint>
DATABASE_USER=admin
DATABASE_PASSWORD=<your-password>
DATABASE_DB_NAME=appointments
```

## Cost Estimate

**Per App (you'll have 2):**
- Amplify hosting: $5-15/month
- Aurora Serverless v2 (optional): $10-30/month

**Total for both apps:** $10-90/month depending on database choice

## Managing Both Apps

**Same Codebase:**
- Both apps deploy from the same Git repo
- Push once, both apps update automatically
- Keep business logic consistent

**Separate Data:**
- Each app has its own database
- Different services and providers
- Independent bookings

## Admin Access

Create superuser for each app after first deployment:

```bash
# You'll need to do this via Amplify's SSM/console access or locally
python manage.py createsuperuser
```

## Next Steps

1. Deploy both apps on Amplify
2. Create admin users for each
3. Add services and providers via Django admin
4. Test booking flow on both
5. (Optional) Add custom domains for each app

## Troubleshooting

**If deployments fail:**
- Check build logs in Amplify Console
- Verify all environment variables are set
- Ensure SECRET_KEY is different for each app

**If you see wrong business name:**
- Check environment variables in Amplify Console
- Redeploy after updating variables
