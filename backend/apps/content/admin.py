from django.contrib import admin
from .models import Subject, Topic, Question, AnswerOption, QuestionReview

class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 4

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'target_questions', 'display_order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('display_order', 'is_active')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'slug', 'display_order', 'is_active')
    list_filter = ('subject', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text_short', 'subject', 'difficulty', 'review_status', 'is_active')
    list_filter = ('subject', 'difficulty', 'review_status', 'is_active')
    search_fields = ('question_text', 'correct_answer', 'explanation')
    inlines = [AnswerOptionInline]

    def question_text_short(self, obj):
        return obj.question_text[:75]
    question_text_short.short_description = 'Question'

@admin.register(QuestionReview)
class QuestionReviewAdmin(admin.ModelAdmin):
    list_display = ('question', 'reviewer', 'status', 'reviewed_at')
    list_filter = ('status',)

