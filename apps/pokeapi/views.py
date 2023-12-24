from django.shortcuts import render, redirect
import json
import requests

# https://www.youtube.com/watch?v=xqFM6ykQEwo&ab_channel=Pyplane
# https://websitehurdles.com/display-json-data-html-django/

# BASE_URL_indi = "https://pokeapi.co/api/v2/pokemon/1/"
#BASE_URL = "http://pokeapi.co/api/v2/pokemon/" ## OBTENEMOS LOS POKEMOS "result": 20
BASE_URL = "https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0" ## OBTENEMOS LOS POKEMOS "result" = 1292

BASE_URL_2 = "http://pokeapi.co/api/v2"


URL_JSON_FAV = 'https://api.jsonbin.io/v3/b/65766d9112a5d37659a60702'
HEADERS_JSON_FAV = {
  'Content-Type': 'application/json',
  'X-Master-Key': '$2a$10$6j/bE9qv.Fv0guqxeiYNjOZV00H3W8pGmimJV.199zoJ3/mMtyoFW'
  }


## https://github.com/PokeAPI/pokebase/blob/master/pokebase/common.py
def url_build(endpoint, resource_id=None, subresource=None): ## EJEMPLO https://pokeapi.co/api/v2/pokemon/13/
  if resource_id is not None:
    if subresource is not None:
      return "/".join([BASE_URL_2, endpoint, str(resource_id), subresource, ""])
    return "/".join([BASE_URL_2, endpoint, str(resource_id), ""])
  return "/".join([BASE_URL_2, endpoint, ""])


def reqsGet(url):
    response = requests.get(url) ## OBTENEMOS DATOS DEL POKEMON
    response_json = response.json() ## LE DAMOS FORMATO JSON
    return response_json



def listPokemons(request): # RETORNAMOS DOS LISTAS. LISTA DE POKEMON DE LA API Y LA LISTA DE FAVORITOS
    response_json = reqsGet(BASE_URL)
    resul = response_json['results'] ## OBTENEMOS TODA LOS POKEMON EN UNA LISTA DE DIC. EJEM: [{NAME:VALUE, URL:VALUE}, {NAME:VALUE, URL:VALUE}]
    # list_fav = chek_fav_pkmon() # OBTENEMOS LA LISTA DE FAVORITOS
    return render(request,'pokemon/test.html', {'mylist':resul, 'mylist_fav':LIST_FAV})
    


def detail_pokemon(request): ## FUNCIONA
    data =  []
    data_abil = []

    if request.method == 'POST':
      print("entro por por POST")
      query = request.POST.get("pkmon_fav")
      #print(query)
      favorite(query)
      #return redirect('inicio')
      # return render(request,'pokemon/detail.html')

    
    querey_dict = request.GET # ESTO ES UN DICCIONARIO
    # print("querey_dict: ", querey_dict)
    query = querey_dict.get("POKEMON")
    # print("QUERY: "+query)
    link_complete = url_build("pokemon", query, subresource=None)
    # print("LINK_COMPLETO: ", link_complete) ## type : <class 'str'>
    url_link = reqsGet(link_complete)

    data.append(url_link['name'])
    data.append(url_link['id'])
    data.append(url_link['sprites']['front_default'])
    for abil in url_link['abilities']:
      data_abil.append(abil['ability']['name'])
    data.append(data_abil)

    list_fav = chek_fav_pkmon() # OBTENEMOS LA LISTA DE FAVORITOS

    return render(request, 'pokemon/detail.html', {'pokemon_details': data, 'mylist_fav':list_fav}) ## ZONA DE PRUEBAS


######################### ZONA BUSQUEDA ##########################
def buscar_pokemon(request):
    lista_busqueda = []
    ## https://www.youtube.com/watch?v=Nz5F60OxOKI&ab_channel=CodingEntrepreneurs
    ## https://www.youtube.com/watch?v=ELbE2VPOkOw&ab_channel=JuanJos%C3%A9VillaAlzate
    querey_dict = request.GET # ESTO ES UN DICCIONARIO

    query = querey_dict.get("buscar")
    # print("ENTRO POR AQUI "+query)

    if query == "":
        print("ENTRO POR VACIO")
        return  redirect('inicio_poke_api')
        #lista_busqueda.append({'name':"VACIO","url":""})
        #return render(request, 'pokemon/test.html', {'mylist_BUSQUEDA': lista_busqueda})

    else:
        response_json = reqsGet(BASE_URL)
        resul = response_json['results']
        for bus_pkmon in resul:
          if query in bus_pkmon['name'] :
            lista_busqueda.append({'name':bus_pkmon['name'],"url":bus_pkmon['url']})
        # print(lista_busqueda)

    return render(request, 'pokemon/test.html', {'mylist_BUSQUEDA': lista_busqueda, 'mylist_fav':LIST_FAV})


################################### BLOQUE FAVORITOS ###################################
def chek_fav_pkmon():
    #url = 'https://api.jsonbin.io/v3/b/6571dbe154105e766fdafe9b' # ORIGINAL
    url = 'https://api.jsonbin.io/v3/b/65766d9112a5d37659a60702' # json de lista con solo los nomres de los pokemon

    headers = {
    'X-Master-Key': '$2a$10$6j/bE9qv.Fv0guqxeiYNjOZV00H3W8pGmimJV.199zoJ3/mMtyoFW'
    }

    req = requests.get(url, json=None, headers=headers)
    # print(req.text)
    response_json = req.json() ## LE DAMOS FORMATO JSON

    data_favorite = response_json['record']

    return data_favorite

def favorite(new_favorite):
    # url = 'https://api.jsonbin.io/v3/b/65766d9112a5d37659a60702'
    # headers = {
    # 'Content-Type': 'application/json',
    # 'X-Master-Key': '$2a$10$6j/bE9qv.Fv0guqxeiYNjOZV00H3W8pGmimJV.199zoJ3/mMtyoFW'
    # }
    # data = chek_fav_pkmon() # CARGAMOS LOS DATOS COSUMIDOS DEL JSON

    print("ENTRO EN FAVORITOS")

    # CONSUSLTAMOS SI EL POKEMON EXSITE EN LA LISTA
    if new_favorite in LIST_FAV: # SI ESTA EN LA LISTA LO ELIMINAMOS
      print("Eliminando") # LIMINAMOS
      LIST_FAV.remove(new_favorite)
    else: # SI NO ESTA EN LA LISTA LO AGREGAMOS
      print("Agregado")
      LIST_FAV.append(new_favorite) # ADD NUEVO FAVORITO
    
    req = requests.put(URL_JSON_FAV, json=LIST_FAV, headers=HEADERS_JSON_FAV) # CARGAMOS LOS DATOS EN EL JSON



LIST_FAV = chek_fav_pkmon() # OBTENEMOS LA LISTA DE FAVORITOS