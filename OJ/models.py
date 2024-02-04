from django.db import models
from froala_editor.fields import FroalaField
# Create your models here.
class Problem(models.Model):
    Level=[("E","Easy"),("M","Medium"),("H","Hard")]
    title=models.CharField(max_length=100,default="")
    description=FroalaField(default="")
    difficulty=models.CharField(max_length=1,choices=Level)
    time_limit=models.IntegerField(default=2)
    memory_limit=models.IntegerField(default=128)
    def __str__(self) :
        return self.title

class TestCase(models.Model):
    problem=models.ForeignKey(Problem,on_delete=models.CASCADE)     
    input=models.TextField(default="")
    output=models.TextField(default="")
    def __str__(self):
        return f"{self.problem}:{self.id}"