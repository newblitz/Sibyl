import os
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class SendGridEmailService:
    def __init__(self):
        self.api_key = settings.SENDGRID_API_KEY
        self.from_email = settings.DEFAULT_FROM_EMAIL
        
    def send_verification_email(self, to_email, otp):
        """
        Send OTP verification email using Django's email backend (SendGrid)
        """
        try:
            # Create the email content
            subject = "OTP for Email Verification - Euphoria"
            
            # HTML content
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Email Verification</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #06b6d4, #7c3aed); color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .otp-box {{ background: #fff; border: 2px solid #7c3aed; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0; }}
                    .otp-code {{ font-size: 32px; font-weight: bold; color: #7c3aed; letter-spacing: 5px; }}
                    .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 14px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Euphoria</h1>
                        <p>Email Verification</p>
                    </div>
                    <div class="content">
                        <h2>Hello!</h2>
                        <p>Thank you for registering with Euphoria! To complete your registration, please use the verification code below:</p>
                        
                        <div class="otp-box">
                            <p style="margin: 0 0 10px 0; color: #666;">Your verification code is:</p>
                            <div class="otp-code">{otp}</div>
                        </div>
                        
                        <p><strong>Important:</strong></p>
                        <ul>
                            <li>This code will expire in 5 minutes</li>
                            <li>Enter this code exactly as shown</li>
                            <li>If you didn't request this code, please ignore this email</li>
                        </ul>
                        
                        <p>If you have any questions, please contact our support team.</p>
                        
                        <p>Best regards,<br>The Euphoria Team</p>
                    </div>
                    <div class="footer">
                        <p>© 2025 
                    Euphoria. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Plain text content
            text_content = f"""
            Hello!
            
            Thank you for registering with Euphoria! 
            
            Your verification code is: {otp}
            
            This code will expire in 5 minutes. Please enter this code to complete your registration.
            
            If you didn't request this code, please ignore this email.
            
            Best regards,
            Euphoria Team
            """
            
            # Send email using Django's email backend
            print(f"📧 Sending email via Django backend to {to_email}")
            print(f"📧 Using backend: {settings.EMAIL_BACKEND}")
            print(f"📧 From email: {self.from_email}")
            
            try:
                # Use Django's send_mail function
                result = send_mail(
                    subject=subject,
                    message=text_content,
                    from_email=self.from_email,
                    recipient_list=[to_email],
                    html_message=html_content,
                    fail_silently=False
                )
                
                if result:
                    logger.info(f"Email sent successfully to {to_email}")
                    print(f"✅ Email sent successfully via Django backend to {to_email}")
                    return True
                else:
                    logger.error(f"Failed to send email to {to_email}")
                    print(f"❌ Failed to send email to {to_email}")
                    return False
                    
            except Exception as e:
                logger.error(f"Email sending error: {str(e)}")
                print(f"❌ Email sending error: {str(e)}")
                # Fall through to console output
            
            # Fallback: Print to console (for testing or if email fails)
            print(f"\n{'='*60}")
            print(f"📧 EMAIL VERIFICATION OTP (Fallback)")
            print(f"{'='*60}")
            print(f"To: {to_email}")
            print(f"OTP: {otp}")
            print(f"Subject: {subject}")
            print(f"{'='*60}\n")
            
            return True
                
        except Exception as e:
            logger.error(f"Error in email service: {str(e)}")
            # Fallback to console output
            print(f"\n{'='*60}")
            print(f"📧 EMAIL VERIFICATION OTP (Error Fallback)")
            print(f"{'='*60}")
            print(f"To: {to_email}")
            print(f"OTP: {otp}")
            print(f"Error: {str(e)}")
            print(f"{'='*60}\n")
            return True  # Return True so registration can continue

    def send_meet_link_email(self, to_email, patient_name, counsellor_name, appointment_date, appointment_time, meet_link):
        """
        Send Google Meet link email to patient
        """
        try:
            # Create the email content
            subject = f"Your Therapy Session with {counsellor_name} - Google Meet Link"
            
            # HTML content
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Therapy Session - Meet Link</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .meet-link {{ background: #4CAF50; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; font-weight: bold; }}
                    .appointment-details {{ background: white; padding: 20px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #667eea; }}
                    .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎯 Your Therapy Session is Confirmed!</h1>
                        <p>Your appointment has been approved by your counsellor</p>
                    </div>
                    
                    <div class="content">
                        <h2>Hello {patient_name},</h2>
                        
                        <p>Great news! Your therapy session has been approved by <strong>{counsellor_name}</strong>.</p>
                        
                        <div class="appointment-details">
                            <h3>📅 Appointment Details:</h3>
                            <p><strong>Date:</strong> {appointment_date}</p>
                            <p><strong>Time:</strong> {appointment_time}</p>
                            <p><strong>Counsellor:</strong> {counsellor_name}</p>
                        </div>
                        
                        <p>Click the button below to join your therapy session:</p>
                        
                        <div style="text-align: center;">
                            <a href="{meet_link}" class="meet-link">🎥 Join Therapy Session</a>
                        </div>
                        
                        <p><strong>Important Notes:</strong></p>
                        <ul>
                            <li>Please join the session 5 minutes before the scheduled time</li>
                            <li>Ensure you have a stable internet connection</li>
                            <li>Find a quiet, private space for your session</li>
                            <li>Have your camera and microphone ready</li>
                        </ul>
                        
                        <p>If you have any questions or need to reschedule, please contact us.</p>
                        
                        <p>We look forward to supporting you on your mental health journey.</p>
                        
                        <div class="footer">
                            <p>Best regards,<br>The Euphoria Team</p>
                            <p>This is an automated message. Please do not reply to this email.</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Try to send via Django's email backend (SendGrid)
            try:
                result = send_mail(
                    subject=subject,
                    message=f"Your therapy session with {counsellor_name} is confirmed. Meet Link: {meet_link}",
                    from_email=self.from_email,
                    recipient_list=[to_email],
                    html_message=html_content,
                    fail_silently=False
                )
                
                if result:
                    logger.info(f"Meet link email sent successfully to {to_email}")
                    print(f"✅ Meet link email sent successfully to {to_email}")
                    return True
                else:
                    logger.error(f"Failed to send meet link email to {to_email}")
                    print(f"❌ Failed to send meet link email to {to_email}")
                    return False
                    
            except Exception as e:
                logger.error(f"Meet link email sending error: {str(e)}")
                print(f"❌ Meet link email sending error: {str(e)}")
                # Fall through to console output
            
            # Fallback: Print to console (for testing or if email fails)
            print(f"\n{'='*60}")
            print(f"📧 MEET LINK EMAIL (Fallback)")
            print(f"{'='*60}")
            print(f"To: {to_email}")
            print(f"Patient: {patient_name}")
            print(f"Counsellor: {counsellor_name}")
            print(f"Date: {appointment_date}")
            print(f"Time: {appointment_time}")
            print(f"Meet Link: {meet_link}")
            print(f"Subject: {subject}")
            print(f"{'='*60}\n")
            
            return True
                
        except Exception as e:
            logger.error(f"Error in meet link email service: {str(e)}")
            # Fallback to console output
            print(f"\n{'='*60}")
            print(f"📧 MEET LINK EMAIL (Error Fallback)")
            print(f"{'='*60}")
            print(f"To: {to_email}")
            print(f"Patient: {patient_name}")
            print(f"Counsellor: {counsellor_name}")
            print(f"Date: {appointment_date}")
            print(f"Time: {appointment_time}")
            print(f"Meet Link: {meet_link}")
            print(f"Error: {str(e)}")
            print(f"{'='*60}\n")
            return True  # Return True so appointment can continue

# Create a global instance
email_service = SendGridEmailService()