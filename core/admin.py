from django.contrib import admin

from .models import (
    Category,
    Crop,
    DosageRule,
    Field,
    IrrigationLog,
    Issue,
    IssueRecommendation,
    Product,
    SprayLog,
    SprayMixItem,
)


class IssueRecommendationInline(admin.TabularInline):
    model = IssueRecommendation
    extra = 1


class SprayMixItemInline(admin.TabularInline):
    model = SprayMixItem
    extra = 1


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind', 'crop')
    list_filter = ('kind', 'crop')
    search_fields = ('name', 'short_description', 'symptoms')
    inlines = [IssueRecommendationInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'active_ingredient')
    list_filter = ('category__group', 'category')
    search_fields = ('name', 'active_ingredient', 'formulation')


@admin.register(SprayLog)
class SprayLogAdmin(admin.ModelAdmin):
    list_display = ('date_time', 'field', 'crop', 'target_issue')
    list_filter = ('field', 'crop')
    inlines = [SprayMixItemInline]


admin.site.register(Crop)
admin.site.register(Field)
admin.site.register(Category)
admin.site.register(DosageRule)
admin.site.register(IrrigationLog)
admin.site.register(IssueRecommendation)
admin.site.register(SprayMixItem)
