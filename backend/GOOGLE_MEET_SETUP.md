# Google Meet Integration Setup Guide

## Current Status
✅ **Google Meet integration is implemented and ready**
✅ **Google Cloud project is set up** (subtle-osprey-403915)
✅ **Service Account credentials are configured**
❌ **Google Meet API needs proper configuration for genuine meet links**

## What's Working
- The system is configured to generate **GENUINE Google Meet links ONLY**
- **NO fallback or fake links** - only genuine Google Meet API links
- Proper error handling for missing/invalid credentials
- Email notifications with meet links are ready
- **Appointments will NOT be approved without genuine meet links**

## Setup Required

### 1. Enable Required APIs
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project: **subtle-osprey-403915**
3. Go to "APIs & Services" > "Library"
4. Enable these APIs:
   - **Google Calendar API** ✅
   - **Google Meet API** (if available)
   - **Google Workspace API** (if available)
5. Make sure all APIs are enabled and active

### 2. Create Service Account
1. Go to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account"
3. Name: "euphoria-meet-integration"
4. Description: "e"
5. Click "Create and Continue"
6. Role: "Editor" (or "Calendar Admin" if available)
7. Click "Continue" and then "Done"

### 3. Download Service Account Key
1. Click on the created service account (euphoria-meet-integration)
2. Go to "Keys" tab
3. Click "Add Key" > "Create new key"
4. Choose "JSON" format
5. Click "Create" - this will download the JSON file

### 4. Replace Current File
1. **IMPORTANT**: The current file contains Web OAuth credentials, not Service Account credentials
2. Replace `/Users/prateekmac/Desktop/project x/prutha/service_account.json` with the downloaded Service Account JSON file
3. The Service Account JSON should look like this:
```json
{
  "type": "service_account",
  "project_id": "subtle-osprey-403915",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "euphoria-meet-integration@subtle-osprey-403915.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "..."
}
```

### 5. Grant Calendar Access to Gmail Account
**For testing with Gmail account: singprateek165@gmail.com**

1. Copy the service account email from your JSON file (e.g., `euphoria-meet-integration@subtle-osprey-403915.iam.gserviceaccount.com`)
2. Go to [Google Calendar](https://calendar.google.com/) and login with `singprateek165@gmail.com`
3. Click the "+" next to "Other calendars" in the left sidebar
4. Click "Subscribe to calendar"
5. Enter the service account email
6. Set permission to "Make changes to events"
7. Click "Add calendar"

**Alternative: Share your Gmail calendar with the service account**
1. In Google Calendar, click the three dots next to your calendar
2. Select "Settings and sharing"
3. Under "Share with specific people", click "Add people"
4. Enter the service account email
5. Set permission to "Make changes to events"
6. Click "Send"

## Testing
Once setup is complete, test by:
1. Login as a counsellor (e.g., `dr_johnson` / `counsellor123`)
2. Go to pending approvals
3. Approve an appointment
4. Check console for: `✅ GENUINE GOOGLE MEET LINK GENERATED`
5. Patient should receive email with working meet link

## Current Behavior
- **With valid credentials**: Generates genuine Google Meet links
- **With invalid/missing credentials**: Shows clear error messages, no fallback
- **Email sending**: Works with SendGrid regardless of meet link status

## File Locations
- Service Account: `/Users/prateekmac/Desktop/project x/prutha/service_account.json`
- Meet Link Logic: `Counsellordashboard/views.py` (lines 15-72)
- Email Service: `loging/email_service.py`
