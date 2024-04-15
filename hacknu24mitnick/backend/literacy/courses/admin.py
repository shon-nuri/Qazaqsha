from django.contrib import admin

from courses.models import Answer, Quiz, Lesson, Course


# Register your models here.


@admin.register(Course)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('question', 'type')
    search_fields = ('question',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'is_right')
    search_fields = ('answer',)
