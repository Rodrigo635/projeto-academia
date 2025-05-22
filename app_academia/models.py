from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class MuscleGroup(models.Model):
    class Meta:
        verbose_name = 'Grupo muscular'
        verbose_name_plural = 'Grupos musculares'

    name = models.CharField(max_length=50, unique=True, verbose_name="Nome do grupo muscular")

    def __str__(self):
        return self.name


class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=20, unique=True, verbose_name="Nome da tag")
    # ex.: A, B, C, “Peito”, “Pernas”… ou use para diferenciar templates

    def __str__(self):
        return self.name


class Exercise(models.Model):
    class Meta:
        verbose_name = 'Exercício'
        verbose_name_plural = 'Exercícios'

    name = models.CharField(max_length=100, unique=True, verbose_name="Nome do exercício")
    description = models.TextField(verbose_name="Descrição do exercício")
    use_weight = models.BooleanField(default=False, verbose_name="Usa peso?")
    weight = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        verbose_name="Peso"
    )
    tip = models.TextField(verbose_name="Dica")
    photo = models.ImageField(upload_to='exercises/', verbose_name="Foto/gif do exercício")
    video_url = models.URLField(blank=True, verbose_name="URL do video")
    reps = models.PositiveIntegerField(default=0, verbose_name="Repetições")
    sets = models.PositiveIntegerField(default=0, verbose_name="Séries")
    rest_sec = models.PositiveIntegerField(default=60, verbose_name="Descanso")
    muscles = models.ManyToManyField(MuscleGroup, related_name='exercises', verbose_name="Grupos musculares afetados")
    tags = models.ManyToManyField(Tag, related_name='exercises', verbose_name="Tags")

    def __str__(self):
        return self.name


class WorkoutDay(models.Model):
    class Meta:
        verbose_name = 'Dia de treino'
        verbose_name_plural = 'Dias de treino'

    name = models.CharField(max_length=100, verbose_name="Nome do dia de treino")
    description = models.TextField(blank=True, verbose_name="Descrição do dia de treino")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Tags")
    exercises = models.ManyToManyField(
        Exercise,
        through='WorkoutDayExercise',
        related_name='workout_days',
        verbose_name="Exercícios"
    )

    def __str__(self):
        return self.name


class WorkoutDayExercise(models.Model):
    class Meta:
        verbose_name = 'Exercício do dia de treino'
        verbose_name_plural = 'Exercícios do dia de treino'

    day = models.ForeignKey(WorkoutDay, verbose_name="Dia de treino", on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, verbose_name="Exercício", on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=1, verbose_name="Ordem")
    custom_reps = models.PositiveIntegerField(null=True, verbose_name="Repetições", blank=True)
    custom_sets = models.PositiveIntegerField(null=True, verbose_name="Séries", blank=True)
    rest_sec = models.PositiveIntegerField(null=True, verbose_name="Descanso", blank=True)

    def __str__(self):
        return f"{self.day.name} - {self.exercise.name}"


class WorkoutSession(models.Model):
    class Meta:
        verbose_name = 'Sessão de treino'
        verbose_name_plural = 'Sessões de treino'

    user = models.ForeignKey(User, verbose_name="Usuário", on_delete=models.CASCADE)
    day = models.ForeignKey(WorkoutDay, verbose_name="Dia de treino", on_delete=models.CASCADE)
    date = models.DateField(default=timezone.localdate, verbose_name="Data")
    duration = models.DurationField(null=True, blank=True, verbose_name="Duração")
    feeling = models.CharField(
        max_length=20,
        verbose_name="Como foi o treino?",
        choices=[('easy', 'Fácil'), ('normal', 'Normal'), ('hard', 'Difícil'),
                 ('tired', 'Cansativo')]
    )
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.day.name} - {self.date}"


class TrainingPlan(models.Model):
    class Meta:
        verbose_name = 'Plano de treino'
        verbose_name_plural = 'Planos de treino'

    name = models.CharField(max_length=100, verbose_name="Nome do plano de treino")
    description = models.TextField(blank=True, verbose_name="Descrição do plano de treino")
    difficulty = models.CharField(
        max_length=20,
        verbose_name="Dificuldade",
        choices=[('beginner', 'Iniciante'),
                 ('intermediate', 'Intermediário'),
                 ('advanced', 'Avançado')]
    )
    days_count = models.PositiveSmallIntegerField(default=1, verbose_name="Quantidade de dias")
    days = models.ManyToManyField(
        WorkoutDay,
        through='PlanDay',
        related_name='training_plans',
        verbose_name="Dias"
    )
    is_template = models.BooleanField(default=True, verbose_name="É um template?")
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Criador"
    )  # null para templates globais

    def __str__(self):
        return self.name


class PlanDay(models.Model):
    class Meta:
        verbose_name = 'Dia do plano de treino'
        verbose_name_plural = 'Dias do plano de treino'
        
    plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, verbose_name="Plano de treino")
    day = models.ForeignKey(WorkoutDay, on_delete=models.CASCADE, verbose_name="Dia de treino")
    sequence = models.PositiveSmallIntegerField(verbose_name="Ordem")

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

    user        = models.ForeignKey(User, verbose_name="Usuário", on_delete=models.CASCADE)
    plan        = models.ForeignKey(TrainingPlan, verbose_name="Plano de treino", on_delete=models.CASCADE)
    start_date  = models.DateField(auto_now_add=True, verbose_name="Data de inicio")
    end_date    = models.DateField(null=True, blank=True, verbose_name="Data de fim")
    is_active   = models.BooleanField(default=True, verbose_name="Está ativo?")

    def __str__(self):
        return self.plan.name