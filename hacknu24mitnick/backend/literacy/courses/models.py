import math

from django.db import models
from django.urls import reverse


# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    prev_course = models.ForeignKey(
        "Course",
        related_name="next_course",
        on_delete=models.CASCADE,
        null=True,
        blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("courses:course_detail", kwargs={"slug": self.slug})


class Lesson(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    video = models.CharField(max_length=500)
    course = models.ForeignKey("Course", related_name="lessons", on_delete=models.CASCADE)
    prev_lesson = models.ForeignKey(
        "Lesson",
        related_name="next_lesson",
        on_delete=models.CASCADE,
        null=True,
        blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("courses:lesson_detail", kwargs={"slug": self.slug})

    def get_test_link(self):
        return self.get_absolute_url() + "/test"

    def get_percent(self):
        results = Result.objects.filter(quiz__lesson=self)
        if results:
            return math.floor(sum([result.percent for result in results]) / len(results))
        return 0


class Quiz(models.Model):
    question = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    lesson = models.ForeignKey("Lesson", related_name="quizes", on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class Answer(models.Model):
    answer = models.CharField(max_length=255)
    quiz = models.ForeignKey("Quiz", related_name="questions", on_delete=models.CASCADE)
    is_right = models.BooleanField()

    def __str__(self):
        return self.answer


class Result(models.Model):
    user = models.ForeignKey("authorization.User", related_name="results", on_delete=models.CASCADE)
    quiz = models.ForeignKey("Quiz", related_name="results", on_delete=models.CASCADE)
    percent = models.FloatField()


class Feedback(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    checked = models.BooleanField(default=False)

    def is_valid(self):
        return self.full_name and self.email and self.phone and self.message

    def __str__(self):
        return self.full_name
