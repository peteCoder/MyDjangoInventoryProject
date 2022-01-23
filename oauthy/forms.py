from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Profile
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()

GENDER_CHOICE = [('male', 'Male'), ('female', 'Female')]
POSITION = [('manager', 'Manager'), ('cashier', 'Cashier')]



class ProfileForm(forms.ModelForm):

	gender = forms.ChoiceField(
		widget=forms.RadioSelect(), 
		choices=GENDER_CHOICE
	)
	position = forms.ChoiceField(
		widget=forms.RadioSelect(), 
		choices=POSITION
	)

	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)


		""" FOR first_name field """
		self.fields['first_name'].widget.attrs['class'] = 'form-control form-control-user'
		self.fields['first_name'].widget.attrs['type'] = 'text'
		self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
		self.fields['first_name'].widget.attrs['name'] = 'first_name'
		self.fields['first_name'].widget.attrs['id'] = 'exampleFirstName'

		""" FOR last_name field """
		self.fields['last_name'].widget.attrs['class'] = 'form-control form-control-user'
		self.fields['last_name'].widget.attrs['type'] = 'text'
		self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
		self.fields['last_name'].widget.attrs['name'] = 'last_name'
		self.fields['last_name'].widget.attrs['id'] = 'exampleLastName'


		""" FOR birth_date field """
		self.fields['birth_date'].widget.attrs['class'] = 'form-control form-control-user'
		self.fields['birth_date'].widget.attrs['type'] = 'date'
		self.fields['birth_date'].widget.attrs['placeholder'] = 'Date of Birth (yyyy-mm-dd)'
		self.fields['birth_date'].widget.attrs['name'] = 'dob'

		"""   FOR phone_number field  """
		self.fields['phone_number'].widget.attrs['class'] = 'form-control form-control-user'
		self.fields['phone_number'].widget.attrs['type'] = 'tel'
		self.fields['phone_number'].widget.attrs['placeholder'] = 'Phone Number'
		self.fields['phone_number'].widget.attrs['name'] = 'phone'


		""" FOR address field """
		self.fields['address'].widget.attrs['class'] = 'form-control form-control-user mb-3'
		self.fields['address'].widget.attrs['type'] = 'text'
		self.fields['address'].widget.attrs['placeholder'] = 'Enter Contact Address'
		self.fields['address'].widget.attrs['name'] = 'address'

		
	class Meta:
		model = Profile
		fields = [
			'first_name', 
			'last_name',
			'birth_date', 
			'phone_number', 
			'image', 
			'address'
		]





class MyPassWordChangeForm(PasswordChangeForm):

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user')
		print(user)

		super(MyPassWordChangeForm, self).__init__(user, *args, **kwargs)
		
		self.fields['old_password'].widget.attrs['class'] = 'form-control form-control-user'
		self.fields['old_password'].widget.attrs['id'] = 'exampleInputPassword'
		self.fields['old_password'].widget.attrs['type'] = 'password'
		self.fields['old_password'].widget.attrs['aria-describedby'] = 'passwordHelp'
		self.fields['old_password'].widget.attrs['placeholder'] = 'Old Password'


		self.fields['new_password1'].widget.attrs['class'] = 'form-control form-control-user'
		self.fields['new_password1'].widget.attrs['id'] = 'exampleInputPassword'
		self.fields['new_password1'].widget.attrs['type'] = 'password'
		self.fields['new_password1'].widget.attrs['aria-describedby'] = 'passwordHelp'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'New Password'

		self.fields['new_password2'].widget.attrs['class'] = 'form-control form-control-user'
		self.fields['new_password2'].widget.attrs['id'] = 'exampleInputPassword'
		self.fields['new_password2'].widget.attrs['type'] = 'password'
		self.fields['new_password2'].widget.attrs['aria-describedby'] = 'passwordHelp'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm New Password'


	class Meta:
		model = User
		fields = '__all__'







