from django.contrib import admin
from django import forms
from django.forms.models import BaseInlineFormSet
from .models import Question,Choice

# Register your models here.


class AtLeastOneRequiredInlineFormSet(BaseInlineFormSet):

    def clean(self):
        """Check that at least one choice has been entered."""
        super(AtLeastOneRequiredInlineFormSet, self).clean()
        if any(self.errors):
            return
        if not any(cleaned_data and not cleaned_data.get('DELETE', False)
            for cleaned_data in self.cleaned_data):
            raise forms.ValidationError('At least one choice required.')
        
"""class ChoiceInLine(admin.StackedInline):
    model = Choice
    extra = 3"""
class ChoicesInline(admin.TabularInline):
    model = Choice
    formset= AtLeastOneRequiredInlineFormSet
    extra = 3
    exclude= ['votes']

class QuestionAdmin(admin.ModelAdmin):
    fields= ["pub_date", "question_text"]
    inlines=(ChoicesInline,)
    list_display = ("question_text", "pub_date", "was_recently_published")
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()        
        for instance in instances:
            instance.save() 



admin.site.register(Question, QuestionAdmin)



