from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect, get_object_or_404
from . import forms
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from notification.models import *


# Create your views here.



@login_required
def navigation(request):
	template = loader.get_template('navigation.html')
	context = {}
	return HttpResponse(template.render(context, request))



def LoginView(request):
	if request.user.is_authenticated:
		return redirect('navigation')
	else:
		if request.method == 'POST':
			password = request.POST.get('password')
			username = request.POST.get('username')

			user = authenticate(username=username, password=password)

			if user is not None:
				login(request, user)
				messages.success(request, "You have successfully logged in.")	
				return redirect('navigation')
			else:
				messages.error(request, "Please enter a valid username and password.")


	return render(request, 'registration/login.html', {})

	

def LogoutView(request):
	logout(request)
	return redirect('login-user')

def myCreateUserView(request):
	if not request.user.is_authenticated:
		if request.method == 'POST':
			form = forms.CreateUserForm(request.POST)
			if form.is_valid():
				userform = form.save()
				userform.refresh_from_db() # Database is refreshed so that profile will automatically save first_name and last_name
				userform.profile.first_name = form.cleaned_data['first_name']
				userform.profile.last_name = form.cleaned_data['last_name']
				userform.save()

				username = form.cleaned_data['username']
				password = form.cleaned_data['password1']
				user = authenticate(request, username=username, password=password)
				if user is not None:
					if request.user.is_authenticated:
						logout(request)
					login(request, user)
				messages.success(request, f"User {username} was successfully created. You are logged in as {username}. ")
				
				return redirect('create_profile')
				
			messages.error(request, f"No user was successfully added... ")
		else:
			form = forms.CreateUserForm()
	else:
		return redirect('navigation') 


	context = {'form': form}

	return render(request, 'registration/createuser.html', context)




@login_required
def createProfileView(request):
	user_image_path = request.user.profile.image
	if request.method == 'POST':
		form = forms.ProfileForm(request.POST, request.FILES, instance=request.user.profile)
		if form.is_valid():
			profile = form.save(commit=False)
			profile.gender = form.cleaned_data['gender']
			profile.position = form.cleaned_data['position']
			# if profile.position == 'Pharmacist':
			# 	user = User.objects.get(username=request.user.username)
			# 	user.is_active = True
			# 	user.save()
			# 	request.user.is_staff = True
			profile.save()
			return redirect('navigation')

	form = forms.ProfileForm(instance=request.user.profile)

	context = {'form': form, 'image_path': user_image_path}
	return render(request, 'registration/create_profile.html', context)


@login_required
def EditProfileView(request):
	user_image_path = request.user.profile.image
	user = request.user
	if request.method == 'POST':
		form = forms.EditProfileForm(request.POST, request.FILES, instance=user.profile)
		if form.is_valid():
			profile = form.save(commit=False)
			profile.gender = user.profile.gender 
			profile.position = user.profile.position 
			profile.save()
			return redirect('profile-detail')

	form = forms.ProfileForm(instance=user.profile)

	context = {'form': form, 'image_path': user_image_path}

	return render(request, 'registration/edit_profile.html', context)






@login_required
def profileDetailView(request):
	user = request.user
	nav_notify = PharmacyNotification.objects.all().order_by('-date')[:2]

	notification_count = PharmacyNotification.objects.filter(is_seen=False).all().count()

	context = {
		'user':user,
		'nav_notify':nav_notify,
		'notification_count':notification_count

	}
	return render(request, 'registration/user_profile.html', context)


# @login_required
# def myPasswordChangeView(request):
# 	form = forms.MyPassWordChangeForm(user=request.user)
# 	if request.method == 'POST':
# 		form = forms.MyPassWordChangeForm(user=request.user, data=request.POST or None)
# 		if form.is_valid():
# 			form.save()
# 			update_session_auth_hash(request, form.user)
# 			messages.success(request, 'Password was changed successfully')
# 			return redirect('navigation')
# 		else:
# 			messages.error(request, 'Was unable to change Password. Something went wrong.')

# 	context = {'form':form}


# 	return render(request, 'registration/password_change.html', context)




class myPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
	template_name = 'registration/password_change.html'
	form_class = forms.MyPassWordChangeForm
	success_url = reverse_lazy('navigation')

	# DEFAULT
	def get_form_kwargs(self):
		kwargs = super(myPasswordChangeView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		# kwargs.pop('user')
		return kwargs

