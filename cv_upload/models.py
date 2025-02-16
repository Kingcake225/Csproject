from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}: {self.subject}"

class CV(models.Model):
    POSITION_CHOICES = [
        ('SE', 'Software Engineer'),
        ('HR', 'Human Resources'),
        ('CSR', 'Client Service Representative'),
        ('SMM', 'Social Media Manager'),
        ('CA', 'Compliance Analyst'),
    ]
    
    EDUCATION_CHOICES = [
        ('PHD', 'PhD'),
        ('MASTERS', 'Masters'),
        ('UNDERGRAD', 'Undergraduate'),
        ('ALEVELS', 'A Levels'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    position = models.CharField(max_length=3, choices=POSITION_CHOICES)
    education_level = models.CharField(max_length=10, choices=EDUCATION_CHOICES)
    education_discipline = models.CharField(max_length=100, default='None')
    personal_statement = models.TextField(blank=True, null=True)
    custom_message = models.TextField(blank=True, null=True)
    pdf_file = models.FileField(upload_to='cvs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    rating = models.IntegerField(null=True, blank=True)
    admin_notes = models.TextField(blank=True, null=True)

    # Structured data fields
    structured_data = models.JSONField(null=True, blank=True)
    skills_score = models.FloatField(null=True, blank=True)
    education_score = models.FloatField(null=True, blank=True)
    experience_score = models.FloatField(null=True, blank=True)
    overall_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}'s CV - {self.status}"

    def update_ranking(self):
        """Update ranking scores based on structured data"""
        if self.structured_data:
            from cv_upload.ranking_utils import rank_candidate
            scores = rank_candidate(self.structured_data, self.position)
            self.overall_score = scores.get('total_score', 0)
            self.skills_score = scores.get('skills_score', 0)
            self.education_score = scores.get('education_score', 0)
            self.experience_score = scores.get('experience_score', 0)
            self.save()
