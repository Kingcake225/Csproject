from django.db import models
from django.contrib.auth.models import User

# Extended User Model

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Creates one-to-one relationship between this model and the default user model, on deleting of user delete the profile, but don't delete the user if profile deleted.
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'