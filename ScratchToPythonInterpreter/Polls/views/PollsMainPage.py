from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from Polls.models import Question, Answer
from Polls.forms import AnswerForm


class PollsMainPage(View):
    def get(self, request):
        return render(request, 'Polls/polls_main_page.html', {'pools': AnswerForm()})

    def get_questions(self):
        questions_list = list()
        questions = Question.objects.filter(is_visible=True).values_list('id', 'question_text')
        for question in questions:
            questions_list.append({'question_id': question[0], 'question_text': question[1],
                                   'answers': self.get_answers_for_question(question[0])})
        return questions_list

    def get_answers_for_question(self, question_id):
        answers_list = list()
        answers = Answer.objects.filter(question_id=question_id).values_list('id', 'answer_text')
        for answer in answers:
            answers_list.append({'answer_id': answer[0], 'answer_text': answer[1]})
        return answers_list
