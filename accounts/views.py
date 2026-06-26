from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm,ProfileUpdateForm,CompanyForm
from .models import UserProfile
from jobs.models import Application,Company,Job
from django.core .mail import send_mail
from .tasks import send_welcome_email

#-----------Register View---------
def register_view(request):
    if request.user.is_authenticated:
        return redirect('job_list')
    # Already logged in hai toh register page pe kyun aaye

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
              #login after register directly

            send_welcome_email.delay(user.username,user.email)

            messages.success(request,f'Welcome {user.username}! Account Created successfully!')

            return redirect('job_list')
        
    else:
        form = RegisterForm()


    return render(request,'accounts/register.html',{'form':form})


#--------login View----------------
def login_view(request):
    if request.user.is_authenticated: 
        return redirect('job_list') #means it checks that user logged in or not in session

    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username ,password=password)
        
        if user is not None:
            login(request,user)
            messages.success(request,f'Welcome back,{user.username}!')
            next_url = request.GET.get('next','job_list')
            return redirect(next_url)
        else:
            messages.error(request,'Invalid username or password!')

    return render(request,'accounts/login.html')

#-------logout view--------
def logout_view(request):
    logout(request)
    messages.info(request,'Logged out successfully!')
    return redirect('login')

#--------Profile View-------
@login_required
def profile_view(request):
    profile =   request.user.profile   

    skills = profile.skills.split(',')

    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST, #it contains text data of user
            request.FILES,
            instance=profile #don't create new profile update old profile

        )
        if form.is_valid():
            form.save()
            messages.success(request,'Profile updated!')
            return redirect('profile')
        
    else:
        form = ProfileUpdateForm(instance=profile) 

    if profile.role == 'candidate':
        template = 'accounts/candidate_profile.html'
    else:
        template = 'accounts/company_profile.html' 

    return render(request,template,{
        'form':form,
        'profile':profile,'skills':skills
    })    

#-------companyupddate------
@login_required
def CompanyProfile_view(request):
    
    try:
        company = request.user.company
    except:
        return redirect('company_create')  
    if request.method == 'POST':
        form = CompanyForm(
            request.POST, #it contains text data of user
            request.FILES,
            instance=company #don't create new profile update old profile

        )
        if form.is_valid():
            
            form.save()
            messages.success(request,'Profile updated!')
            return redirect('company_profile')
        
       
        
    else:
        form = CompanyForm(instance=company)

    company.total_jobs = company.jobs.count()   
    company.approved_jobs_count = company.jobs.filter(is_approved=True).count()
      

    

    return render(request,'accounts/company_profile.html' ,{
        'form':form,
        'company':company
    })    

        
@login_required
def my_applications(request):

    applications = Application.objects.filter(
        applicant = request.user
    ).order_by('-applied_at')

    return render(request,'accounts/my_applications.html',{
        'applications':applications
    })


@login_required
def application_detail(request,pk):
    
    application = get_object_or_404(Application,pk=pk)

    if application.job.company.owner != request.user:
        return redirect('my_applications')
    
    return render(request,'jobs/application_detail.html',{
        'application':application
    })


@login_required
def CompanyProfileUpdate_view(request):
    
    try:
        company = request.user.company
    except:
        return redirect('company_create')  
    if request.method == 'POST':
        form = CompanyForm(
            request.POST, #it contains text data of user
            request.FILES,
            instance=company #don't create new profile update old profile

        )
        if form.is_valid():
            
            form.save()
            messages.success(request,'Profile updated!')
            return redirect('company_profile')
        
       
        
    else:
        form = CompanyForm(instance=company)


    
    return render(request,'accounts/company_profile_update.html' ,{
        'form':form,
        'company':company
    })   



def company_profile_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)

    jobs = Job.objects.filter(
        company=company,is_approved=True
    ).order_by('-created_at')

    return render(
        request,
        'accounts/company_profile_detail.html',
        {
            'company': company,
            'jobs': jobs
        }
    )


#---------edit candidate profile------

#--------Profile View-------
@login_required
def profile_update(request):
    profile =   request.user.profile   

    skills = profile.skills.split(',')

    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST, #it contains text data of user
            request.FILES,
            instance=profile #don't create new profile update old profile

        )
        if form.is_valid():
            form.save()
            messages.success(request,'Profile updated!')
            return redirect('profile')
        
    else:
        form = ProfileUpdateForm(instance=profile) 

    if profile.role == 'candidate':
        template = 'accounts/candidate_profile_update.html'
   

    return render(request,template,{
        'form':form,
        'profile':profile,'skills':skills
    })    