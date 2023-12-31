from django.contrib import admin

from .models import Choice, Question, Vote


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        (
            'Date information',
            {'fields': ['pub_date', 'end_date'], 'classes': ['collapse']}),
    ]
    list_display = ('id', 'question_text', 'pub_date', 'end_date',
                    'is_published', 'was_published_recently', 'can_vote')
    inlines = [ChoiceInline]
    list_filter = ['pub_date', 'end_date']
    search_fields = ['question_text']
    ordering = ('id',)


class QuestionVote(admin.ModelAdmin):
    list_display = ('user', 'id', 'choice')
    ordering = ('user',)


admin.site.register(Question, QuestionAdmin)

admin.site.register(Vote, QuestionVote)
