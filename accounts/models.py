from django.contrib.auth.models import User
from django.db import models

from jobs.models import Application


# Create your models here.
class UserProfile(models.Model):
    role_choices = [
        ("candidate", "Candidate"),
        ("company", "Company"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    role = models.CharField(max_length=100, choices=role_choices, default="candidate")
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)

    skills = models.CharField(max_length=500, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    experience = models.IntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.role}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("new_application", "New Applications"),
        ("status_changed", "Status Changed"),
        ("new_job", "New Job Posted"),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )

    message = models.TextField()

    is_read = models.BooleanField(default=False)
    notif_type = models.CharField(
        max_length=50, choices=NOTIFICATION_TYPES, default="new_application"
    )
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} -> {self.message[:30]}"
