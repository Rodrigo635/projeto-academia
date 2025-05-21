from django.db import models
from django.contrib.auth.models import User


class MuscleGroup(models.Model):
    class Meta:
        verbose_name = 'Grupo muscular'
        verbose_name_plural = 'Grupos musculares'

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=20, unique=True)
    # ex.: A, B, C, “Peito”, “Pernas”… ou use para diferenciar templates

    def __str__(self):
        return self.name


class Exercise(models.Model):
    class Meta:
        verbose_name = 'Exercício'
        verbose_name_plural = 'Exercícios'

    name = models.CharField(max_length=100)
    description = models.TextField()
    use_weight = models.BooleanField(default=False)
    weight = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True
    )
    tip = models.TextField()
    photo = models.ImageField(upload_to='media/exercises/photos/')
    video_url = models.URLField(blank=True)
    reps = models.PositiveIntegerField(default=0)
    sets = models.PositiveIntegerField(default=0)
    rest_sec = models.PositiveIntegerField(default=60)
    muscles = models.ManyToManyField(MuscleGroup, related_name='exercises')
    tags = models.ManyToManyField(Tag, related_name='exercises')

    def __str__(self):
        return self.name


class WorkoutDay(models.Model):
    class Meta:
        verbose_name = 'Dia de treino'
        verbose_name_plural = 'Dias de treino'

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    exercises = models.ManyToManyField(
        Exercise,
        through='WorkoutDayExercise',
        related_name='workout_days'
    )

    def __str__(self):
        return self.name


class WorkoutDayExercise(models.Model):
    class Meta:
        verbose_name = 'Exercício do dia de treino'
        verbose_name_plural = 'Exercícios do dia de treino'

    day = models.ForeignKey(WorkoutDay, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=1)
    custom_reps = models.PositiveIntegerField(null=True, blank=True)
    custom_sets = models.PositiveIntegerField(null=True, blank=True)
    rest_sec = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.day.name} - {self.exercise.name}"


class WorkoutSession(models.Model):
    class Meta:
        verbose_name = 'Sessão de treino'
        verbose_name_plural = 'Sessões de treino'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.ForeignKey(WorkoutDay, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    duration = models.DurationField(null=True, blank=True)
    feeling = models.CharField(
        max_length=20,
        choices=[('easy', 'Fácil'), ('hard', 'Difícil'),
                 ('tired', 'Cansativo')]
    )
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.day.name} - {self.date}"


class TrainingPlan(models.Model):
    class Meta:
        verbose_name = 'Plano de treino'
        verbose_name_plural = 'Planos de treino'

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    difficulty = models.CharField(
        max_length=20,
        choices=[('beginner', 'Iniciante'),
                 ('intermediate', 'Intermediário'),
                 ('advanced', 'Avançado')]
    )
    days_count = models.PositiveSmallIntegerField(default=1)
    days = models.ManyToManyField(
        WorkoutDay,
        through='PlanDay',
        related_name='training_plans'
    )
    is_template = models.BooleanField(default=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )  # null para templates globais

    def __str__(self):
        return self.name


class PlanDay(models.Model):
    class Meta:
        verbose_name = 'Dia do plano de treino'
        verbose_name_plural = 'Dias do plano de treino'
        
    plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE)
    day = models.ForeignKey(WorkoutDay, on_delete=models.CASCADE)
    sequence = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.day.name} - {self.plan.name}'


class CustomPlan(TrainingPlan):
    # herda tudo, mas is_template=False e owner obrigatório
    class Meta:
        proxy = True

class ActivePlan(models.Model):
    class Meta:
        verbose_name = 'Plano de treino ativo'
        verbose_name_plural = 'Planos de treino ativos'

    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    plan        = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE)
    start_date  = models.DateField(auto_now_add=True)
    end_date    = models.DateField(null=True, blank=True)
    is_active   = models.BooleanField(default=True)

    def __str__(self):
        return self.plan.name
