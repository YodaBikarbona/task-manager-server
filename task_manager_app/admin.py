from django.contrib import admin
from .models import (
    Department,
    Role,
    User,
    UserRole,
    Priority,
    Task,
    TrackerRoadmap,
    TrackerRoadmapTask
)

# Register your models here.

admin.register(Department)(admin.ModelAdmin)
admin.register(Role)(admin.ModelAdmin)
admin.register(User)(admin.ModelAdmin)
admin.register(UserRole)(admin.ModelAdmin)
admin.register(Priority)(admin.ModelAdmin)
admin.register(Task)(admin.ModelAdmin)
admin.register(TrackerRoadmap)(admin.ModelAdmin)
admin.register(TrackerRoadmapTask)(admin.ModelAdmin)
