from django.db import models
from django.contrib.auth.models import AbstractUser
from OJ.models import Problem

# Create your models here.

class User(AbstractUser):
    email=models.EmailField(max_length=100,unique=True,default="")
    username=models.CharField(max_length=40,default="",unique=True)
    total_score=models.IntegerField(default=0)
    profile_picture=models.ImageField(upload_to='',default="default.jpg",blank=True,null=True)
    
    class Meta:
        ordering=['-total_score']
    
    def __str__(self):
        return self.username

class Submission(models.Model):
    LANGUAGES=[("C++","C++"),("Python3","Python3"),("Java","Java")]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    problem=models.ForeignKey(Problem,on_delete=models.CASCADE)
    code=models.TextField(default="")
    verdict=models.CharField(max_length=50,default="")
    sub_time=models.DateTimeField(auto_now=True,null=True)
    language=models.CharField(max_length=10,default="C++",choices=LANGUAGES)
    runtime=models.DecimalField(max_digits=5,decimal_places=2, default=0, null=True)
    stderr=models.TextField(default="")
    stdout=models.TextField(default="")

    class Meta:
        ordering=['-sub_time']

    def __str__(self) :
        return f"{self.user}:{self.problem}:{self.sub_time}:{self.language}:{self.verdict}"
