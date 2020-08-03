from django.db import models
from datetime import datetime
import bcrypt

class PostManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['post_content']) < 2:
            errors["post_content"] = "Post content should be at least 2 characters"
        return errors

class Post(models.Model):
    post_content = models.CharField(max_length=255)
    created_on = models.DateField(auto_now_add=True)
    objects = PostManager()

class UsersManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be atleast 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "Passowrds do not match"
        if len(postData['email']) <1:
            errors["email"] = "Email address cannot be blank"
        return errors

    def login_validator(self, postData):
        errors = {}
        check = User.objects.filter(email=postData['login_email'])
        if not check:
            errors['login_email'] = "Email has not been registered"
        else:
            if not bcrypt.checkpw(postData['login_password'].encode(), check[0].password):
                errors['login_email'] = 'Email and password do not match'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)

    objects = UsersManager()