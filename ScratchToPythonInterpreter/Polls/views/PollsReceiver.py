from django.shortcuts import render, redirect
from django.views.generic import View
from Polls.models import Question, Answer
from django.http import HttpResponseNotAllowed
from django.db.models import F


class PollsReceiver(View):
    def get(self, request):
        return HttpResponseNotAllowed(" ")

    def post(self, request, *args, **kwargs):
        questions = self.get_questions()
        user_answers = list()
        for question in questions:
            user_answers.append(request.POST[question])
        self.add_answers_to_database(user_answers)
        return render(request, 'Polls/PollsReceive.html')

    def get_questions(self):
        questions_list = list()
        questions = Question.objects.filter(is_visible=True).values_list('id', 'question_text')
        for question in questions:
            questions_list.append(question[1])
        return questions_list

    def add_answers_to_database(self, user_answers):
        for user_answer in user_answers:
            Answer.objects.filter(id=user_answer).update(votes=F('votes') + 1)
