from django.contrib import admin

from .models import AdvUser
from .models import SuperRubric, SubRubric
from .forms import SubRubricForm
from .models import Bv, AdditionalImage

admin.site.register(AdvUser)

class SubRubricInline(admin.TabularInline):
    model = SubRubric

class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ('super_rubric',)
    inlines = (SubRubricInline,)

admin.site.register(SuperRubric, SuperRubricAdmin)

class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm

admin.site.register(SubRubric, SubRubricAdmin)

class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage

class BvAdmin(admin.ModelAdmin):
    list_display = ('rubric', 'title', 'content', 'author', 'created_at')
    fields = (('rubric','author'), 'title', 'content', 'price', 'contacts', 'image', 'is_active')
    inlines = (AdditionalImageInline,)

admin.site.register(Bv, BvAdmin)
