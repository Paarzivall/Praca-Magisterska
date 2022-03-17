from django import forms
from .models import Question, Answer


class AnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        questions = Question.objects.filter(is_visible=True).values_list('id', 'question_text')
        for question in questions:
            self.fields[question[1]] = forms.ModelChoiceField(
                required=True,
                queryset=Answer.objects.filter(question_id=question[0]).all(),
                empty_label="Wybierz odpowiedź...",
            )
