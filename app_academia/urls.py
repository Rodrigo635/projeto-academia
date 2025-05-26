from django.urls import path
from .views import *

urlpatterns = [
    # Home
    path('', home, name='home'),
    path('inicio/', inicio, name='inicio'),

    # Autenticacao
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Treinos
    path('treinos/', treinos, name='treinos'),
    path('treinos/novo/', novo_plano, name='novo_plano'),
    path('treinos/<int:plano_id>/editar/', editar_plano, name='editar_plano'),
    path('treinos/<int:plano_id>/ativar/', ativar_plano, name='ativar_plano'),
    path('treinos/<int:plano_id>/dias/<int:dia_id>/exercicios/novo/', cadastrar_exercicio_no_dia, name='cadastrar_exercicio_no_dia'),
    path('treinos/desativar/', desativar_plano, name='desativar_plano'),
    # Dias de treino
    path('treinos/<int:plano_id>/dias/novo/', novo_dia, name='novo_dia'),
    path('dias/<int:dia_id>/editar/', editar_dia, name='editar_dia'),
    path('treinos/<int:plano_id>/dias/', listar_dias, name='listar_dias'),
    path('treinos/<int:plano_id>/dias/adicionar/<int:dia_id>/', adicionar_dia_ao_plano, name='adicionar_dia_ao_plano'),
    path('treinos/<int:plano_id>/dias/<int:pd_id>/remover/', remover_dia_do_plano, name='remover_dia_do_plano'),
    path(
        'treinos/<int:plano_id>/dias/<int:dia_id>/exercicios/<int:wd_id>/editar/',
        editar_exercicio_no_dia,
        name='editar_exercicio_no_dia'
    ),
    path(
        'treinos/<int:plano_id>/dias/<int:dia_id>/exercicios/<int:wd_id>/remover/',
        remover_exercicio_no_dia,
        name='remover_exercicio_no_dia'
    ),

    # Exercicios
    path('exercicios/', exercicios, name='exercicios'),
    path('exercicios/novo/', cadastrar_exercicio, name='cadastrar_exercicio'),

    # Estatisticas
    path('estatisticas/', estatisticas, name='estatisticas'),
]