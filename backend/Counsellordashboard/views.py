from django.shortcuts import render,redirect
from django.views import View
from django.utils import timezone
from django.contrib import messages
from CounsellorIntern.forms import DailyLog_CounsellorFormpopup,DailyCousellorForm
from CounsellorIntern.models import DailyLog_Counsellor,DailyNotification_Counsellor,Dailylog_Counserllor_patient
from .forms import DailyNotification_CounsellorForm
from userend.models import Appointment
from loging.email_service import email_service
from userend.daily_utils import create_daily_meeting_for_appointment
from datetime import datetime, timedelta
# Create your views here.

# Google Calendar API removed - now using Daily.co API

class Notification_approval(View):
    def get(self, request):
        # Check if user is authenticated and is a counsellor
        if not request.user.is_authenticated:
            return redirect('loging:loginView')
        
        if request.user.user_type != 'Counsellor':
            # Redirect non-counsellors to appropriate dashboard
            if request.user.user_type == 'Patient':
                return redirect('userend:appointment')
            else:
                return redirect('loging:login')
        
        current_date=timezone.now().date()
        
        # Get pending appointments for this doctor
        pending_appointments = Appointment.objects.filter(
            selected_doctor__Auth_id=request.user,
            IsPending=True
        ).order_by('appointment_date')
        
        return render(request, "Counsellordashborad/pending_approval.html", {
            "pending_appointments": pending_appointments
        })
    def post(self, request):
        appointment_id = request.POST.get("appointment_id")
        action = request.POST.get("action")
        
        if appointment_id and action:
            try:
                appointment = Appointment.objects.get(
                    id=appointment_id,
                    selected_doctor__Auth_id=request.user,
                    IsPending=True
                )
                
                if action == "approve":
                    appointment.IsPending = False
                    appointment.Assigned_doctor = appointment.selected_doctor
                    appointment.save()  # Save the approval first
                    
                    # Generate Daily.co meeting link
                    try:
                        # Generate Daily.co meeting link using the existing utility function
                        meet_link, room_name = create_daily_meeting_for_appointment(appointment)
                        
                        if meet_link:
                            appointment.meet_link = meet_link
                            appointment.meet_name = room_name
                            appointment.save()
                            
                            print(f"✅ Daily.co meeting link generated: {meet_link}")
                            
                            # Send email to patient with meet link
                            patient_name = f"{appointment.first_name} {appointment.last_name}"
                            counsellor_name = f"{appointment.selected_doctor.Auth_id.first_name} {appointment.selected_doctor.Auth_id.last_name}"
                            patient_email = appointment.user.email
                            
                            email_service.send_meet_link_email(
                                to_email=patient_email,
                                patient_name=patient_name,
                                counsellor_name=counsellor_name,
                                appointment_date=appointment.appointment_date.strftime('%B %d, %Y'),
                                appointment_time=appointment.time_slot,
                                meet_link=meet_link
                            )
                            
                            print(f"✅ Daily.co meeting link generated and email sent for appointment {appointment.id}")
                            messages.success(request, f"Appointment approved! Meeting link sent to {patient_name}.")
                        else:
                            print("⚠️ Daily.co meeting link generation failed, but appointment approved")
                            messages.warning(request, "Appointment approved, but meeting link generation failed. Please contact the patient directly.")
                        
                    except Exception as e:
                        print(f"❌ Error generating Daily.co meeting link: {e}")
                        print("⚠️ Proceeding with approval without meet link")
                        messages.warning(request, "Appointment approved, but meeting link generation failed. Please contact the patient directly.")
                    
                    # Create entry in Dailylog_Counserllor_patient
                    from CounsellorIntern.models import Dailylog_Counserllor_patient
                    Dailylog_Counserllor_patient.objects.create(
                        doctor_id=appointment.selected_doctor.Auth_id,
                        patient_id=appointment,
                        date=appointment.appointment_date,
                        time_slot=appointment.time_slot
                    )
                    
                elif action == "reject":
                    patient_name = f"{appointment.first_name} {appointment.last_name}"
                    appointment.delete()
                    messages.success(request, f"Appointment request from {patient_name} has been rejected.")
                    
            except Appointment.DoesNotExist:
                pass  # Appointment not found or doesn't belong to this doctor
        
        return redirect('Counsellordashboard:pending_approval')

class CounsellorAppointments(View):
    def get(self, request):
        # Check if user is authenticated and is a counsellor
        if not request.user.is_authenticated:
            return redirect('loging:loginView')
        
        if request.user.user_type != 'Counsellor':
            # Redirect non-counsellors to appropriate dashboard
            if request.user.user_type == 'Patient':
                return redirect('userend:appointment')
            else:
                return redirect('loging:login')
        current_date = timezone.now().date()
        current_datetime = timezone.now()
        
        # Get approved appointments for this counsellor
        
        approved_appointments = Dailylog_Counserllor_patient.objects.filter(doctor_id=request.user,date=current_date,completed=False).order_by('time_slot')
        timed_appointments = []
        for appointment in approved_appointments:
            if current_datetime.time() <= datetime.strptime(appointment.time_slot, "%H:%M").time():
                timed_appointments.append(appointment)
        # DailyCousellingForm = DailyCousellorForm()
        list_of_appointments = []
        for appointment in timed_appointments:
            name=f"{appointment.patient_id.first_name} {appointment.patient_id.last_name}"
            DailyCousellingForm = DailyCousellorForm(instance=appointment,initial={'name':name})
            list_of_appointments.append({
                'form': DailyCousellingForm,
                'appointment': appointment,
                'patient': appointment.patient_id
            })
        return render(request, "Counsellordashborad/appointmentofcounsellor.html", {
            "approved_appointments": list_of_appointments
        })

    def post(self, request):
        if request.POST.get("completed"):
            appointment_id = request.POST.get("appointment_id")
            appointment = Dailylog_Counserllor_patient.objects.get(id=appointment_id)
            appointment.completed = True
            appointment.save()
            return redirect('Counsellordashboard:appointments')

        # appointment_id = request.POST.get("appointment_id")
        # action = request.POST.get("action")
        # if appointment_id and action:
        #     try:
        #         appointment = Dailylog_Counserllor_patient.objects.get(id=appointment_id)
        #         appointment.completed = True
        #         appointment.save()
        #     except Dailylog_Counserllor_patient.DoesNotExist:
        #         pass