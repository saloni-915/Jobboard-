from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/update/", views.profile_update, name="profile_update"),
    path("my-applications/", views.my_applications, name="my_applications"),
    path("application-detail/", views.application_detail, name="application_detail"),
    path("company-profile/", views.CompanyProfile_view, name="company_profile"),
    path(
        "company-profile/update-profile/",
        views.CompanyProfileUpdate_view,
        name="company_update_profile",
    ),
    path(
        "company/<int:pk>/", views.company_profile_detail, name="company_profile_detail"
    ),
]
