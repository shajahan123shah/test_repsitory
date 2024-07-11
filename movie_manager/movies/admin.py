from django.contrib import admin

# Register your models here.
from .models import MovieInfo,CensorInfo,Director,Actor

@admin.register(MovieInfo)
class MovieInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'description' )
    search_fields = ('title', 'year')
    list_filter = ('year',)
    
@admin.register(Director)
class DirectorsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Actor)
class ActorsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(CensorInfo)
class CensorInfoAdmin(admin.ModelAdmin):
    list_display = ('rating', 'certified_by')
    search_fields = ('rating', 'certified_by')