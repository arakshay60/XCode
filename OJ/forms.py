from django.forms import ModelForm
from Users.models import Submission

class Code(ModelForm):
    class Meta:
        model=Submission
        fields=['code','language']