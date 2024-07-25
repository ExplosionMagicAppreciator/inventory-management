from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Category, InventoryItem, Warehouse


class UserRegistirationForm(forms.ModelForm):
	password = forms.CharField(
		label='Password',
		widget=forms.PasswordInput
	)
	password2 = forms.CharField(
		label='Repeat password',
		widget=forms.PasswordInput
	)
	"""id_number = forms.CharField(
		label='ID number',
		widget=forms.TextInput
	)"""

	
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'id', 'email']

	def clean_password2(self):
		cleaned = self.cleaned_data
		if cleaned['password'] != cleaned ['password2']:
			raise forms.ValidationError('passwords do not match')
		return cleaned['password2']
	
	def clean_id(self):
		data = self.cleaned_data['id']
		if User.objects.filter(id=data).exists():
			raise forms.ValidationError(
				'ID number is already linked to another account'
			)
		return data
	
	def clean_email(self):
		data = self.cleaned_data['email']
		if User.objects.filter(email=data).exists():
			return forms.ValidationError(
				'Email address is already linked to another account'
			)
		return data


class InventoryItemForm(forms.ModelForm):
	category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)
	warehouse = forms.ModelChoiceField(queryset=Warehouse.objects.all(), initial=0)
	class Meta:
		model = InventoryItem
		fields = ['name', 'quantity', 'category', 'warehouse']