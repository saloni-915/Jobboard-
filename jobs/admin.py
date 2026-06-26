from django.contrib import admin
from .models import Company, Application, Job

# Register your models here.


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "created_at"]


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = ["title", "company", "is_approved", "created_at"]

    list_filter = ["is_approved", "job_type"]


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ["applicant", "job", "status", "applied_at"]
