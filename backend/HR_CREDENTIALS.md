# HR User Credentials for MindEase

## 🔐 HR Login Credentials

### HR User #1 - Primary HR Manager
```
Username: hr@mindease.com
Email: hr@mindease.com
Password: hr123456
Name: Sarah Johnson
Role: HR Manager
```

### HR User #2 - HR Admin
```
Username: hr.admin@mindease.com
Email: hr.admin@mindease.com
Password: hradmin123
Name: Michael Chen
Role: HR Admin
```

### HR User #3 - Recruitment Specialist
```
Username: recruitment@mindease.com
Email: recruitment@mindease.com
Password: recruit123
Name: Emma Williams
Role: Recruitment Specialist
```

---

## 📱 How to Access HR Dashboard

1. **Login Page:**
   - Navigate to: `http://127.0.0.1:8000/create/login/`
   - Or: `http://127.0.0.1:8000/accounts/login/`

2. **Enter Credentials:**
   - Use any of the HR credentials above
   - Username: `hr@mindease.com`
   - Password: `hr123456`

3. **After Login:**
   - You'll be redirected to: `http://127.0.0.1:8000/create/redirect/`
   - Then automatically to HR Dashboard: `http://127.0.0.1:8000/loging/hr/`

---

## 🎯 HR Dashboard Features

### Available Functions:
- ✅ **View Dashboard** - Statistics and analytics
- ✅ **Post New Job** - Create job openings (`/hr/post-job/`)
- ✅ **View Public Jobs** - See all active job listings (`/internship`)
- ✅ **Review Applications** - Check candidate submissions
- ✅ **Manage Calendar** - Schedule interviews
- ✅ **View Recent Responses** - Track new applications

---

## 📋 Quick Test Steps

### 1. Test HR Login
```bash
# Login with:
Username: hr@mindease.com
Password: hr123456
```

### 2. Post a New Job
- Click "Post New Job" in sidebar
- Or navigate to: `/hr/post-job/`
- Fill out job details:
  - Job Title (e.g., "Senior Counsellor")
  - Job Description
  - Location (Remote/On-site)
  - Type (Counsellor/Intern)
  - Salary
  - Duration (in months)
  - Experience (in years)
  - Last date to apply

### 3. View Public Job Listings
- Navigate to: `/internship`
- See all active job postings
- Test "Apply Now" button

### 4. Test Job Application
- Click "Apply Now" on any job
- Fill application form
- Upload resume and cover letter
- Submit and see success page

---

## 🔄 Password Reset (if needed)

If you need to reset any password, run:

```bash
cd /Users/prateekmac/Desktop/project\ x/prutha
source virtual/bin/activate
python manage.py shell
```

Then in Python shell:
```python
from loging.models import CustomUser
from django.contrib.auth.hashers import make_password

user = CustomUser.objects.get(email='hr@mindease.com')
user.password = make_password('newpassword123')
user.save()
```

---

## 📞 Support

For any issues:
- Check Django logs in terminal
- Verify user_type is set to 'HR'
- Ensure email_verified is True

---

**Created:** October 11, 2025  
**Last Updated:** October 11, 2025  
**System:** MindEase HR Management System

