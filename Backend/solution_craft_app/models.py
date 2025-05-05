from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLES = (
        ('Admin', 'Admin'),
        ('Support Agent', 'Support Agent'),
        ('Customer', 'Customer')
    )

    STATUS = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive')
    )

    role = models.CharField(max_length=50, choices=ROLES, default='Support Agent')
    status = models.CharField(max_length=50, choices=STATUS, default='Active')
    profile_picture = models.CharField(max_length=255, null=True, blank=True)
    permissions = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved')
    ]
    
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical')
    ]
    
    title = models.CharField(max_length=255, default="Default Title")
    customer_name = models.CharField(max_length=255)
    email = models.EmailField()
    issue_description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Open')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='Medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(
        "solution_craft_app.CustomUser", 
        related_name='assigned_tickets', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL
    )
    resolved_by = models.ForeignKey(
        "solution_craft_app.CustomUser", 
        related_name='resolved_tickets', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL
    )
    resolved_at = models.DateTimeField(null=True, blank=True)
    customer_satisfaction_rating = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title
