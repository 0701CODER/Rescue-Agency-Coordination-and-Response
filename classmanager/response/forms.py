from django import forms
from django.contrib.auth.forms import UserCreationForm
from response.models import User,Agency,Rescue,RescueMarks,MessageToAgency,ClassNotice,ClassAssignment,SubmitAssignment
from django.db import transaction
from .models import Location

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['latitude', 'longitude']

## User Login Form (Applied in both rescue and Agency login)
class UserForm(UserCreationForm):
    class Meta():
        model = User
        fields = ['username','password1','password2']
        widgets = {
                'username': forms.TextInput(attrs={'class':'answer'}),
                'password1': forms.PasswordInput(attrs={'class':'answer'}),
                'password2': forms.PasswordInput(attrs={'class':'answer'}),
                }
        
## Agency Registration Form 
class AgencyProfileForm(forms.ModelForm):
    class Meta():
        model =  Agency
        fields = ['name','subject_name','phone','email']
        widgets = {
                'name': forms.TextInput(attrs={'class':'answer'}),
                'subject_name': forms.TextInput(attrs={'class':'answer'}),
                'phone': forms.NumberInput(attrs={'class':'answer'}),
                'email': forms.EmailInput(attrs={'class':'answer'}),
                }

## Agency Profile Update Form
class AgencyProfileUpdateForm(forms.ModelForm):
    class Meta():
        model = Agency
        fields = ['name','subject_name','email','phone','agency_profile_pic']

## Rescue Registration Form
class RescueProfileForm(forms.ModelForm):
    class Meta():
        model =  Rescue
        fields = ['name','roll_no','phone','email']
        widgets = {
                'name': forms.TextInput(attrs={'class':'answer'}),
                'roll_no': forms.NumberInput(attrs={'class':'answer'}),
                'phone': forms.NumberInput(attrs={'class':'answer'}),
                'email': forms.EmailInput(attrs={'class':'answer'}),
                }

## Rescue profile update form
class RescueProfileUpdateForm(forms.ModelForm):
    class Meta():
        model = Rescue
        fields = ['name','roll_no','email','phone','rescue_profile_pic']
        
## Form for uploading marks and also for updating it.
class MarksForm(forms.ModelForm):
    class Meta():
        model = RescueMarks
        fields = ['subject_name','marks_obtained','maximum_marks']

## Writing message to agency        
class MessageForm(forms.ModelForm):
    class Meta():
        model = MessageToAgency
        fields = ['message']

## Writing notice in the class        
class NoticeForm(forms.ModelForm):
    class Meta():
        model = ClassNotice
        fields = ['message']

## Form for uploading or updating assignment (agencys only)       
class AssignmentForm(forms.ModelForm):
    class Meta():
        model = ClassAssignment
        fields = ['assignment_name','assignment']

## Form for submitting assignment (Rescues only)        
class SubmitForm(forms.ModelForm):
    class Meta():
        model = SubmitAssignment
        fields = ['submit']
