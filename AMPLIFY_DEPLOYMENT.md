# AWS Amplify Deployment Guide

## What I've Set Up

Your Django app is now ready for AWS Amplify deployment with:

1. **amplify.yml** - Build configuration for Amplify
2. **Updated settings.py** - Environment-based configuration
3. **WhiteNoise** - For serving static files efficiently
4. **Gunicorn** - Production WSGI server

## Deployment Steps

### 1. Push to Git Repository
Make sure your code is in a Git repository (GitHub, GitLab, Bitbucket, or AWS CodeCommit).

### 2. Create Amplify App

Go to AWS Amplify Console:
```
https://console.aws.amazon.com/amplify/
```

1. Click "New app" → "Host web app"
2. Connect your Git repository
3. Select your branch
4. Amplify will auto-detect the `amplify.yml` file

### 3. Configure Environment Variables

In Amplify Console, add these environment variables:

**Required:**
- `SECRET_KEY` - Generate a new one: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- `DEBUG` - Set to `False` for production

**Optional (for MySQL/RDS):**
- `DATABASE_HOST` - Your RDS endpoint
- `DATABASE_USER` - Database username
- `DATABASE_PASSWORD` - Database password
- `DATABASE_DB_NAME` - Database name

**Note:** If you don't set database variables, it will use SQLite (stored in the container, resets on redeploy).

### 4. Deploy

Click "Save and deploy" - Amplify will:
- Install dependencies
- Collect static files
- Run migrations
- Deploy your app

## Database Options

### Option 1: SQLite (Simple, but resets on redeploy)
- No additional setup needed
- Good for testing
- Data is lost on each deployment

### Option 2: Amazon RDS MySQL (Recommended for production)
1. Create an RDS MySQL instance
2. Add the environment variables above
3. Ensure Amplify can access RDS (security groups)

### Option 3: Amazon RDS with IAM Authentication
- Don't set `DATABASE_PASSWORD`
- Configure IAM role for Amplify
- More secure, no password needed

## Cost Estimate

Amplify pricing is much cheaper than EKS:
- **Build minutes:** ~$0.01/minute (only during deployments)
- **Hosting:** ~$0.15/GB served + $0.023/GB stored
- **Typical small app:** $5-15/month

Plus RDS if you use it:
- **db.t3.micro:** ~$15/month
- **db.t4g.micro:** ~$12/month

## Post-Deployment

After deployment, Amplify gives you:
- A `.amplifyapp.com` URL
- Automatic HTTPS
- CI/CD on every git push
- Easy rollbacks

## Troubleshooting

If deployment fails:
1. Check build logs in Amplify Console
2. Verify environment variables are set
3. Make sure `ALLOWED_HOSTS` includes your Amplify domain
4. Check that migrations run successfully

## Custom Domain

To add your own domain:
1. Go to "Domain management" in Amplify Console
2. Add your domain
3. Follow DNS configuration steps
