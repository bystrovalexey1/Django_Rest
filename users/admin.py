from django.contrib import admin

from users.models import CustomUser, Payments


@admin.register(CustomUser)
class UsersAdmin(admin.ModelAdmin):
    exclude = ("password",)

@admin.register(Payments)
class UsersAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "pay_date",
        "pay_course",
        "pay_lesson",
        "payment_amount",
        "payment_method",
    )
    list_filter = ("pay_date",)
    search_fields = (
        "user",
        "pay_date",
    )