from django.contrib import admin
from .models import *


admin.site.register(Exercise)
admin.site.register(MuscleGroup)
admin.site.register(Tag)
admin.site.register(WorkoutDay)
admin.site.register(WorkoutDayExercise)
admin.site.register(TrainingPlan)
admin.site.register(PlanDay)
admin.site.register(ActivePlan)
admin.site.register(WorkoutSession)

