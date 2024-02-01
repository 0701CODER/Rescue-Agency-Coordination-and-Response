from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings
import misaka


# Create your models here.
class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"Latitude: {self.latitude}, Longitude: {self.longitude}"
    
class User(AbstractUser):
    is_rescue = models.BooleanField(default=False)
    is_agency = models.BooleanField(default=False)


class Rescue(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='Rescue')
    name=models.CharField(max_length=250)
    roll_no = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()
    rescue_profile_pic = models.ImageField(upload_to="response/rescue_profile_pic",blank=True)

    def get_absolute_url(self):
        return reverse('response:rescue_detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['roll_no']

class Agency(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='Agency')
    name = models.CharField(max_length=250)
    subject_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()
    agency_profile_pic = models.ImageField(upload_to="response/agency_profile_pic",blank=True)
    class_rescues = models.ManyToManyField(Rescue,through="RescuesInClass")

    def get_absolute_url(self):
        return reverse('response:agency_detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.name

class RescueMarks(models.Model):
    agency = models.ForeignKey(Agency,related_name='given_marks',on_delete=models.CASCADE)
    rescue = models.ForeignKey(Rescue,related_name="marks",on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=250)
    marks_obtained = models.IntegerField()
    maximum_marks = models.IntegerField()

    def __str__(self):
        return self.subject_name

class RescuesInClass(models.Model):
    agency = models.ForeignKey(Agency,related_name="class_agency",on_delete=models.CASCADE)
    rescue = models.ForeignKey(Rescue,related_name="user_rescue_name",on_delete=models.CASCADE)

    def __str__(self):
        return self.rescue.name

    class Meta:
        unique_together = ('agency','rescue')

class MessageToAgency(models.Model):
    rescue = models.ForeignKey(Rescue,related_name='rescue',on_delete=models.CASCADE)
    agency = models.ForeignKey(Agency,related_name='messages',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)

    def __str__(self):
        return self.message

    def save(self,*args,**kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args,**kwargs)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['rescue','message']

class ClassNotice(models.Model):
    agency = models.ForeignKey(Agency,related_name='agency',on_delete=models.CASCADE)
    rescues = models.ManyToManyField(Rescue,related_name='class_notice')
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)

    def __str__(self):
        return self.message

    def save(self,*args,**kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args,**kwargs)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['agency','message']

class ClassAssignment(models.Model):
    rescue = models.ManyToManyField(Rescue,related_name='rescue_assignment')
    agency = models.ForeignKey(Agency,related_name='agency_assignment',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    assignment_name = models.CharField(max_length=250)
    assignment = models.FileField(upload_to='assignments')

    def __str__(self):
        return self.assignment_name

    class Meta:
        ordering = ['-created_at']

class SubmitAssignment(models.Model):
    rescue = models.ForeignKey(Rescue,related_name='rescue_submit',on_delete=models.CASCADE)
    agency = models.ForeignKey(Agency,related_name='agency_submit',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    submitted_assignment = models.ForeignKey(ClassAssignment,related_name='submission_for_assignment',on_delete=models.CASCADE)
    submit = models.FileField(upload_to='Submission')

    def __str__(self):
        return "Submitted"+str(self.submitted_assignment.assignment_name)

    class Meta:
        ordering = ['-created_at']
