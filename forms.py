from django import forms
from .models import Signup
from .models import *

class SignupForm(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ['contact', 'branch', 'role']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['assignment_title', 'due_date', 'assignment_file']

class ReviewqueForm(forms.ModelForm):
    class Meta:
        model = Reviewque
        fields = ['branch', 'subject', 'notesfile', 'filetype', 'description', 'status']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text', 'is_correct']


