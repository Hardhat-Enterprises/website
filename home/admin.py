from django.contrib import admin

# Keeping only one instance of ResourceAdmin
@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)
    list_filter = ('created_at',)

    def created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M:%S')
    created_at.admin_order_field = 'created_at'
    created_at.short_description = 'Created At'