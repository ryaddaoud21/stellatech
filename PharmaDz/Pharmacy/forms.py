from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Userprofile
from Store.models import Review,RATE_CHOICES

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Userprofile
        fields = ['name','Sex', 'Address','Email', 'Phone','is_admin',]




from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class AddReviewForm(forms.ModelForm):
    class Meta :
        model = Review
        fields = '__all__'




class RateForm(forms.ModelForm):
	rate = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(), required=True)
	class Meta:
		model = Review
		fields = ('rate',)

from .models import Customer
class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'

