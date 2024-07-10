# forms.py
from django import forms
from django.forms import ModelForm, Form, TextInput, PasswordInput, CharField,CheckboxInput,DateField,DateInput,Select
from .models import User,EmployeeEmployer, Address,JobSeeker,RelationshipType,UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator
from django.utils import timezone


class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)


class UserForm(UserCreationForm):
    first_name = CharField(
        label=("First Name"),
        max_length=30,
        required=False,
        widget=TextInput(attrs={"class": "form-control"}),
    )
    last_name = CharField(
        label=("Last Name"),
        max_length=30,
        required=False,
        widget=TextInput(attrs={"class": "form-control"}),
        
    )
    dob = DateField(
        label="Date of Birth",
        required=False,
        widget=DateInput({"class": "form-control"}),
        initial=timezone.now,
    )
    
    
    smoke = CharField(
        label="Smoke",
        required=False,
        widget=Select(
            choices=[("N", "No"), ("Y", "Yes"), ("P", "Plan to Quit")],
            attrs={"class": "form-select"},
        ),
    )
    drinking = CharField(
        label="Drinking",
        required=False,
        widget=Select(
            choices=[("T", "Yes"), ("F", "No"), ("P", "Plan to Quit")],
            attrs={"class": "form-select"},
        ),
    )
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "dob",
            "smoke",
            "drinking",
           
        ]
    

class EmployeeEmployerForm(ModelForm):
    class Meta:
        model = EmployeeEmployer
        fields = "__all__"
        
class JobSeekerForm(ModelForm):
    class Meta:
        model = JobSeeker
        fields = "__all__"

class RelationshipTypeForm(forms.ModelForm):
    class Meta:
        model = RelationshipType
        fields = "__all__"
        widgets = {
        'name': forms.RadioSelect(choices=RelationshipType.RELATIONSHIP_CHOICES)
        }
    class UserPreferenceForm(forms.Form):
        GENDER_CHOICES = [
            ('men', 'Men'),
            ('women', 'Women'),
            ('both', 'Both'),
    ]
    
        gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)



class AddressUpsertForm(ModelForm):
    class Meta:
        model = Address
        exclude = ['user']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'address_line_1': TextInput(attrs={'class': 'form-control'}),
            'address_line_2': TextInput(attrs={'class': 'form-control'}),
            'address_line_3': TextInput(attrs={'class': 'form-control'}),
            'city': TextInput(attrs={'class': 'form-control'}),
            'state': TextInput(attrs={'class': 'form-control'}),
            'country': TextInput(attrs={'class': 'form-control'}),
            'pincode': TextInput(attrs={'class': 'form-control'}),
            'is_default': CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_photo', 'name', 'age'] 

        