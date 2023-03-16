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
        

class ChoicesInline(admin.TabularInline):
    model = Choice
    formset= AtLeastOneRequiredInlineFormSet
    extra = 1
    exclude= ['votes']

class QuestionAdmin(admin.ModelAdmin):
    inlines=(ChoicesInline,)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()        
        for instance in instances:
            instance.save() 

admin.site.register(Question, QuestionAdmin)

