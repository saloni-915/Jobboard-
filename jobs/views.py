from django.shortcuts import render, get_object_or_404, redirect
from .models import Job, Company, Application
from django.contrib.auth.decorators import login_required
from accounts.forms import CompanyForm
from .forms import JobForm, ApplicationForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from accounts.models import Notification


# Create your views here.
# ---------job list---------
def job_list(request):
    jobs = Job.objects.filter(is_approved=True).order_by("-created_at")

    # job list filtering
    job_type = request.GET.get(
        "job_type"
    )  # it will get request from browser in filter box
    location = request.GET.get("location")

    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if location:
        jobs = jobs.filter(location__icontains=location)

    # pagination
    paginator = Paginator(jobs, 5)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "jobs/job_list.html",
        {
            "jobs": page_obj,
            "page_obj": page_obj,
            "job_type": job_type,
            "location": location,
        },
    )


# -----------job detail----------
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)

    return render(request, "jobs/job_detail.html", {"job": job})


# -----------job create-------
@login_required
def job_create(request):

    if request.user.profile.role != "company":
        return redirect("job_list")

    try:
        company = request.user.company

    except:
        return redirect("company_create")
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = company
            job.save()
            Notification.objects.create(
                user=request.user, message="New Job Posted", notif_type="new_job"
            )
            messages.success(request, "Created successfully!")
            return redirect("job_list")
    else:
        form = JobForm()

    return render(request, "jobs/job_create.html", {"form": form})


@login_required
def my_posts(request):

    try:
        company = request.user.company
    except:
        return redirect("company_create")

    jobs = Job.objects.filter(company=company).prefetch_related("applications")

    return render(request, "jobs/my_posts.html", {"jobs": jobs})


@login_required
def company_create(request):
    if request.user.profile.role != "company":
        return redirect("job_list")

    if request.method == "POST":

        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            return redirect("job_create")

    else:
        form = CompanyForm()

    return render(request, "jobs/company_create.html", {"form": form})


@login_required
def job_apply(request, pk):

    job = get_object_or_404(Job, pk=pk)

    if request.user.profile.role != "candidate":
        return redirect("job_list")

    already_applied = Application.objects.filter(
        job=job, applicant=request.user
    ).exists()

    if already_applied:
        messages.warning(request, "Already applied for this job!")
        return redirect("job_detail", pk=pk)

    initial_data = {
        "full_name": request.user.username,
        "email": request.user.email,
        "phone": request.user.profile.phone,
        "bio": request.user.profile.bio,
    }

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()

            Notification.objects.create(
                user=job.company.owner,
                message=f"{request.user.username} applied for {job.title}",
                notif_type="new_application",
            )
            messages.success(request, "Applied successfully!")
            return redirect("my_applications")

    else:
        form = ApplicationForm(initial=initial_data)

    return render(request, "jobs/job_apply.html", {"job": job, "form": form})


def job_search(request):
    query = request.GET.get("q", "")

    if query:
        jobs = Job.objects.filter(is_approved=True).filter(
            Q(title__icontains=query)
            | Q(location__icontains=query)
            | Q(company__name__icontains=query)
        )
    else:
        jobs = Job.objects.filter(is_approved=True)

    return render(request, "jobs/job_cards.html", {"jobs": jobs})


@login_required
def application_update(request, pk):  # for application accept and reject

    application = get_object_or_404(Application, pk=pk)

    if application.job.company.owner != request.user:
        return redirect("job_list")

    status = request.POST.get("status", "").strip().lower()
    application.status = status
    application.save()
    if status == "accepted":
        Notification.objects.create(
            user=application.applicant,
            application=application,
            message=f"Congratulations! your {application.job.title} accepted",
            notif_type="status_changed",
        )
    elif status == "rejected":
        Notification.objects.create(
            user=application.applicant,
            application=application,
            message=f"Sorry! your {application.job.title} are rejected",
            notif_type="status_changed",
        )

    return redirect("my_posts")


@login_required
def job_update(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if job.company.owner != request.user:
        return redirect("job_list")

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)

        if form.is_valid():
            form.save()
            messages.success(request, "Updated")
            return redirect("my_posts")

    else:
        form = JobForm(instance=job)

    return render(request, "jobs/job_update.html", {"form": form, "job": job})


@login_required
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if job.company.owner != request.user:
        return redirect("my_posts")

    if request.method == "POST":
        job.delete()
        messages.success(request, "post deleted")
        return redirect("my_posts")

    return render(request, "jobs/job_delete.html", {"job": job})


@login_required
def notifications(request):
    notifs = Notification.objects.filter(user=request.user)
    unread_count = notifs.filter(is_read=False).count()

    notifs.filter(is_read=False).update(is_read=True)

    return render(
        request,
        "accounts/notifications.html",
        {"notifs": notifs, "unread_count": unread_count},
    )


from django.http import HttpResponse


def robots_txt(request):
    content = """User-agent:*

Disallow: /admin/
Disallow: /accounts/login/
Disallow: /accounts/register/
Disallow: /accounts/password-reset/
Allow: /

Sitemap: http://localhost:8000/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")
