from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# -----------Company-----------
class Company(models.Model):

    COMPANY_SIZE_CHOICES = [
        ("1-10", "1-10"),
        ("11-50", "11-50"),
        ("51-200", "51-200"),
        ("201-500", "201-500"),
        ("500+", "500+"),
    ]

    INDUSTRY_CHOICES = [
        ("technology", "Technology"),
        ("finance", "Finance"),
        ("healthcare", "Healthcare"),
        ("education", "Education"),
        ("ecommerce", "E-Commerce"),
        ("manufacturing", "Manufacturing"),
        ("consulting", "Consulting"),
        ("other", "Other"),
    ]
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company")

    name = models.CharField(max_length=200)

    logo = models.ImageField(upload_to="logos/", blank=True, null=True)

    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    location = models.TextField(blank=True)
    company_size = models.CharField(
        max_length=20, choices=COMPANY_SIZE_CHOICES, blank=True
    )
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES, blank=True)
    founded_year = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class Job(models.Model):
    Job_type_choice = [
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("contract", "Contract"),
        ("internship", "Internship"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    job_type = models.CharField(
        max_length=20, choices=Job_type_choice, default="full_time"
    )
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} at {self.company.name}"

    # Application------model


class Application(models.Model):

    status_choices = [
        ("pending", "Pending"),
        ("reviewed", "Reviewed"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="applications"
    )
    full_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)

    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to="resumes/", null=True)
    status = models.CharField(max_length=20, choices=status_choices, default="pending")

    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["job", "applicant"]

    def __str__(self):
        return f"{self.applicant.username} -> {self.job.title}"
