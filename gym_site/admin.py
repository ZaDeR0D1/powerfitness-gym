from django.contrib import admin
from .models import Coach, Program, ContactMessage

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization')
    list_filter = ('specialization',)
    search_fields = ('name', 'specialization')

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'coach', 'duration', 'price', 'level')
    list_filter = ('level', 'duration')
    search_fields = ('title', 'description')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('created_at',)