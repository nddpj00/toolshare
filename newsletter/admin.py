from django.contrib import admin
from .models import Newsletter


class NewsletterAdmin(admin.ModelAdmin):

  
    list_display = (
        'first_name',
        'email',
        'is_registered_already',
    )


admin.site.register(Newsletter,NewsletterAdmin)
