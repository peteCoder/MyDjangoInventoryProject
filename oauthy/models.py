from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
	GENDER_CHOICE = [('male', 'Male'), ('female', 'Female')]
	POSITION = [('manager', 'manager'), ('cashier', 'cashier')]
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=100, blank=True)
	last_name = models.CharField(max_length=100, blank=True)
	phone_number = models.CharField(max_length=100, blank=True)
	address = models.CharField(max_length=100, blank=True)
	gender = models.CharField(max_length=6, choices=GENDER_CHOICE, blank=True, default='male')
	position = models.CharField(max_length=10, choices=POSITION, blank=True, default='cashier')
	birth_date = models.DateField(null=True, blank=True)
	image = models.ImageField(upload_to='profile', null=False, blank=True)
	bio = models.TextField(blank=True, null=True)


	@property
	def birth_date_format(self):
		date = self.birth_date.strftime("%d/%m/%Y")
		return date



	@property
	def getFullName(self):
		return self.first_name.title() + " " + self.last_name.title()
	
	# In case User instance does not upload an image. 
	# These are the default images that will be uploaded if user is either male or female.
	@property
	def ImageURL(self):
		try:
			url = self.image.url
		except:
			if self.gender == 'female':
				url = '/media/profile/undraw_profile_female.svg'
			else:
				url = '/media/profile/undraw_profile_male.svg'
		return url

	def __str__(self):
		return self.user.username


	


# Profile will be automatically created when user is created

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)




