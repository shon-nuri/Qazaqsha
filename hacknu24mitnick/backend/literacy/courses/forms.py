from slugify import slugify
from django import forms

from courses.models import Lesson, Course, Feedback


class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['name', 'video', 'course']

    def save(self, commit=True):
        self.instance.slug = slugify(self.instance.name)
        return super().save(commit=commit)


class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name',]

    def save(self, commit=True):
        self.instance.slug = slugify(self.instance.name)
        return super().save(commit=commit)


class FeedbackForm(forms.Form):
    full_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    message = forms.CharField(widget=forms.Textarea)

    def save(self):
        feedback = Feedback(
            full_name=self.cleaned_data['full_name'],
            email=self.cleaned_data['email'],
            phone=self.cleaned_data['phone'],
            message=self.cleaned_data['message']
        )
        feedback.save()
        return feedback
