from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
import re
from .models import Creator,usermodel as um,loginmodel,CreatorHomepage,CreatorBid,Auction, payment, UserComplaint, ArtistComplaint
# forms.py

class CreatorRegistrationForm(forms.ModelForm):
    Gender_choice = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('0', 'Others')
    )
    Gender = forms.ChoiceField(choices=Gender_choice, widget=forms.RadioSelect())

    class Meta:
        model = Creator
        fields = ['Name', 'Gender', 'DOB', 'ContactNo', 'Email', 'Password']
        widgets = {
            'DOB': forms.DateInput(attrs={'type': 'date'}),
            'Gender': forms.RadioSelect(),
        }

    def clean_Email(self):
        email = self.cleaned_data.get('Email')
        if Creator.objects.filter(Email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_ContactNo(self):
        contact_no = self.cleaned_data.get('ContactNo')
        if len(str(contact_no)) != 10:
            raise forms.ValidationError("Contact number must be 10 digits.")
        return contact_no

    def clean(self):
        cleaned_data = super().clean()
        dob = cleaned_data.get('DOB')
        # Custom validation logic if needed
        if dob and dob.year > 2010:
            raise forms.ValidationError("DOB must indicate an age above 14.")
        return cleaned_data
  
class UserRegistrationForm(forms.ModelForm):
    Gender_choice = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('0', 'Others')
    )
    Gender = forms.ChoiceField(choices=Gender_choice, widget=forms.RadioSelect())

    class Meta:
        model = um  # Replace with the actual model name
        fields = ['Name', 'Gender', 'DOB', 'Adress', 'ContactNo', 'Email', 'Password']
        widgets = {
            'DOB': forms.DateInput(attrs={'type': 'date'}),
            'Gender': forms.RadioSelect(),
        }

    def clean_Name(self):
        name = self.cleaned_data.get('Name')
        if not re.match(r'^[a-zA-Z\s]+$', name):
            raise ValidationError('Name can only contain letters and spaces.')
        return name

    def clean_DOB(self):
        dob = self.cleaned_data.get('DOB')
        if dob > timezone.now().date():
            raise ValidationError('Date of Birth cannot be in the future.')
        return dob

    # def clean_ContactNo(self):
    #     contact_no = self.cleaned_data.get('ContactNo')
    #     if not re.match(r'^\d{10}$', contact_no):
    #         raise ValidationError('Contact number must be a 10-digit number.')
    #     return contact_no
    def clean_ContactNo(self):
        contact_no = self.cleaned_data.get('ContactNo')
        contact_no_str = str(contact_no)  # Convert to string
        if not re.match(r'^\d{10}$', contact_no_str):
            raise ValidationError('Contact number must be a 10-digit number.')
        return contact_no


    def clean_Email(self):
        email = self.cleaned_data.get('Email')
        # Additional email validation logic can go here
        return email

    def clean_Password(self):
        password = self.cleaned_data.get('Password')
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        if not any(char.isupper() for char in password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not any(char.islower() for char in password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain at least one digit.')
        if not any(char in '!@#$%^&*(),.?":{}|<>' for char in password):
            raise ValidationError('Password must contain at least one special character.')
        return password
class loginform(forms.ModelForm):
    
    class Meta:
       model= loginmodel
       fields=['Email','Password']

class CreatorHomepageForm(forms.ModelForm):
    class Meta:
       model=CreatorHomepage
       fields=['ArtCatogory','Image','Amount','ArtDetails']
       widgets={
            'Image':forms.FileInput()
            
                } 
class CreatorBidForm(forms.ModelForm):
    class Meta:
       model=CreatorBid
       fields=['Bidstartdate','Bidstarttime','Bidendtime']

       widgets={
            'Bidstartdate':forms.DateInput(attrs={'type':'date'}),
            'Bidstarttime':forms.TimeInput(attrs={'type':'time'}),
            'Bidendtime':forms.TimeInput(attrs={'type':'time'}),

            
                }       
class AuctionForm(forms.ModelForm):
    class Meta:
        model=Auction
        fields=['Amount']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = payment
        fields = ['Cardno', 'nameoncard', 'expiredate', 'cvv']
        widgets = {
            'Cardno': forms.TextInput(attrs={'placeholder': 'Card Number', 'class': 'form-control'}),
            'nameoncard': forms.TextInput(attrs={'placeholder': 'Name on Card', 'class': 'form-control'}),
            'expiredate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cvv': forms.TextInput(attrs={'placeholder': 'CVV', 'class': 'form-control'}),
        }

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = UserComplaint
        fields = ['subject','complaint']   
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'Enter your subject...', 'class': 'form-control'}),
            'complaint': forms.TextInput(attrs={'placeholder': 'Enter your complaint...', 'class': 'form-control'}),
        }

class ReplayForm(forms.ModelForm):
    class Meta:
        model=UserComplaint
        fields=['reply'] 
        widgets = {
            'reply': forms.TextInput(attrs={'class': 'form-control'}),
        }    


class ArtistComplaintForm(forms.ModelForm):
    class Meta:
        model = ArtistComplaint
        fields = ['subject','complaint']   
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'Enter your subject...', 'class': 'form-control'}),
            'complaint': forms.TextInput(attrs={'placeholder': 'Enter your complaint...', 'class': 'form-control'}),
        }

class ArtistReplayForm(forms.ModelForm):
    class Meta:
        model=ArtistComplaint
        fields=['reply'] 
        widgets = {
            'reply': forms.TextInput(attrs={'class': 'form-control'}),
        }    
       
            
class PasswordResetRequestForm(forms.Form):
    Email = forms.EmailField(label="Enter your email", max_length=254)

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(label="Enter the OTP sent to your email", max_length=6)

class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    

                             

