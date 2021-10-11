from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
import datetime
from django.contrib.auth.models import User


def dashboard(request):
    classrooms = Classroom.objects.all()
    content = {'classrooms': classrooms}
    return render(request, 'dashboard.html', content)


def classroom(request, cid):
    croom = Classroom.objects.get(id=cid)
    quizzes = croom.quiz_set.all()
    context = {'quizzes': quizzes}
    return render(request, 'classroom.html', context)


def quiz(request, qid):
    qz = Quiz.objects.get(id=qid)
    questions = qz.question_set.all()
    context = {'questions': questions, 'qid': qid}
    return render(request, 'quiz.html', context)


def submit(request):
    if request.method == 'POST':
        try:
            qid = request.POST['qid']

            qz = Quiz.objects.get(id=qid)
            questions = qz.question_set.all()
            marks = 0
            for q in questions:
                aid = request.POST[str(q.id)]
                ans = Answer.objects.get(id=aid)
                if ans.correct:
                    marks += 1

            qres = QuizResult.objects.create(
                        quiz=qz,
                        studName=request.POST['studName'],
                        studRollNo=request.POST['studRollNo'],
                        score=marks)
            qres.save()
            msg = 'submitted successfully with marks ' + str(marks)
        except:
            msg = 'submission failed!!'
        context = {'msg': msg}
        return render(request, 'submit.html', context)
    else:
        return redirect('/')


def tdashboard(request):
    classrooms = []
    if request.user.is_authenticated:
        teacher = request.user.teacher
        classrooms = teacher.classroom_set.all()
    context = {'classrooms': classrooms}
    return render(request, 'tdashboard.html', context)


def createClassRoom(request):
    if request.method == 'POST':
        name = request.POST['name']
        teacher = request.user.teacher
        classroom, created = Classroom.objects.get_or_create(name=name, teacher=teacher)
        classroom.save()
        return redirect('/teacher/')
    return render(request, 'createClassRoom.html')


def tclassroom(request, cid):
    croom = Classroom.objects.get(id=cid)
    quizzes = croom.quiz_set.all()
    context = {'quizzes': quizzes, 'cid':cid}
    return render(request, 'tclassroom.html', context)


def createQuiz(request, cid):
    if request.method == 'POST':
        title = request.POST['title']
        classroom = Classroom.objects.get(id=cid)
        quiz, created = Quiz.objects.get_or_create(title=title, classroom=classroom)
        quiz.save()
        return redirect("/teacher/classroom/"+str(cid)+"/createQuiz/"+str(quiz.id)+"/")
    else:
        return render(request, "createQuiz.html")


def createQuizQuestion(request, cid, qid):
    msg = ''
    if request.method == 'POST':
        try:
            quiz = Quiz.objects.get(id=qid)
            qtext = request.POST['qtext']
            option1 = request.POST['option1']
            option2 = request.POST['option2']
            option3 = request.POST['option3']
            option4 = request.POST['option4']
            correct = request.POST['correct']
            question, created = Question.objects.get_or_create(quiz=quiz, question_text=qtext)
            question.save()

            answer1, created = Answer.objects.get_or_create(question=question,content=option1)
            answer2, created = Answer.objects.get_or_create(question=question, content=option2)
            answer3, created = Answer.objects.get_or_create(question=question, content=option3)
            answer4, created = Answer.objects.get_or_create(question=question, content=option4)

            if int(correct) == 1:
                answer1.correct=True
            elif int(correct) == 2:
                answer2.correct=True
            elif int(correct) == 3:
                answer3.correct=True
            elif int(correct) == 4:
                answer4.correct=True

            answer1.save()
            answer2.save()
            answer3.save()
            answer4.save()
            msg = 'saved successfully!!'
        except:
            msg='failed!'

    context = {'msg': msg}
    return render(request, "createQuizQuestion.html", context)


def report(request):
    quizResult={
        'quiz':'',
        'studName': '',
        'studRollNo':'',
        'score':'',
        'subTime':''
    }
    msg =''
    teacher = request.user.teacher
    classrooms = teacher.classroom_set.all()
    quizzes = Quiz.objects.filter(classroom__in=classrooms)
    if request.method == 'POST':
        try:
            qid = request.POST['qid']
            quiz = Quiz.objects.get(id=qid)
            quizResult = QuizResult.objects.filter(quiz = quiz)
        except:
            msg='error generating reports'
    context = {
        'quizResult': quizResult,
        'quizzes':quizzes
    }
    return render(request, "results.html",context)

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        user, created = User.objects.get_or_create(username = username)
        print(password)
        user.set_password(password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        teacher, created = Teacher.objects.get_or_create(user=user)
        teacher.save()
        return redirect('/teacher/login/')
    return render(request, 'register.html')


def slogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            return redirect('/teacher/')
    return render(request,'login.html')


def slogout(request):
    logout(request)
    return HttpResponseRedirect('/')

