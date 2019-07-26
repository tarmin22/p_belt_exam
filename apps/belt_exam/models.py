from __future__ import unicode_literals
from django.db import models
import bcrypt, re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'([A-Za-z]+[0-9]|[0-9]+[A-Za-z])[A-Za-z0-9]*')




class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors ={}

        check_email = User.objects.filter(email = postData['femail'])

        if (len(postData['f_name']) <2) or (not(NAME_REGEX.match(postData['f_name']))):
            errors['f_name'] = "First name must contain at least two letters and contain letters only"

        if (len(postData['l_name']) <2) or (not(NAME_REGEX.match(postData['f_name']))):
            errors['l_name'] = 'Last name must contain at least two letter and contain letters only'

        if not EMAIL_REGEX.match(postData['femail']):
            errors['femail'] = "Invalid email format"

        if len(check_email) > 0:
            errors['email1']='Email already exists'

        if (len(postData['f_pw']) < 8) or (not(PASSWORD_REGEX.match(postData['f_pw']))):
            errors['f_pw_b']="Must have at least one upper case and one number in password and at least 8 characters"

        if postData['f_pw'] != postData['c_pw']:
            errors['f_pw_c']= "Password must match"

        return errors

    def user_validator(self, postData):
        errors ={}

        user = User.objects.filter(email = postData['log_email'])

        if not EMAIL_REGEX.match(postData['log_email']):
            errors['log_email'] = "Invalid email format"

        if len(user) < 1:
            errors['email1']='cannnot log you in, cannot find email address'

        if len(user) > 0:
            if (len(postData['log_pw']) < 8) or (not(PASSWORD_REGEX.match(postData['log_pw']))):
                errors['f_pw_a']="Must have at least one upper case and one number in password and at least 8 characters"

            if not (bcrypt.checkpw(postData['log_pw'].encode(), user[0].password.encode())):
                errors['f_pw_b']= "Invalid password entered. Cannot log you in!"

        return errors



class User (models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email =models.CharField(max_length=45)
    password =models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Org (models.Model):
    name = models.CharField(max_length=45)
    desc = models.TextField()
    created_by = models.ForeignKey(User, related_name="created_org")
    joined_by = models.ManyToManyField(User, related_name = "joined_org")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