class CreateUserForm(UserCreationForm):
	
	def __init__(self, *args, **kwargs):

		super(CreateUserForm, self).__init__(*args, **kwargs)

		""" FOR username field """
		self.fields['username'].widget.attrs['class'] = 'form-control form-control-user'
		self.fields['username'].widget.attrs['type'] = 'text'
		self.fields['username'].widget.attrs['placeholder'] = 'Username'
		self.fields['username'].widget.attrs['name'] = 'username'
		self.fields['username'].widget.attrs['id'] = 'exampleInputUsername'

		""" FOR email field """
		self.fields['email'].widget.attrs['class'] = 'form-control form-control-user'
		self.fields['email'].widget.attrs['type'] = 'email'
		self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
		self.fields['email'].widget.attrs['name'] = 'email'
		self.fields['email'].widget.attrs['id'] = 'exampleInputEmail'

		""" FOR first_name field """
		self.fields['first_name'].widget.attrs['class'] = 'form-control form-control-user'
		self.fields['first_name'].widget.attrs['type'] = 'text'
		self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
		self.fields['first_name'].widget.attrs['name'] = 'first_name'
		self.fields['first_name'].widget.attrs['id'] = 'exampleFirstName'

		""" FOR last_name field """
		self.fields['last_name'].widget.attrs['class'] = 'form-control form-control-user'
		self.fields['last_name'].widget.attrs['type'] = 'text'
		self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
		self.fields['last_name'].widget.attrs['name'] = 'last_name'
		self.fields['last_name'].widget.attrs['id'] = 'exampleLastName'


		""" FOR password1 field """
		self.fields['password1'].widget.attrs['class'] = 'form-control form-control-user'
		self.fields['password1'].widget.attrs['type'] = 'password'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].widget.attrs['name'] = 'password1'
		self.fields['password1'].widget.attrs['id'] = 'exampleInputPassword'



		""" FOR password2 field """
		self.fields['password2'].widget.attrs['class'] = 'form-control form-control-user'
		self.fields['password2'].widget.attrs['type'] = 'password'
		self.fields['password2'].widget.attrs['placeholder'] = 'Password Confirmation'
		self.fields['password2'].widget.attrs['name'] = 'password2'
		self.fields['password2'].widget.attrs['id'] = 'exampleRepeatPassword'

	class Meta:
		model = User
		fields = [
			'first_name', 'last_name', 
			'username', 'email', 'password1', 
			'password2'
		]







class EditProfileForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)

		""" FOR first_name field """
		self.fields['first_name'].widget.attrs['class'] = 'form-control form-control-user'
		self.fields['first_name'].widget.attrs['type'] = 'text'
		self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
		self.fields['first_name'].widget.attrs['name'] = 'first_name'
		self.fields['first_name'].widget.attrs['id'] = 'exampleFirstName'

		""" FOR last_name field """
		self.fields['last_name'].widget.attrs['class'] = 'form-control form-control-user'
		self.fields['last_name'].widget.attrs['type'] = 'text'
		self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
		self.fields['last_name'].widget.attrs['name'] = 'last_name'
		self.fields['last_name'].widget.attrs['id'] = 'exampleLastName'


		""" FOR birth_date field """
		self.fields['birth_date'].widget.attrs['class'] = 'form-control form-control-user'
		self.fields['birth_date'].widget.attrs['type'] = 'date'
		self.fields['birth_date'].widget.attrs['placeholder'] = 'Date of Birth (yyyy-mm-dd)'
		self.fields['birth_date'].widget.attrs['name'] = 'dob'

		"""   FOR phone_number field  """
		self.fields['phone_number'].widget.attrs['class'] = 'form-control form-control-user'
		self.fields['phone_number'].widget.attrs['type'] = 'tel'
		self.fields['phone_number'].widget.attrs['placeholder'] = 'Phone Number'
		self.fields['phone_number'].widget.attrs['name'] = 'phone'


		""" FOR address field """
		self.fields['address'].widget.attrs['class'] = 'form-control form-control-user mb-3'
		self.fields['address'].widget.attrs['type'] = 'text'
		self.fields['address'].widget.attrs['placeholder'] = 'Enter Contact Address'
		self.fields['address'].widget.attrs['name'] = 'address'

		
	class Meta:
		model = Profile
		fields = [
			'first_name', 
			'last_name',
			'birth_date', 
			'phone_number', 
			'image', 
			'address',
		]