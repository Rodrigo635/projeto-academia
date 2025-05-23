from django.shortcuts import render
from app_academia.forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import date, timedelta, timezone
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods


def home(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    else:
        return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                username = User.objects.get(email=email).username
                user = authenticate(
                    request, username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    return redirect(request.GET.get('next', 'inicio'))
                else:
                    form.add_error(None, 'Email ou senha incorretos')
            except User.DoesNotExist:
                form.add_error('email', 'Email não registrado')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            auth_login(request, user)
            return redirect('inicio')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('home')

@login_required
@require_http_methods(['GET', 'POST'])
def inicio(request):
    # 1) buscar plano ativo
    try:
        active = ActivePlan.objects.get(user=request.user, is_active=True)
    except ActivePlan.DoesNotExist:
        return render(request, 'inicio.html', {'workout_day': None})

    plan = active.plan
    plan_days_qs = PlanDay.objects.filter(plan=plan).order_by('sequence')
    total_days = plan_days_qs.count()
    if total_days == 0:
        return render(request, 'inicio.html', {'workout_day': None})

    # 2) seq vindo do querystring (navegação) ou calculado por sessões concluídas
    seq_param = request.GET.get('seq')
    if seq_param:
        try:
            seq = int(seq_param)
        except ValueError:
            seq = 1
    else:
        done = WorkoutSession.objects.filter(
            user=request.user,
            day__in=plan.days.all(),
            completed=True
        ).count()
        seq = (done % total_days) + 1

    # wrap-around
    if seq < 1: seq = total_days
    if seq > total_days: seq = 1

    plan_day = plan_days_qs.get(sequence=seq)
    dia = plan_day.day
    items = WorkoutDayExercise.objects.filter(day=dia).order_by('order')

    # 3) tratamento de POST vindo do modal
    if request.method == 'POST':
        form = WorkoutSessionForm(request.POST)
        if form.is_valid():
            sess = form.save(commit=False)
            sess.user = request.user
            sess.day = dia
            sess.completed = True
            sess.save()
            return redirect('inicio')  # reinicia loop
    else:
        today_str = date.today().strftime('%Y-%m-%d')  # converte para string no formato correto
        form = WorkoutSessionForm(initial={
            'date': today_str,
            'duration': timedelta(hours=1),
        })

    return render(request, 'inicio.html', {
        'workout_day': dia,
        'exercises': items,
        'form': form,
        'seq': seq,
        'total_days': total_days,
    })

@login_required
def treinos(request):
    meus_planos = TrainingPlan.objects.filter(owner=request.user)
    plano_ativo = ActivePlan.objects.filter(
        user=request.user, is_active=True).first()
    return render(request, 'treinos.html', {
        'meus_planos': meus_planos,
        'plano_ativo': plano_ativo,
    })


@login_required
def novo_dia(request):
    if request.method == 'POST':
        form = WorkoutDayForm(request.POST)
        if form.is_valid():
            form.save()
            # ou para uma lista global de dias
            return redirect('treinos')
    else:
        form = WorkoutDayForm()
    return render(request, 'novo_dia.html', {'form': form})


@login_required
def editar_dia(request, dia_id):
    dia = get_object_or_404(WorkoutDay, id=dia_id)
    if request.method == 'POST':
        form = WorkoutDayForm(request.POST, instance=dia)
        if form.is_valid():
            form.save()
            return redirect('listar_dias', plano_id=None)
    else:
        form = WorkoutDayForm(instance=dia)
    return render(request, 'editar_dia.html', {'form': form, 'dia': dia})


@login_required
def listar_dias(request, plano_id):
    plano = get_object_or_404(TrainingPlan, id=plano_id, owner=request.user)
    associados = PlanDay.objects.filter(plan=plano).select_related('day')
    todos_dias = WorkoutDay.objects.exclude(training_plans=plano)
    return render(request, 'listar_dias.html', {
        'plano': plano,
        'associados': associados,
        'todos_dias': todos_dias,
    })


@login_required
def adicionar_dia_ao_plano(request, plano_id, dia_id):
    plano = get_object_or_404(TrainingPlan, id=plano_id, owner=request.user)
    dia = get_object_or_404(WorkoutDay, id=dia_id)
    # define sequência como +1 do último
    ultima_seq = PlanDay.objects.filter(plan=plano).aggregate(
        models.Max('sequence'))['sequence__max'] or 0
    PlanDay.objects.create(plan=plano, day=dia, sequence=ultima_seq + 1)
    return redirect('listar_dias', plano_id=plano.id)

@login_required
def remover_dia_do_plano(request, plano_id, pd_id):
    plano = get_object_or_404(TrainingPlan, id=plano_id, owner=request.user)
    plan_day = get_object_or_404(PlanDay, id=pd_id, plan=plano)
    if request.method == 'POST':
        plan_day.delete()
    return redirect('listar_dias', plano_id=plano_id)


@login_required
def cadastrar_exercicio_no_dia(request, plano_id, dia_id):
    dia = get_object_or_404(WorkoutDay, id=dia_id)
    # pega todas as associações WorkoutDayExercise para esse dia
    existing = WorkoutDayExercise.objects.filter(day=dia).select_related('exercise')

    if request.method == 'POST':
        form = WorkoutDayExerciseForm(request.POST)
        if form.is_valid():
            exerc = form.save(commit=False)
            exerc.day = dia
            exerc.save()
            return redirect('listar_dias', plano_id=plano_id)
    else:
        form = WorkoutDayExerciseForm()

    return render(request, 'cadastrar_exercicio_no_dia.html', {
        'form': form,
        'dia': dia,
        'plano_id': plano_id,
        'existing': existing,    # <<--- aqui
    })

@login_required
def editar_exercicio_no_dia(request, plano_id, dia_id, wd_id):
    wd = get_object_or_404(WorkoutDayExercise, id=wd_id, day__id=dia_id)
    if request.method == 'POST':
        form = WorkoutDayExerciseForm(request.POST, instance=wd)
        if form.is_valid():
            form.save()
            return redirect('cadastrar_exercicio_no_dia', plano_id=plano_id, dia_id=dia_id)
    else:
        form = WorkoutDayExerciseForm(instance=wd)
    return render(request, 'editar_exercicio_no_dia.html', {
        'form': form,
        'dia': wd.day,
        'plano_id': plano_id,
        'wd': wd,
    })

@login_required
def remover_exercicio_no_dia(request, plano_id, dia_id, wd_id):
    wd = get_object_or_404(WorkoutDayExercise, id=wd_id, day__id=dia_id)
    if request.method == 'POST':
        wd.delete()
    return redirect('cadastrar_exercicio_no_dia', plano_id=plano_id, dia_id=dia_id)

@login_required
def novo_plano(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        dificuldade = request.POST.get('dificuldade')
        if nome and dificuldade:
            plano = TrainingPlan.objects.create(
                name=nome,
                description=descricao,
                difficulty=dificuldade,
                owner=request.user,
                is_template=False
            )
            return redirect('treinos')
    return render(request, 'novo_plano.html')


@login_required
def ativar_plano(request, plano_id):
    plano = get_object_or_404(TrainingPlan, id=plano_id, owner=request.user)

    # Desativa plano atual, se existir
    ActivePlan.objects.filter(
        user=request.user, is_active=True).update(is_active=False)

    # Ativa o novo plano
    ActivePlan.objects.create(
        user=request.user, plan=plano, start_date=date.today(), is_active=True)

    return redirect('treinos')


@login_required
def desativar_plano(request):
    ActivePlan.objects.filter(
        user=request.user, is_active=True).update(is_active=False)
    return redirect('treinos')


@login_required
def editar_plano(request, plano_id):
    plano = get_object_or_404(TrainingPlan, id=plano_id, owner=request.user)

    if request.method == 'POST':
        plano.name = request.POST.get('nome')
        plano.description = request.POST.get('descricao')
        plano.difficulty = request.POST.get('dificuldade')
        plano.save()
        return redirect('treinos')

    return render(request, 'editar_plano.html', {'plano': plano})


@login_required
def exercicios(request):
    exercicios = Exercise.objects.all()
    return render(request, 'exercicios.html', {'exercicios': exercicios})


@login_required
def cadastrar_exercicio(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('exercicios')
    else:
        form = ExerciseForm()
    return render(request, 'cadastrar_exercicio.html', {'form': form})


@login_required
def estatisticas(request):
    sessoes_concluidas = WorkoutSession.objects.filter(
        user=request.user,
        completed=True
    ).order_by('-date')

    total_concluidas = sessoes_concluidas.count()

    return render(request, 'estatisticas.html', {
        'total_concluidas': total_concluidas,
        'sessoes': sessoes_concluidas
    })
