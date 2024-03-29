from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=300)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=300)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.answer_text
