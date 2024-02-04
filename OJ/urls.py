from django.urls import path, include
from OJ import views
urlpatterns = [
    path('',views.problemPage,name='home'),
    path('problems',views.problemPage,name='problem'),
    path('problems/<int:problem_id>/',views.descriptionPage,name='description'),
    path('leaderboard/',views.leaderBoard,name='leaderboard'),
    path('problems/<int:problem_id>/verdict/',views.verdictPage,name='verdict'),
    path('submissions/',views.submissionPage,name='submission'),
    path('submissions/<int:submission_id>',views.submissionCode,name='code'),
]