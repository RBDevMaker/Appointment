# ✨ Luxe Hair Studio – Appointment Booking App

A beautifully designed hair studio booking system featuring **AWS App Runner deployment, Docker**, and a fully automated **CI/CD pipeline** powered by GitHub Actions.

## 🚀 CI/CD Pipeline – Fully Automated

Whenever you push to the **main branch**:

**1. GitHub Actions** builds your Docker image

**2.** Pushes the image to **Amazon ECR**

**3. App Runner** pulls the new image and deploys automatically

## 🔍 Pipeline in action:

- Open GitHub repo → **Actions**tab

- See the workflow: **“Deploy to AWS App Runner”**

- Make any small change (e.g., update text or a color), push it — the app redeploys automatically!

## 💇‍♀️ Current Features
### 🗓️ Booking System

- View available stylists: **Ann** and **Jackie**

- Browse each stylist’s available time slots

- Select appointment date from a calendar

- Book using **name + contact details**

- **12-hour time format** (e.g., 9:00 AM)

- All appointments stored in SQLite

- Email appointment confirmations

- SMS reminders

- Online payments

- Admin dashboard for managing appointments

- Customer accounts / login

- Appointment cancellation

- Recurring appointments

- Select services (cut, color, style, etc.)

- Pricing display

### 🎨 Design & UI

- **Soft pink** #f5a3b8 and **rose gold** #d4af37 

- Warm beige background for a cozy feel

- Headers in **Playfair Display**
  
- Smooth hover animations

- Responsive stylist cards

- Designed for both **hair** and **nail** salons

### 🛠 Technical Overview

- Backend: **Django**

- Database: **SQLite** (local storage)

- Deployment: **AWS App Runner**

- CI/CD: GitHub Actions → Build → Docker → Push to ECR → App Runner Deploy

- Environment variables for configuration

- Dockerized for consistent deployment

- Supports multiple business themes (hair or nail studios)

### 🧱 Tech Stack

- **Python / Django**

- **HTML / CSS / JavaScript**

- **Docker**

- **GitHub Actions**

- **Amazon ECR**

- **AWS App Runner**

![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.x-092E20?logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-App%20Runner-FF9900?logo=amazonaws&logoColor=white)
![ECR](https://img.shields.io/badge/AWS-ECR-FF9900?logo=amazonaws&logoColor=white)


## 🚀 Deployment Workflow

Triggered automatically on push to main:

CI/CD: GitHub Actions → Build → Docker → Push to ECR → App Runner Deploy

No manual deployment needed.
