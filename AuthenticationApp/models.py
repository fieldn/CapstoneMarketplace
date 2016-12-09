"""AuthenticationApp Models

Created by Naman Patwari on 10/4/2016.
"""

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.signals import post_save
from tinymce.models import HTMLField

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email=None, password=None, first_name=None, last_name=None, is_student=None, is_teacher=None, is_engineer=None):
        if not email:
            raise ValueError('Users must have an email address')

        #We can safely create the user; only the email field is required
        user = self.model(email=email)
        user.set_password(password)
        user.last_name = last_name
        user.is_student = is_student
        user.is_teacher = is_teacher
        user.is_engineer = is_engineer

        #If first_name is not present, set it as email's username by default
        if first_name is None or first_name == "" or first_name == '':                                
            user.first_name = email[:email.find("@")]            
        else:
            user.first_name = first_name

        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, first_name=None, last_name=None, is_student=None, is_teacher=None, is_engineer=None):
        user = self.create_user(email, password=password, first_name=first_name, last_name=last_name, is_student=True, is_teacher=True, is_engineer=True)
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    email = models.EmailField( verbose_name='email address', max_length=255, unique=True,) 
    first_name = models.CharField( max_length=120, null=True, blank=True,)    
    last_name = models.CharField( max_length=120, null=True, blank=True,)

    is_active = models.BooleanField(default=True,)
    is_admin = models.BooleanField(default=False,)
    is_student = models.BooleanField(default=False,)
    is_teacher = models.BooleanField(default=False,)
    is_engineer = models.BooleanField(default=False,)    

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # user can only select to be one of {student, teacher, engineer}
    # otherwise, just make them a student before saving in the database
    def save(self, *args, **kwargs):
        if self.is_student:
            self.is_teacher = self.is_engineer = False
        if self.is_teacher:
            self.is_student = self.is_engineer = False
        if self.is_engineer:
            self.is_student = self.is_teacher = False
        super(MyUser, self).save(*args, **kwargs)

    def get_full_name(self):        
        return "%s %s" %(self.first_name, self.last_name)

    def get_short_name(self):        
        return self.first_name

    def __str__(self):              #Python 3
        return self.email

    def __unicode__(self):           # Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):        
        return True

    @property
    def is_staff(self):
        return self.is_admin

#     def new_user_reciever(sender, instance, created, *args, **kwargs):
#       if created:   

# Going to use signals to send emails
# post_save.connect(new_user_reciever, sender=MyUser)


class Student(models.Model):
    user = models.OneToOneField( MyUser, on_delete=models.CASCADE, primary_key=True, related_name="student_info") 
    phone = models.CharField( max_length=11, null=True, blank=True,) 
    photo = models.ImageField(upload_to="static/userimages", default=0)
    about = HTMLField()
    
    # which languages you need to know
    c_lang = models.BooleanField(default=False)
    java_lang = models.BooleanField(default=False)
    python_lang = models.BooleanField(default=False)
    no_lang = models.BooleanField(default=True)

    # which specialties you have
    front_end_spec = models.BooleanField(default=False)
    back_end_spec = models.BooleanField(default=False)
    full_stack_spec = models.BooleanField(default=False)
    mobile_spec = models.BooleanField(default=False)
    no_spec = models.BooleanField(default=True)

    yrs_of_exp = models.IntegerField(default=0)

    def get_full_name(self):        
        return "%s %s" %(self.user.first_name, self.user.last_name)

    def get_short_name(self):        
        return self.user.first_name

    def __str__(self):              #Python 3
        return self.user.email

    def __unicode__(self):           # Python 2
        return self.user.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):        
        return True

    @property
    def is_staff(self):
        return False

class Teacher(models.Model):
    user = models.OneToOneField( MyUser, on_delete=models.CASCADE, primary_key=True) 
    phone = models.CharField( max_length=11, null=True, blank=True,) 
    photo = models.ImageField(upload_to="static/userimages", default=0, blank=True)
    about = HTMLField()

    title = models.CharField( max_length=32, null=True, blank=True,) 
    email = models.CharField( max_length=255, null=True, blank=True,) 
    office = models.CharField( max_length=32, null=True, blank=True,) 

    def get_full_name(self):        
        return "%s %s" %(self.user.first_name, self.user.last_name)

    def get_short_name(self):        
        return self.user.first_name

    def __str__(self):              #Python 3
        return self.user.email

    def __unicode__(self):           # Python 2
        return self.user.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):        
        return True


    @property
    def is_staff(self):
        return False

class Engineer(models.Model):
    user = models.OneToOneField( MyUser, on_delete=models.CASCADE, primary_key=True) 
    phone = models.CharField( max_length=11, null=True, blank=True,) 
    photo = models.ImageField(upload_to="static/userimages", default=0)
    about = HTMLField()

    title = models.CharField( max_length=32, null=True, blank=True,) 
    email = models.CharField( max_length=255, null=True, blank=True,) 
    almaMater = models.CharField( max_length=32, null=True, blank=True,)

    def get_full_name(self):        
        return "%s %s" %(self.user.first_name, self.user.last_name)

    def get_short_name(self):        
        return self.user.first_name

    def __str__(self):              #Python 3
        return self.user.email

    def __unicode__(self):           # Python 2
        return self.user.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):        
        return True

    @property
    def is_staff(self):
        return False
