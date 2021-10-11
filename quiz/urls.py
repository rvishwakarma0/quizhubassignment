from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('classroom/<int:cid>/', classroom, name='classroom'),
    path('quiz/<int:qid>/', quiz, name='quiz'),
    path('submit/', submit, name='submit'),
    path('teacher/', tdashboard, name='tdashboard'),
    path('teacher/createClassRoom/', createClassRoom, name='createClassRoom'),
    path('teacher/classroom/<int:cid>/', tclassroom, name='tclassroom'),
    path('teacher/classroom/<int:cid>/createQuiz/', createQuiz, name='createQuiz'),
    path('teacher/classroom/<int:cid>/createQuiz/<int:qid>/', createQuizQuestion, name='createQuizQuestion'),
    path('teacher/report/', report, name='report'),
    path('teacher/register/', register, name='register'),
    path('teacher/login/', slogin, name='login'),
    path('teacher/logout/', slogout, name='logout')
]
'''
path('question/<int:quiz_id>/<int:qno>', question, name="question"),
path('answer/<int:quiz_id>', answer, name='answer'),
path('result/<int:quiz_id>', result, name='result'),


'''