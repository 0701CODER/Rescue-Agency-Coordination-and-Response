from django.shortcuts import render,get_object_or_404,redirect
from django.views import generic
from django.views.generic import  (View,TemplateView,
                                  ListView,DetailView,
                                  CreateView,UpdateView,
                                  DeleteView)
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from response.forms import UserForm,AgencyProfileForm,RescueProfileForm,MarksForm,MessageForm,NoticeForm,AssignmentForm,SubmitForm,AgencyProfileUpdateForm,RescueProfileUpdateForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.http import HttpResponseRedirect,HttpResponse
from response import models
from response.models import RescuesInClass,RescueMarks,ClassAssignment,SubmitAssignment,Rescue,Agency
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import LocationForm

def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('response:success_url')  # Redirect to the success page
    else:
        form = LocationForm()
    return render(request, 'response/location_form.html', {'form': form})

def success_view(request):
    return render(request, 'response/success.html')

# For Agency Sign Up
def AgencySignUp(request):
    user_type = 'agency'
    registered = False

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        agency_profile_form = AgencyProfileForm(data = request.POST)

        if user_form.is_valid() and agency_profile_form.is_valid():

            user = user_form.save()
            user.is_agency = True
            user.save()

            profile = agency_profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors,agency_profile_form.errors)
    else:
        user_form = UserForm()
        agency_profile_form = AgencyProfileForm()

    return render(request,'response/agency_signup.html',{'user_form':user_form,'agency_profile_form':agency_profile_form,'registered':registered,'user_type':user_type})


###  For rescue Sign Up
def RescueSignUp(request):
    user_type = 'rescue'
    registered = False

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        rescue_profile_form = RescueProfileForm(data = request.POST)

        if user_form.is_valid() and rescue_profile_form.is_valid():

            user = user_form.save()
            user.is_rescue = True
            user.save()

            profile = rescue_profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors,rescue_profile_form.errors)
    else:
        user_form = UserForm()
        rescue_profile_form = RescueProfileForm()

    return render(request,'response/rescue_signup.html',{'user_form':user_form,'rescue_profile_form':rescue_profile_form,'registered':registered,'user_type':user_type})

## Sign Up page which will ask whether you are agency or rescue.
def SignUp(request):
    return render(request,'response/signup.html',{})

## login view.
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))

            else:
                return HttpResponse("Account not active")

        else:
            messages.error(request, "Invalid Details")
            return redirect('response:login')
    else:
        return render(request,'response/login.html',{})

## logout view.
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

## User Profile of rescue.
class RescueDetailView(LoginRequiredMixin,DetailView):
    context_object_name = "rescue"
    model = models.Rescue
    template_name = 'response/rescue_detail_page.html'

## User Profile for agency.
class AgencyDetailView(LoginRequiredMixin,DetailView):
    context_object_name = "agency"
    model = models.Agency
    template_name = 'response/agency_detail_page.html'

## Profile update for rescues.
@login_required
def RescueUpdateView(request,pk):
    profile_updated = False
    rescue = get_object_or_404(models.Rescue,pk=pk)
    if request.method == "POST":
        form = RescueProfileUpdateForm(request.POST,instance=rescue)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'rescue_profile_pic' in request.FILES:
                profile.rescue_profile_pic = request.FILES['rescue_profile_pic']
            profile.save()
            profile_updated = True
    else:
        form = RescueProfileUpdateForm(request.POST or None,instance=rescue)
    return render(request,'response/rescue_update_page.html',{'profile_updated':profile_updated,'form':form})

## Profile update for agencys.
@login_required
def AgencyUpdateView(request,pk):
    profile_updated = False
    agency = get_object_or_404(models.Agency,pk=pk)
    if request.method == "POST":
        form = AgencyProfileUpdateForm(request.POST,instance=agency)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'agency_profile_pic' in request.FILES:
                profile.agency_profile_pic = request.FILES['agency_profile_pic']
            profile.save()
            profile_updated = True
    else:
        form = AgencyProfileUpdateForm(request.POST or None,instance=agency)
    return render(request,'response/agency_update_page.html',{'profile_updated':profile_updated,'form':form})

