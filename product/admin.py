from django.contrib import admin
from .models import Product,SearchHistory



class PriceFilter(admin.SimpleListFilter):
    title = "Price Range"
    parameter_name = "price"

    def lookups(self, request, model_admin):
        return (
            ("500-", "Less than 500"),
            ("1000-", "Less than 1000"),
            ("1000+", "Greater than 1000"),
            ("5000+", "Greater than 5000"),
        )

    def queryset(self, request, queryset):
        if self.value() == "500-":
            return queryset.filter(price__lt=500)
        elif self.value() == "1000-":
            return queryset.filter(price__lt=1000)
        elif self.value() == "1000+":
            return queryset.filter(price__gt=1000)
        elif self.value() == "5000+":
            return queryset.filter(price__gt=5000)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug", "price", "available", "created", "updated"]
    list_filter = ["available", "created", "updated", PriceFilter]
    list_editable = ["price", "available"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]

admin.site.register(SearchHistory)