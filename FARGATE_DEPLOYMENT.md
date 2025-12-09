# AWS Fargate Deployment Guide

## Prerequisites
- AWS CLI installed and configured
- Docker installed locally
- AWS account with appropriate permissions

## Step 1: Create ECR Repository
```bash
aws ecr create-repository --repository-name luxe-hair-studio --region us-east-1
```

## Step 2: Build and Push Docker Image
```bash
# Get ECR login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

# Build image
docker build -t luxe-hair-studio .

# Tag image
docker tag luxe-hair-studio:latest <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/luxe-hair-studio:latest

# Push to ECR
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/luxe-hair-studio:latest
```

## Step 3: Create Secrets in AWS Secrets Manager
```bash
aws secretsmanager create-secret \
  --name django-secret-key \
  --secret-string "h070k21hg)+r+#5tdv1$73+=&jdxz&qxqh_8%tz6-*@6p)buh9" \
  --region us-east-1
```

## Step 4: Create ECS Cluster
```bash
aws ecs create-cluster --cluster-name luxe-hair-studio-cluster --region us-east-1
```

## Step 5: Update task-definition.json
- Replace `<YOUR_ECR_IMAGE_URI>` with your ECR image URI
- Replace `REGION` and `ACCOUNT` in secrets ARN

## Step 6: Register Task Definition
```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

## Step 7: Create Application Load Balancer (ALB)
1. Go to EC2 Console → Load Balancers
2. Create Application Load Balancer
3. Configure security groups (allow HTTP/HTTPS)
4. Create target group (type: IP, port: 8000)

## Step 8: Create ECS Service
```bash
aws ecs create-service \
  --cluster luxe-hair-studio-cluster \
  --service-name luxe-hair-studio-service \
  --task-definition luxe-hair-studio \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx,subnet-yyy],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=django-app,containerPort=8000"
```

## Step 9: Update ALLOWED_HOSTS
Add your ALB DNS name to Railway environment variables:
```
ALLOWED_HOSTS=your-alb-name.us-east-1.elb.amazonaws.com
```

## Cost Estimate
- Fargate: ~$15-20/month (0.25 vCPU, 0.5 GB)
- ALB: ~$16/month
- **Total: ~$31-36/month**

## Benefits
- Fully managed (no servers)
- Auto-scaling
- Integrated with AWS services
- Production-ready
