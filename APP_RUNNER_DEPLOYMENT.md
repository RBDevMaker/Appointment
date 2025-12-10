# AWS App Runner Deployment Guide

## Overview
AWS App Runner is a fully managed service that makes it easy to deploy containerized web applications and APIs. It's perfect for Django apps and much simpler than Fargate.

## Cost Estimate
- **App Runner**: ~$7-12/month (0.25 vCPU, 0.5 GB memory)
- **Much cheaper than Fargate** (no ALB needed)

## Prerequisites
- AWS Account
- GitHub repository with your code
- AWS CLI (optional, for command line deployment)

## Deployment Steps

### Option 1: AWS Console (Recommended)

1. **Go to AWS App Runner Console**
   - Navigate to: https://console.aws.amazon.com/apprunner/
   - Click "Create service"

2. **Configure Source**
   - Source type: "Source code repository"
   - Repository type: "GitHub"
   - Connect to your GitHub account
   - Select your repository
   - Branch: "main" (or your default branch)
   - Deployment trigger: "Automatic" (deploys on every push)

3. **Configure Build**
   - Configuration file: "Use a configuration file"
   - Configuration file name: `apprunner.yaml`

4. **Configure Service**
   - Service name: `luxe-hair-studio`
   - Virtual CPU: 0.25 vCPU
   - Memory: 0.5 GB
   - Environment variables (add these):
     ```
     SECRET_KEY = h070k21hg)+r+#5tdv1$73+=&jdxz&qxqh_8%tz6-*@6p)buh9
     DEBUG = False
     BUSINESS_TYPE = hairdresser
     BUSINESS_NAME = Luxe Hair Studio
     PROVIDER_TITLE = Hairdresser
     PROVIDER_TITLE_PLURAL = Hairdressers
     PRIMARY_COLOR = #f5a3b8
     SECONDARY_COLOR = #d4af37
     ACCENT_COLOR = #fce4ec
     BACKGROUND_COLOR = #f0e6d8
     ```

5. **Configure Security (Optional)**
   - Auto-scaling: Default settings are fine
   - Health check: Default settings are fine

6. **Review and Create**
   - Review all settings
   - Click "Create & deploy"

### Option 2: AWS CLI

```bash
# Create apprunner.yaml (already done)
# Push to GitHub
git add .
git commit -m "Add App Runner configuration"
git push origin main

# Create App Runner service
aws apprunner create-service \
  --service-name luxe-hair-studio \
  --source-configuration '{
    "ImageRepository": {
      "ImageIdentifier": "public.ecr.aws/docker/library/python:3.11-slim",
      "ImageConfiguration": {
        "Port": "8000"
      },
      "ImageRepositoryType": "ECR_PUBLIC"
    },
    "CodeRepository": {
      "RepositoryUrl": "https://github.com/YOUR_USERNAME/YOUR_REPO",
      "SourceCodeVersion": {
        "Type": "BRANCH",
        "Value": "main"
      },
      "CodeConfiguration": {
        "ConfigurationSource": "REPOSITORY"
      }
    }
  }' \
  --instance-configuration '{
    "Cpu": "0.25 vCPU",
    "Memory": "0.5 GB"
  }'
```

## After Deployment

1. **Get Your URL**
   - App Runner will provide a URL like: `https://abc123.us-east-1.awsapprunner.com`
   - This is your live application URL

2. **Update ALLOWED_HOSTS**
   - Add your App Runner URL to environment variables:
   ```
   ALLOWED_HOSTS = abc123.us-east-1.awsapprunner.com,*.awsapprunner.com
   ```

3. **Test Your Application**
   - Visit your App Runner URL
   - Test booking functionality
   - Check that colors and styling are correct

## Benefits of App Runner

✅ **Simple**: No load balancers, no container orchestration
✅ **Cost-effective**: Pay only for what you use
✅ **Auto-scaling**: Handles traffic spikes automatically
✅ **Managed**: No server maintenance required
✅ **CI/CD**: Automatic deployments from GitHub
✅ **HTTPS**: SSL certificate included for free

## Monitoring

- **Logs**: Available in App Runner console
- **Metrics**: CPU, memory, requests automatically tracked
- **Health checks**: Built-in application health monitoring

## Custom Domain (Optional)

1. Go to App Runner service
2. Click "Custom domains"
3. Add your domain (e.g., luxehairstudio.com)
4. Update DNS records as instructed
5. App Runner will handle SSL certificate automatically

## Troubleshooting

**Build Fails:**
- Check `apprunner.yaml` syntax
- Ensure all dependencies are in `requirements.txt`
- Check build logs in App Runner console

**App Won't Start:**
- Check environment variables are set correctly
- Verify `SECRET_KEY` is provided
- Check application logs for Django errors

**502 Errors:**
- Ensure gunicorn is binding to `0.0.0.0:8000`
- Check that port 8000 is specified in apprunner.yaml
- Verify Django `ALLOWED_HOSTS` includes App Runner domain

## Next Steps

1. Deploy using the steps above
2. Test the hair salon application
3. Create a separate App Runner service for the nail salon (when ready)
4. Set up custom domain if desired