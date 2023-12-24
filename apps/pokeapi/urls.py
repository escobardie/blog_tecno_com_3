from django.urls import path
from . import views

urlpatterns = [
    #path('', views.listPokemons, name='inicio_poke_api'), # original
    path('pokeapi/', views.listPokemons, name='inicio_poke_api'), # prueba
    path('detail/',views.detail_pokemon),
    path('test/',views.buscar_pokemon),

]