## List of all rescues that agency has added in their class.
def class_rescues_list(request):
    query = request.GET.get("q", None)
    rescues = RescuesInClass.objects.filter(agency=request.user.Agency)
    rescues_list = [x.rescue for x in rescues]
    qs = Rescue.objects.all()
    if query is not None:
        qs = qs.filter(
                Q(name__icontains=query)
                )
    qs_one = []
    for x in qs:
        if x in rescues_list:
            qs_one.append(x)
        else:
            pass
    context = {
        "class_rescues_list": qs_one,
    }
    template = "response/class_rescues_list.html"
    return render(request, template, context)

class ClassRescuesListView(LoginRequiredMixin,DetailView):
    model = models.Agency
    template_name = "response/class_rescues_list.html"
    context_object_name = "agency"

## For Marks obtained by the rescue in all subjects.
class RescueAllMarksList(LoginRequiredMixin,DetailView):
    model = models.Rescue
    template_name = "response/rescue_allmarks_list.html"
    context_object_name = "rescue"

## To give marks to a rescue.
@login_required
def add_marks(request,pk):
    marks_given = False
    rescue = get_object_or_404(models.Rescue,pk=pk)
    if request.method == "POST":
        form = MarksForm(request.POST)
        if form.is_valid():
            marks = form.save(commit=False)
            marks.rescue = rescue
            marks.agency = request.user.Agency
            marks.save()
            messages.success(request,'Marks uploaded successfully!')
            return redirect('response:submit_list')
    else:
        form = MarksForm()
    return render(request,'response/add_marks.html',{'form':form,'rescue':rescue,'marks_given':marks_given})

## For updating marks.
@login_required
def update_marks(request,pk):
    marks_updated = False
    obj = get_object_or_404(RescueMarks,pk=pk)
    if request.method == "POST":
        form = MarksForm(request.POST,instance=obj)
        if form.is_valid():
            marks = form.save(commit=False)
            marks.save()
            marks_updated = True
    else:
        form = MarksForm(request.POST or None,instance=obj)
    return render(request,'response/update_marks.html',{'form':form,'marks_updated':marks_updated})

## For writing notice which will be sent to all class rescues.
@login_required
def add_notice(request):
    notice_sent = False
    agency = request.user.Agency
    rescues = RescuesInClass.objects.filter(agency=agency)
    rescues_list = [x.rescue for x in rescues]

    if request.method == "POST":
        notice = NoticeForm(request.POST)
        if notice.is_valid():
            object = notice.save(commit=False)
            object.agency = agency
            object.save()
            object.rescues.add(*rescues_list)
            notice_sent = True
    else:
        notice = NoticeForm()
    return render(request,'response/write_notice.html',{'notice':notice,'notice_sent':notice_sent})

## For rescue writing message to agency.
@login_required
def write_message(request,pk):
    message_sent = False
    agency = get_object_or_404(models.Agency,pk=pk)

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            mssg = form.save(commit=False)
            mssg.agency = agency
            mssg.rescue = request.user.Rescue
            mssg.save()
            message_sent = True
    else:
        form = MessageForm()
    return render(request,'response/write_message.html',{'form':form,'agency':agency,'message_sent':message_sent})

## For the list of all the messages agency have received.
@login_required
def messages_list(request,pk):
    agency = get_object_or_404(models.Agency,pk=pk)
    return render(request,'response/messages_list.html',{'agency':agency})

## rescue can see all notice given by their agency.
@login_required
def class_notice(request,pk):
    rescue = get_object_or_404(models.Rescue,pk=pk)
    return render(request,'response/class_notice_list.html',{'rescue':rescue})

## To see the list of all the marks given by the agency to a specific rescue.
@login_required
def rescue_marks_list(request,pk):
    error = True
    rescue = get_object_or_404(models.Rescue,pk=pk)
    agency = request.user.Agency
    given_marks = RescueMarks.objects.filter(agency=agency,rescue=rescue)
    return render(request,'response/rescue_marks_list.html',{'rescue':rescue,'given_marks':given_marks})

