from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model): # Each class is its own table in the database
    title = models.CharField(max_length=100) # Each attributes of the class are different fields
    content = models.TextField() # Text field is for longer, unrestricted text, unlike Char field
    date_posted = models.DateTimeField(default=timezone.now) # No parenthesis after .now() because don't want to execute at this moment, just want to call upon it.
    author = models.ForeignKey(User, on_delete=models.CASCADE) # on_delete=models.CASCADE - deletes users post if user is deleted.

    def __str__(self):
        return self.title