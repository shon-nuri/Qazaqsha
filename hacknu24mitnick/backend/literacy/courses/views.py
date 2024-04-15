import json

import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.contrib import messages

from courses.forms import CreateLessonForm, CreateCourseForm, FeedbackForm
from courses.models import Course, Lesson, Result


# Create your views here.


def base_page(request):
    if request.method == "POST":
        form = FeedbackForm()
        return render(request, "courses/index.html")
    form = FeedbackForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Feedback sent successfully")
    return render(request, "courses/index.html")


class CoursesList(ListView):
    model = Course
    template_name = "courses/course/course-list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        print(context)

        return context


class CourseDetail(DetailView):
    model = Course
    template_name = "courses/course_detail.html"

    def get_queryset(self):
        slug = get_object_or_404(Course, slug=self.kwargs.get("course"))


class CreateCourse(CreateView, ):
    model = Course
    template_name = "courses/course/create.html"
    form_class = CreateCourseForm
    success_url = reverse_lazy('courses:course_list')


class LessonDetail(DetailView):
    model = Lesson
    template_name = "courses/lessons/detail.html"


class LessonList(ListView):
    model = Lesson
    template_name = "courses/lessons/list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        t = []
        for lesson in context["lesson_list"]:
            a = []
            for quiz in lesson.quizes.all():
                percents = quiz.results.filter(user=self.request.user).first()
                if percents:
                    a.append(percents.percent)
            lesson.percent = sum(a) / len(a) if a else 0
            t.append(lesson)
        context["lesson_list"] = t
        print(context)
        return context


class CreateLesson(CreateView):
    model = Lesson
    template_name = "courses/lessons/create.html"
    form_class = CreateLessonForm

    def get_success_url(self):
        return reverse("courses:lesson_detail", kwargs={"slug": self.object.slug})


class LessonTest(DetailView):
    model = Lesson
    template_name = "courses/lessons/test.html"

    def get(self, request, *args, **kwargs):
        lesson = self.get_object()
        quizes = lesson.quizes.all()
        try:
            get = Result.objects.get(user=request.user, quiz=quizes.first())
        except Result.DoesNotExist:
            get = None
        if get:
            return HttpResponseRedirect(reverse("courses:lesson_detail", kwargs={"slug": lesson.slug}))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        lesson = self.get_object()
        quizes = lesson.quizes.all()
        try:
            get = Result.objects.get(user=request.user, quiz=quizes.first())
        except Result.DoesNotExist:
            get = None
        if get:
            return JsonResponse({"error": "You have already passed this test"})
        submitted_answers = {i: request.POST[i] for i in request.POST.keys() if
                             i not in ["quiz", "csrfmiddlewaretoken"]}
        correct_answers = [quiz.questions.filter(is_right=True).values_list("id", flat=True).first()
                           for quiz in
                           quizes]
        correct_count = sum(
            [1 for i in submitted_answers.keys() if int(i) in correct_answers])
        incorrect_count = sum(
            [1 for i in submitted_answers.keys() if int(i) not in correct_answers and int(submitted_answers[i]) == int(i)])
        percent = correct_count / len(correct_answers) * 100

        print(submitted_answers, correct_answers, incorrect_count, correct_count, percent)

        # Save the result in the database
        result = Result.objects.create(
            user=request.user,
            quiz=quizes.first(),
            percent=percent
        )

        return HttpResponseRedirect(reverse("courses:lesson_detail", kwargs={"slug": lesson.slug}))


@csrf_exempt
def translate(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed", 'info': "Available languages: en, ru, kk"})

    print(request.headers)
    data = json.loads(request.body.decode('utf-8'))
    texts = data.get("texts")
    source_language = data.get("sourceLanguageCode")
    target_language = data.get("targetLanguageCode")

    print(data)

    url = "https://translate.api.cloud.yandex.net/translate/v2/translate"
    payload = {
        "texts": texts,
        "sourceLanguageCode": source_language,
        "targetLanguageCode": target_language,
        "format": "PLAIN_TEXT",
        "folderId": "b1g7eqq5q277knhj42b2",
        "speller": True
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key AQVN0bZNKdTiZI1L7whsPeoSRdfODJpQA05vdb-Q"
    }

    response = requests.post(url, json=payload, headers=headers)
    return JsonResponse(response.json())


def translator(request):
    return render(request, "courses/translator.html")
