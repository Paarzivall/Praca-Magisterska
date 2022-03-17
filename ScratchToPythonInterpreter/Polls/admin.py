from django.contrib import admin
from .models import Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Is visible', {'fields': ['is_visible']}),
    ]
    inlines = [AnswerInline]


admin.site.register(Question, QuestionAdmin)
