from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Quiz)
admin.site.register(Question)

admin.site.register(QuizResult)
admin.site.register(Teacher)
admin.site.register(Classroom)

admin.site.register(Answer)