## To add rescue in the class.
class add_rescue(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('response:rescues_list')

    def get(self,request,*args,**kwargs):
        rescue = get_object_or_404(models.Rescue,pk=self.kwargs.get('pk'))

        try:
            RescuesInClass.objects.create(agency=self.request.user.Agency,rescue=rescue)
        except:
            messages.warning(self.request,'warning, rescue already in class!')
        else:
            messages.success(self.request,'{} successfully added!'.format(rescue.name))

        return super().get(request,*args,**kwargs)

@login_required
def rescue_added(request):
    return render(request,'response/rescue_added.html',{})

## List of rescues which are not added by agency in their class.
def rescues_list(request):
    query = request.GET.get("q", None)
    rescues = RescuesInClass.objects.filter(agency=request.user.Agency)
    rescues_list = [x.rescue for x in rescues]
    qs = Rescue.objects.all()
    if query is not None:
        qs = qs.filter(
                Q(name__icontains=query)
                )
    qs_one = []
    for x in qs:
        if x in rescues_list:
            pass
        else:
            qs_one.append(x)

    context = {
        "rescues_list": qs_one,
    }
    template = "response/rescues_list.html"
    return render(request, template, context)

## List of all the agency present in the portal.
def agencys_list(request):
    query = request.GET.get("q", None)
    qs = Agency.objects.all()
    if query is not None:
        qs = qs.filter(
                Q(name__icontains=query)
                )

    context = {
        "agencys_list": qs,
    }
    template = "response/agencys_list.html"
    return render(request, template, context)


####################################################

## Agency uploading assignment.
@login_required
def upload_assignment(request):
    assignment_uploaded = False
    agency = request.user.Agency
    rescues = Rescue.objects.filter(user_rescue_name__agency=request.user.Agency)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.agency = agency
            rescues = Rescue.objects.filter(user_rescue_name__agency=request.user.Agency)
            upload.save()
            upload.rescue.add(*rescues)
            assignment_uploaded = True
    else:
        form = AssignmentForm()
    return render(request,'response/upload_assignment.html',{'form':form,'assignment_uploaded':assignment_uploaded})

## Rescues getting the list of all the assignments uploaded by their agency.
@login_required
def class_assignment(request):
    rescue = request.user.Rescue
    assignment = SubmitAssignment.objects.filter(rescue=rescue)
    assignment_list = [x.submitted_assignment for x in assignment]
    return render(request,'response/class_assignment.html',{'rescue':rescue,'assignment_list':assignment_list})

## List of all the assignments uploaded by the agency himself.
@login_required
def assignment_list(request):
    agency = request.user.Agency
    return render(request,'response/assignment_list.html',{'agency':agency})

## For updating the assignments later.
@login_required
def update_assignment(request,id=None):
    obj = get_object_or_404(ClassAssignment, id=id)
    form = AssignmentForm(request.POST or None, instance=obj)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        if 'assignment' in request.FILES:
            obj.assignment = request.FILES['assignment']
        obj.save()
        messages.success(request, "Updated Assignment".format(obj.assignment_name))
        return redirect('response:assignment_list')
    template = "response/update_assignment.html"
    return render(request, template, context)

## For deleting the assignment.
@login_required
def assignment_delete(request, id=None):
    obj = get_object_or_404(ClassAssignment, id=id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Assignment Removed")
        return redirect('response:assignment_list')
    context = {
        "object": obj,
    }
    template = "response/assignment_delete.html"
    return render(request, template, context)

## For rescues submitting their assignment.
@login_required
def submit_assignment(request, id=None):
    rescue = request.user.Rescue
    assignment = get_object_or_404(ClassAssignment, id=id)
    agency = assignment.agency
    if request.method == 'POST':
        form = SubmitForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.agency = agency
            upload.rescue = rescue
            upload.submitted_assignment = assignment
            upload.save()
            return redirect('response:class_assignment')
    else:
        form = SubmitForm()
    return render(request,'response/submit_assignment.html',{'form':form,})

## To see all the submissions done by the rescues.
@login_required
def submit_list(request):
    agency = request.user.Agency
    return render(request,'response/submit_list.html',{'agency':agency})

##################################################################################################

## For changing password.
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST , user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password changed")
            return redirect('home')
        else:
            return redirect('response:change_password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request,'response/change_password.html',args)

