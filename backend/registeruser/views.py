# # from django.shortcuts import render

# # # Create your views here.
# from django.shortcuts import render, redirect
# # from django.contrib.auth import login
# from .forms import UserRegistrationForm
# from django.urls import reverse_lazy
# # def register(request):
# #     if request.method == "POST":
# #         user_form = UserRegistrationForm(request.POST)
# #         profile_form = ProfileForm(request.POST)

# #         if user_form.is_valid() and profile_form.is_valid():
# #             user = user_form.save(commit=False)   # Save User but don’t commit yet
# #             user.set_password(user_form.cleaned_data['password'])  # Hash password
# #             user.save()

# #             # Create profile linked to user
# #             profile = profile_form.save(commit=False)
# #             profile.user = user
# #             profile.save()

# #             login(request, user)  # Auto-login after register
# #             return redirect('home')  # redirect to homepage
# #     else:
# #         user_form = UserRegistrationForm()
# #         profile_form = ProfileForm()

# #     return render(request, 'register.html', {
# #         'user_form': user_form,
# #         'profile_form': profile_form
# #     })

# from django.shortcuts import render, redirect
# from django.views import View
# from .forms import UserRegistrationForm

# class RegisterView(View):
#     def get(self, request):
#         user_form = UserRegistrationForm()
#         return render(request, "registeruser/register.html", {"user_form": user_form})

#     def post(self, request):
#         user_form = UserRegistrationForm(request.POST)

#         if user_form.is_valid():
#             user = user_form.save()
#             return redirect(reverse_lazy("userend:home"))

#         return render(request, "registeruser/register.html", {"user_form": user_form})