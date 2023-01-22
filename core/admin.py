from django.contrib import admin
from .models import City

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', '_user', 'lon', 'lat')
    list_filter = ('name', 'user', 'lon')
    readonly_fields = ('user',)
    save_as = True

    def	_user(self, row):
            return ','.join([x.username for x in row.user.all()])

admin.site.register(City, CategoryAdmin)
