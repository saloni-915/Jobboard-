from django.urls import path

from accounts.views import application_detail

from . import views

urlpatterns = [
    path("", views.job_list, name="job_list"),
    path("job/<int:pk>/", views.job_detail, name="job_detail"),
    path("job/create/", views.job_create, name="job_create"),
    path("my-posts/", views.my_posts, name="my_posts"),
    path("company/create/", views.company_create, name="company_create"),
    path("job/<int:pk>/apply/", views.job_apply, name="job_apply"),
    path("jobs/search/", views.job_search, name="job_search"),
    path(
        "application/<int:pk>/update/",
        views.application_update,
        name="application_update",
    ),
    path("jobs/<int:pk>/update/", views.job_update, name="job_update"),
    path("jobs/<int:pk>/delete/", views.job_delete, name="job_delete"),
    path("application-detail/<int:pk>/", application_detail, name="application_detail"),
    path("notifications/", views.notifications, name="notifications"),
]
