"""AuthenticationApp Forms

Created by Naman Patwari on 10/4/2016.
"""
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import MyUser, Student, Teacher, Engineer
from tinymce.widgets import TinyMCE

class LoginForm(forms.Form):
    email = forms.CharField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class RegisterStudentForm(forms.Form):
    email = forms.CharField(label='Email', widget=forms.EmailInput, required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=True)    

    firstname = forms.CharField(label="First name", widget=forms.TextInput, required=False)
    lastname = forms.CharField(label="Last name", widget=forms.TextInput, required=False)               
    studentPhone =  forms.CharField(label="Phone", widget=forms.TextInput, required=False)
    #studentAbout = forms.CharField(label="About", widget=forms.TextInput, required=False)               
    studentAbout = forms.CharField(label="About", widget=TinyMCE(attrs={'cols': 20, 'rows':5}), required=False)               
    # which languages you need to know
    c_lang = forms.BooleanField(label='C', widget=forms.CheckboxInput, required=False)
    java_lang = forms.BooleanField(label='Java', widget=forms.CheckboxInput, required=False)
    python_lang = forms.BooleanField(label='Python', widget=forms.CheckboxInput, required=False)
    no_lang = forms.BooleanField(label='None', widget=forms.CheckboxInput, required=False)

    # which specialties you have
    front_end_spec = forms.BooleanField(label='Front end', widget=forms.CheckboxInput, required=False)
    back_end_spec = forms.BooleanField(label='Back end', widget=forms.CheckboxInput, required=False)
    full_stack_spec = forms.BooleanField(label='Full Stack', widget=forms.CheckboxInput, required=False)
    mobile_spec = forms.BooleanField(label='Mobile', widget=forms.CheckboxInput, required=False)
    no_spec = forms.BooleanField(label='None', widget=forms.CheckboxInput, required=False)

    yrs_of_exp = forms.IntegerField(label='Experience', required=False)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        #Check if email exists before
        try:
            exists = MyUser.objects.get(email=email)
            raise forms.ValidationError("This email has already been taken")
        except MyUser.DoesNotExist:
            return email
        except:
            raise forms.ValidationError("There was an error, please contact us later")
    
class RegisterTeacherForm(forms.Form):
    teacherTitle = forms.CharField(label="Title", widget=forms.TextInput, required=False)               
    teacherPhone =  forms.CharField(label="Phone", widget=forms.TextInput, required=False)
    teacherEmail =  forms.CharField(label="Email", widget=forms.TextInput, required=False)
    teacherOffice = forms.CharField(label="Office", widget=forms.TextInput, required=False)
    teacherAbout = forms.CharField(label="About", widget=TinyMCE(attrs={'cols': 20, 'rows':5}), required=False)               

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        #Check if email exists before
        try:
            exists = MyUser.objects.get(email=email)
            raise forms.ValidationError("This email has already been taken")
        except MyUser.DoesNotExist:
            return email
        except:
            raise forms.ValidationError("There was an error, please contact us later")

class RegisterEngineerForm(forms.Form):
    engineerTitle = forms.CharField(label="Title", widget=forms.TextInput, required=False)               
    engineerAlmaMater = forms.CharField(label="Alma Mater", widget=forms.TextInput, required=False)               
    engineerPhone =  forms.CharField(label="Phone", widget=forms.TextInput, required=False)
    engineerEmail =  forms.CharField(label="Email", widget=forms.TextInput, required=False)
    engineerAbout = forms.CharField(label="About", widget=TinyMCE(attrs={'cols': 20, 'rows':5}), required=False)               

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        #Check if email exists before
        try:
            exists = MyUser.objects.get(email=email)
            raise forms.ValidationError("This email has already been taken")
        except MyUser.DoesNotExist:
            return email
        except:
            raise forms.ValidationError("There was an error, please contact us later")

class UpdateForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'first_name', 'last_name')

    def clean_password(self):            
        return self.initial["password"]        

    def clean_email(self):
        email = self.cleaned_data.get("email")
        #Check is email has changed
        if email == self.initial["email"]:
            return email
        #Check if email exists before
        try:
            exists = MyUser.objects.get(email=email)
            raise forms.ValidationError("This email has already been taken")
        except MyUser.DoesNotExist:
            return email
        except:
            raise forms.ValidationError("There was an error, please contact us later")

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        #Check is email has changed
        if first_name is None or first_name == "" or first_name == '':  
            email = self.cleaned_data.get("email")                               
            return email[:email.find("@")]      
        return first_name

class UpdateStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('about', 'phone', 'c_lang', 'java_lang', 'python_lang', 'no_lang', 'front_end_spec', 'back_end_spec', 'full_stack_spec', 'mobile_spec', 'no_spec', 'yrs_of_exp')

    def clean_about(self):
        return self.cleaned_data.get("about")

    def clean_phone(self):
        return self.cleaned_data.get("phone")

class UpdateTeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('about', 'phone', 'title', 'office')

    def clean_about(self):
        return self.cleaned_data.get("about")

    def clean_phone(self):
        return self.cleaned_data.get("phone")
   
    def clean_title(self):
        return self.cleaned_data.get("title")

    def clean_office(self):
        return self.cleaned_data.get("office")

class UpdateEngineerForm(forms.ModelForm):
    class Meta:
        model = Engineer
        fields = ('about', 'phone', 'title', 'almaMater')

    def clean_about(self):
        return self.cleaned_data.get("about")

    def clean_phone(self):
        return self.cleaned_data.get("phone")

    def clean_title(self):
        return self.cleaned_data.get("title")

    def clean_almaMater(self):
        return self.cleaned_data.get("almaMater")


"""Admin Forms"""

class AdminUserCreationForm(forms.ModelForm):
    """A form for Admin to creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(AdminUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for Admin for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'first_name', 'last_name', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]        
