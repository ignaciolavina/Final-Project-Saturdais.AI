












____________________________________________________________________________




def test_function_from_index():
    print ("TESTING FUNCTION FROM INDEX")

    # api = requires_twitter_auth()   
    print ('\n\nUUU\n')

    tweet_id = "1232408046564970496"
    variable = db.master_case_table(db.master_case_table.tweet_id == tweet_id).select().first()
    # ret = variable.retweets



# Falta implementar el metodo que avisa, que manda el tweet
def start_tracking():
    print("\n\nSTART TRACKING API")
    print(request.vars)
    tweet_id = request.vars.tweet_id
    text_response =  request.vars.text_response

    # Recuperamos el tweet de la base de datos
    stored_element = db.tracking_table.update_or_insert(db.tracking_table.tweet_id == tweet_id,
        tweet_id = tweet_id,
        text_response = text_response,
        # date = today()
    )

    tweet = db(db.master_case_table.tweet_id == tweet_id).select().first()
    print("DABTATAS")
    # print(tweet)


    retweets = tweet.retweets
    # try catch


    # METODO ALERTA SOURCE ___________
    # https://python-twitter.readthedocs.io/en/latest/_modules/twitter/api.html#Api.PostDirectMessage
    print("\nalerting the Source")
    alert_source(tweet_id, text_response)
    # alertar_source(tweet_id)
    alerted_tweet = db.alerted_tweets.update_or_insert(db.alerted_tweets.tweet_id == tweet_id,
        tweet_id = tweet_id
    )
    
    # METODO ALERTA RETWEETS________
    print("alerting retweets")
    print("method that alerts the retweets")

    # print(type(retweets))
    retweets = json.loads(retweets)

    for ret in retweets:
        id_retweet = ret["id_str"]
        
        # METODO ALERTA

        print("alertando a: " + id_retweet)
        alerted_tweet = db.alerted_tweets.update_or_insert(db.alerted_tweets.tweet_id == id_retweet,
            tweet_id = id_retweet
        )


def alert_source(tweet_id, text_response):    
    print("Alerting source " + tweet_id)
    # Funsiona perfe
    if (text_response == ""):
        text_response = """
        Hola! Formo parte de un proyecto que se dedica a desmentir Fake News, y parece que el algoritmo ha detectado tu tweet como falso, 
        Si estoy equivocado, házmelo saber (Responde con un "NO") y así puedo mejorar, gracias!!
        """
    tweet_id = str(tweet_id)
    print("responding " + text_response)
    api = requires_twitter_auth()      
    result = api.PostUpdate(status = text_response, in_reply_to_status_id = "1241436712821235712" )



def update_retweets():
    print("\n\nupdate retweets")
    tweet_id = str(request.vars.id)

    # Recuperamos los retweets que ya existen 
    tweet = db(db.master_case_table.tweet_id == tweet_id).select().first()
    retweets_string = tweet.retweets
    retweets_list = json.loads(retweets_string)
    # print(type(retweets_list)) #LIST
    # past_retweets = [retweet.AsDict() for retweet in retweets_list]  

#     # buscamos los nuevos tweets 
#     # Get all the retweets anadir la fecha nueva
    api = requires_twitter_auth()     
    new_retweets = api.GetRetweets(tweet_id, count=15, trim_user=False)
    new_retweets_list =  [retweet.AsDict() for retweet in new_retweets]  
    # print(type(new_retweets)) # lIST
    # final_list = retweets_list
    
    
    print("len BEFORE" + str(len(new_retweets_list)))

    # Para evitar los repetidos, creamos una lista con los antiguos ids
    id_list = []
    for item in retweets_list:
        item = json.dumps(item)
        obj = Objeto_JSON(item)
        id_list.append(obj.id)
    # Si alguno de los nuevos retweets estaba en la lista, no se incluye
    print("lista ids")
    print(id_list)
    print("len BEFORE" + str(len(new_retweets_list)))
    for item in new_retweets_list:
        print("a")

        item_js = json.dumps(item)
        obj = Objeto_JSON(item_js)
        # print(type(item))

        if (obj.id in id_list):
            print("REPETIDO!! " + str(obj.id))
            new_retweets_list.remove(item)
        # else:
        #     print("NO TEPE!! " + str(obj.id))
        #     new_retweets_list.remove(item)

    print("len AFTER" + str(len(new_retweets_list)))
    # print()

    f = retweets_list + new_retweets_list
    # print(f)
    db.master_case_table.update_or_insert(db.master_case_table.tweet_id == tweet_id,
        retweets = json.dumps(f)
    )

    # # UPDATE PROCEDURE (Not working yet)    
    # lista_final_retweets = retweets_list
    # lista2 = []

    
    # print("inicial len")
    # print(len(lista_final_retweets))


    # lista2_final =  [retweet.AsDict() for retweet in lista2] 
    # lista_final_retweets.append(lista2_final)

    # print("final len")
    # print(len(lista_final_retweets))

    # a = [retweet.AsDict() for retweet in lista_final_retweets]

    # PROBLEMA, NO SE GUARDA BIEN!!
    # # # json.dumps(lista_final_retweets) NO parece ser suficiente
    # variable = db.master_case_table.update_or_insert(db.master_case_table.tweet_id == tweet_id,
    #     retweets = json.dumps(lista_final_retweets)
    # )



# ____________________________ STORING ON THE DB _______________________________________

# method created 18-Feb-2020
def add_to_database():
    print("\n\nadd to DATABASE method") 

    api = requires_twitter_auth()     
    
    #retrieveing the tweet from the client POST in json string
    tweet_json = request.vars.tweet
    # Convert to python object
    tweet = Objeto_JSON(tweet_json)

    # tweet = tweet_objeto #to work with

    # Get the data from the tweet
    title = tweet.full_text
    urls = tweet.urls
    # The valid ID is the tweet.id_string in Integer format
    # id = int(tweet.id_str)
    id = tweet.id_str

    # status = api.GetStatus(int(tweet.id_str))
    
    # Params for api methods
    number_of_rt = 30

    # Get all the retweets
    retweets = api.GetRetweets(id, count=number_of_rt, trim_user=False)
    retweets =  [retweet.AsDict() for retweet in retweets]  

    print(retweets)


    # Get the user to object to work with 
    user_string = json.dumps(tweet.user)
    user_objeto = Objeto_JSON(user_string)
    user_name = user_objeto.name
    print (user_name)


    print("PRE")
    stored_user = db.tweet_users_table.update_or_insert(db.tweet_users_table.name == user_name,
        name = user_name,
        user_data = user_string
    )

    print("storede user")
    print(stored_user)

    # other_tweets = api.GetSearch()
    # Remember to use the id (tweet.id_str)

    variable = db.master_case_table.update_or_insert(db.master_case_table.tweet_id == id,
        title = tweet.full_text,
        utls = tweet.urls,
        tweet_id = id,
        tweet_user = stored_user,
        tweet = tweet_json,
        retweets = json.dumps(retweets)
    )
    # Redirect not working
    # return redirect(URL('default', 'fake_news_panel'))
# ____________________________________________________________________________________



# DEPRECATED!!!!!
# def store_data():
#     api = requires_twitter_auth()            
#     print ('\n\nUUU\n')

#     # Get tweets
#     tweets = api.GetSearch(term="taza", count=1)
#     tweets = [tweet.AsDict() for tweet in tweets]

#     for tweet in tweets:
#         tweet_json = json.dumps(tweet)
#         tweet_objeto = Objeto_JSON(tweet_json)
#         print (tweet_objeto.id)

#         # get retweets
#         number_of_rt = 50
#         retweets = api.GetRetweets(tweet_objeto.id, count=number_of_rt, trim_user=False)
#         retweets =  [retweet.AsDict() for retweet in retweets]    

#         variable = db.data_table.update_or_insert(
#             stored_data = json.dumps(tweet),
#             retweets = json.dumps(retweets)
#         )




# definimos una clase, que convierte JSON en objeto
class Objeto_JSON(object):
    def __init__(self, data):
	    self.__dict__ = json.loads(data)


def get_logged_in_user():
    user = None if auth.user is None else auth.user
    return response.json(dict(user=user))

    # GET RETWEETS 
    # https://api.twitter.com/1.1/statuses/home_timeline.json
    # getRetweet

    # Usar un embellecedor
    # @requires_twitter_logged

# OWN DECORATOR


# TO-DO
# En el metodo una vex esta loggeado en twitter con las credentials, hacer un get request normal
# como en la pagina del drive (problemas & soluciones), del tio que hace
# @GET(url, q=word?&count=ffff) y ver el resultado
# (bypass teweetpy api)

# ___________________________ SEARCH BY USER ____________________________________

def search_by_user():
        
    api = requires_twitter_auth()      
    user_to_search =  request.vars.user_to_search
    # user_to_search = ""

    # Number of retweets to retrieve
    count = 10

    # Api method to search the user. It is valid either by user Id or by @Twitter_shortname
    tweets_timeline = api.GetUserTimeline(screen_name = user_to_search, count = count)
    data = [tweet.AsDict() for tweet in tweets_timeline]
    

    return response.json(dict(data = data))


# ____________________________________________________________________________________
def extract_title(url):
    import requests
    from bs4 import BeautifulSoup as bs

    # url = 'http://www.oldbaileyonline.org/browse.jsp?id=t17800628-33&div=t17800628-33'
    url = "https://t.co/83chfo0PL9"
    # url2 = "https://maldita.es/malditobulo/quaden-bayles-enanismo-acondroplasia-disneyland-estafa-australia/?utm_content=buffercab8b&utm_medium=social&utm_source=twitter.com&utm_campaign=buffer"

    r = requests.get(url)
    soup = bs(r.content, 'lxml')
    title = soup.select_one('title').text
    # print(title)

    # QUITAMOS LOS ICONOS
    import re
    emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            "]+", flags=re.UNICODE)
    print(emoji_pattern.sub(r'', title)) # no emoji



# def get_similar_tweets():
    # si los tengo los cojo de la db
    # sino los extraigo
    # todo esto de acuerdo a la fecha de last_update
    # informo de los nuevos tweets encontrados

def get_similar_tweets():   
    print(request.vars)

    text = request.vars.text
    id = request.vars.id
    username = "-@" + str(request.vars.username)
    text = text + username

    # Si no hay texto que buscar
    if((text is None) or (text == "")):
        return response.json(dict(data = data, success = False))


    # Si ya existen en la base de datos
    if (False):
        # NOT WORKING YET
        print(id)
        print(type(id))
        results = db(db.master_case_table.tweet_id == id)
        print("\n\nSIMILAR")
        print(results)
        similar_tweets = [tweet.AsDict() for tweet in results]
        similar_tweets = json.dumps(results)
    else:
        api = requires_twitter_auth()   
        results = api.GetSearch(text, count = 1)

        similar_tweets = [tweet.AsDict() for tweet in results]
        # Falta guardarlo en la base de datos
    


    return response.json(dict(similar_tweets = similar_tweets))

# _______________________________________________________________________________



# CONTROL de RATES



def requires_twitter_auth():
    # print('decorator activated [Auth]')
    print("AUTH PROCESS ACTIVATED")
    
    consumer_key = 'dXj0dViDbK6VobzAD5P97iCrO'
    consumer_secret = 'DwRbuw8rRgMBh6Gg9qORDXpDJ4RLp0wGq4RWj5SVw4KJT6nDZq'
    access_token = '1164482563198636033-PMEvNG9Pz1aGL3SLKw1QX9TwjStdD5'
    access_secret = '1sYd9Mp8IS6TTXaD0nzgtXguFiABf4eSjvXVPf8va05uG'

    api = twitter.Api(consumer_key = consumer_key,consumer_secret = consumer_secret
    , access_token_key = access_token, access_token_secret = access_secret, sleep_on_rate_limit=True, tweet_mode ="extended")

    # from pprint import pprint
    # pprint(vars(api))

    # print ('\n\nPrinting rate limits objetc inside api')
    # rate_limit = api.rate_limit    
    # pprint(vars(rate_limit))

    
    # print ('\n\nPrinting rate limits per se')
    # pprint(vars(twitter.ratelimit.RateLimit()))

    return api

def log_on_twitter():
    print('\nloggin on twitter')
    api = requires_twitter_auth()
    print(api.VerifyCredentials())


def post_tweet():
    print('post tweet api method')

    requires_twitter_auth()
    string =request.vars.string

    api = twitter.Api(consumer_key = consumer_key,consumer_secret = consumer_secret
    , access_token_key = access_token, access_token_secret = access_secret)

    status = api.PostUpdate(string)
    print('end method')



def get_data():
    # Get the Params
    row_number = int(request.vars.id)
    print("row number")
    print(row_number)

    # Get data from database
    data = db(db.master_case_table.id == row_number).select().first()
    print(data)

    return response.json(dict(data = data))



# ____________________ TEST NO BORRAR _______________________ 
# Para usar esta funcion desting, COMENTAR get_data y descomentar esta
# def get_data():
#     testing = True
#     data = []

#     if testing:
#         data = db(db.data_table).select().first()
#         # print(db(db.data_table.id == 0).select().first())
#     print("data access2")
#     print(data)
#     return response.json(dict(data = data))
# __________________________________________________________________


def clean_word(word):
    text = word
    text = text.split()
    texto_completo = ""
    for t in text:
        texto_completo = texto_completo + " +" + t
    return texto_completo

# Warning los retweets estan con trim_user=True, testear otras opciones
# -TODO
    # - get the number of tweets from client
    # - try catchs
def get_tweet():
    print('\n\nget tweet method')    
    # get the query for search on twitter
    word = request.vars.word

    word = clean_word(word)

    test_mode = request.vars.test_mode

    # Since False != false (JS VS Python)
    testing = False
    if test_mode == 'false':
        testing = False
        
    print(testing)

    if testing:
        # api = requires_twitter_auth()  
        print ('Testing')
        # tweets = get_tweet_json()  
        # retweets = get_retweets_json()
        list_tweets_and_retweets = get_list_tweets_and_retweets_json()
        # To avoid erros, intialize the lsits to return as request.vars
        tweets = []
        retweets = []
        retweets_two = []
        # list_tweets_and_retweets = db(db.list_tweets_retweets.id == 0).select().first()
        # list_tweets_and_retweets = json.dumps(list_tweets_and_retweets)
        # p.nombre_jugador_uno = db(db.jugador.id == p.jugador_uno).select().first().nombre  


    else:
        api = requires_twitter_auth()            
        print ('\n\nUUU\n')

        # Get tweets
        tweets = api.GetSearch(term=word, count=5)    
        tweets = [tweet.AsDict() for tweet in tweets]

        # list of couples [(tweet1, retweeets1), (tweet2, retweeets2), (...)]
        list_tweets_and_retweets = []

        for tweet in tweets:
            tweet_json = json.dumps(tweet)
            tweet_objeto = Objeto_JSON(tweet_json)
            print (tweet_objeto.id)
            
            # Get retweets
            number_of_rt = 50
            retweets = api.GetRetweets(tweet_objeto.id, count=number_of_rt, trim_user=False)

            retweets =  [retweet.AsDict() for retweet in retweets]
            
            # Adding everything in a big list to return as request vars
            list_tweets_and_retweets.append([tweet, retweets])

            # CreateFriendship(self, user_id=None, screen_name=None, follow=True, retweets=True, **kwargs)
            # print(CreateFriendship(self, user_id=None, screen_name=None, follow=True, retweets=True, **kwargs))



        # # Test
        retweets_two = get_retweets_json()
        datos = json.dumps(list_tweets_and_retweets)

        # Store data on the database
        variable = db.tabla_tweets_retweets.update_or_insert(
            stored_data = json.dumps(list_tweets_and_retweets)
        )

        twitter_api = ''

        # print (variable)
        # pareja = db.pareja.update_or_insert(db.pareja.id == request.vars.id,
        # grupo = request.vars.grupo
        # )
        
        # Saved in saved.txt
        # path=os.path.join(request.folder,'private','saved.txt')
        # # fullStr = ' '.join(list_tweets_and_retweets)
        # fullStr = json.dumps(list_tweets_and_retweets)
        # f = open(path, "a")
        # f.write(fullStr)
        # f.close()
        
    # return results as JSON
    # Order list by ascendent date
    # retweets = retweets[::-1]
    return response.json(dict(tweets=tweets, retweets=retweets_two, list_tweets_and_retweets = list_tweets_and_retweets))


# Store data on the database
def save_data():
    # Retrieve the data and prepare the variables
    stored_data = request.vars.stored_data
    error = None

    if ((stored_data is None) or (stored_data == '')):
        error = 'Data to store was empty, nothing stored'
        return response.json(dict(result = False, error = error))

    # Storing data
    variable = db.tabla_tweets_retweets.insert(
        stored_data = stored_data
    )

    # Return True if data is stored correctly
    if (variable is None):
        error = 'Error when storing data'
        return response.json(dict(result = False, error = error))

    return response.json(dict(result = True, error = error))


def mark_as_fake():
    print('marked as fake')    
    stored_data = request.vars.stored_data
    topic = request.vars.topic
    search_line = request.vars.search_line

    if ((stored_data is None) or (stored_data == '')):
        error = 'Data to store was empty, nothing stored'
        return response.json(dict(result = False, error = error))

    # Storing data
    variable = db.fake_news_table.insert(
        stored_data = stored_data,
        search_line = search_line
    )

    # Return True if data is stored correctly
    if (variable is None):
        error = 'Error when storing data'
        return response.json(dict(result = False, error = error))

    return response.json(dict(result = True, error = None))

#           TESTING PURPOSES
# ____________________________________________________________________________________
# The next methods have been created only for testing purposes

def test_index_function():
    print('test function')


# To avoid doing all the tima calls to api
def get_retweets_json():
    path=os.path.join(request.folder,'private','retweets_long.txt')
    with open(path) as json_file:
        retweets = json.load(json_file)
    return retweets

def get_tweet_json():
    path=os.path.join(request.folder,'private','tweet.txt')
    with open(path) as json_file:
        tweet = json.load(json_file)
    return tweet

def get_list_tweets_and_retweets_json():
    path=os.path.join(request.folder,'private','saved.txt')
    with open(path) as json_file:
        list_tweets_and_retweets = json.load(json_file)
    return list_tweets_and_retweets

























# ____________________________________________________________________________________
# Methods for jugadores.html view
def get_jugadores():
    jugadores = db(db.jugador).select()
    return response.json(dict(jugadores=jugadores))

def change_pagado():
    jugador = db(db.jugador.id == request.vars.id).update(pagado = request.vars.pagado)

def change_regalo():
    jugador = db(db.jugador.id == request.vars.id).update(regalo = request.vars.regalo)
# ____________________________________________________________________________________


# Methods for parejas.html
# ____________________________________________________________________________________
def get_parejas():
    parejas = db().select(db.pareja.ALL, orderby=db.pareja.grupo)
    for p in parejas:
        jugador_uno = db(db.jugador.id == p.jugador_uno).select().first()
        jugador_dos = db(db.jugador.id == p.jugador_dos).select().first()
        p.nombre_jugador_uno = jugador_uno.nombre
        p.restricciones_jugador_uno = jugador_uno.restricciones     
        p.nombre_jugador_dos = jugador_dos.nombre
        p.restricciones_jugador_dos = jugador_dos.restricciones      
    return response.json(dict(parejas=parejas))

def update_pareja():
    pareja = db.pareja.update_or_insert(db.pareja.id == request.vars.id,
    grupo = request.vars.grupo
    )
    db.jugador.update_or_insert(db.jugador.id == request.vars.jugador_uno,
    nombre= request.vars.nombre_jugador_uno,
    restricciones = request.vars.restricciones_jugador_uno
    )
    db.jugador.update_or_insert(db.jugador.id == request.vars.jugador_dos,
    nombre= request.vars.nombre_jugador_dos,
    restricciones = request.vars.restricciones_jugador_dos
    )

def delete_pareja():
    id = request.vars.id
    db(db.pareja.id == request.vars.id).delete()
    db(db.jugador.id == request.vars.jugador_uno).delete()    
    db(db.jugador.id == request.vars.jugador_dos).delete()

# ____________________________________________________________________________________


# ____________________________________________________________________________________
# Methods for nueva_pareja.html view
def save_pareja():
        jug_uno = db.jugador.insert(
            nombre=request.vars.jugador_uno,
            restricciones = request.vars.restricciones_uno  
        )
        jug_dos = request.vars.jugador_dos
        if (jug_dos == ''):
            jug_dos = 'Por determinar'
        jug_dos = db.jugador.insert(
            nombre = jug_dos,
            restricciones = request.vars.restricciones_dos
            )
        grupo = request.vars.grupo
        if (grupo == ''):
            grupo = 0
        pareja = db.pareja.insert(
            jugador_uno=jug_uno,
            jugador_dos=jug_dos,
            grupo = grupo
        )
        # print('pareja saved')

        # return redirect(URL('default', 'jugadores'))

        # print(jug_uno, jug_dos, grupo)
        if (jug_uno and jug_dos and pareja):
            return True
        else:
            return False
# ____________________________________________________________________________________


# ____________________________________________________________________________________
# For grupos.html view
def get_grupos():
    lista = []
    counter = 1 
    max_group = 0

    parejas_sin_grupo = db(db.pareja.grupo == 0).select()
    for p in parejas_sin_grupo:
        p.nombre_jugador_uno = db(db.jugador.id == p.jugador_uno).select().first().nombre                
        p.nombre_jugador_dos = db(db.jugador.id == p.jugador_dos).select().first().nombre
        

    while (counter < 20):
        parejas = db(db.pareja.grupo == counter).select()
        if (parejas):
            for p in parejas:
                p.nombre_jugador_uno = db(db.jugador.id == p.jugador_uno).select().first().nombre                
                p.nombre_jugador_dos = db(db.jugador.id == p.jugador_dos).select().first().nombre
            crear_enfrentamientos(parejas)
            lista.append(parejas)
            counter+=1
        else:
            counter+=1
    max_group = counter - 1
    return response.json(dict(parejas = lista, max_group = max_group, parejas_sin_grupo = parejas_sin_grupo))

def update_group_for_pareja():
    id_pareja = request.vars.index
    pareja = db.pareja.update_or_insert(db.pareja.id == id_pareja,
    grupo = request.vars.grupo
    )    

    db(db.enfrentamiento).delete()
    # pareja.nombre_jugador_uno = 'make' # db(db.jugador.id == p.jugador_uno).select().first().nombre                
    # pareja.nombre_jugador_dos = 'lele' #db(db.jugador.id == p.jugador_dos).select().first().nombre


# ____________________________________________________________________________________
# Methods for partidos.html view
def crear_enfrentamientos(parejas):
    for i in range(len(parejas)):
        for j in range(i+1, len(parejas)):
            # print("enfrentamiento: ", parejas[i].id , " VS ", parejas[j].id )
            db.enfrentamiento.update_or_insert(grupo = parejas[i].grupo, pareja_uno=parejas[i].id, pareja_dos=parejas[j].id)
        

def save_result():
    stored = db.enfrentamiento.update_or_insert(
        db.enfrentamiento.id == request.vars.index,
        resultado_uno = request.vars.result_one,
        resultado_dos = request.vars.result_two 
    )
# ____________________________________________________________________________________
    
    
def get_partidos():
    # retrieveing jugadores from DB for display the names in the view
    jugadores = db(db.jugador).select()
    parejas = db(db.pareja).select()

    lista = []
    counter = 1 
    max_group = 0
    # "problema cuando no falta un grupo"
    while (counter < 20):
        enfrentamiento = db(db.enfrentamiento.grupo == counter).select()
        # print (parejas)
        if (enfrentamiento):
            for e in enfrentamiento:
                # De cada enfrentamiento, extraer pareja uno y dos
                p1_id = parejas.find(lambda pareja: pareja.id == e.pareja_uno)            
                p2_id = parejas.find(lambda pareja: pareja.id == e.pareja_dos)
                # De cada pareja, extraer los nombres uno y dos
                nombres_pareja_uno = jugadores.find(lambda jugador: jugador.id == p1_id[0].jugador_uno)[0].nombre + ' & ' + jugadores.find(lambda jugador: jugador.id == p1_id[0].jugador_dos)[0].nombre
                nombres_pareja_dos = jugadores.find(lambda jugador: jugador.id == p2_id[0].jugador_uno)[0].nombre + ' & ' + jugadores.find(lambda jugador: jugador.id == p2_id[0].jugador_dos)[0].nombre
                # print(nombres_pareja_)
                e.nombres_pareja_uno = nombres_pareja_uno
                e.nombres_pareja_dos = nombres_pareja_dos
            lista.append(enfrentamiento)
            counter+=1
        else:
            counter+=1
    max_group = counter - 1
    return response.json(dict(enfrentamiento = lista, max_group = max_group))


# Methdos for resultados.html view
# ____________________________________________________________________________________

def get_results():
    # Partidos ganados, perdidos, JF jC Dif juegos, Posicion
    # print('\n\nGET RESULTS')
    lista_enfrentamientos = []
    lista_parejas = []
    counter = 1 
    max_group = 0
    # "problema cuando no falta un grupo"
    while (counter < 20):
        enfrentamientos = db(db.enfrentamiento.grupo == counter).select()        
        parejas = db(db.pareja.grupo == counter).select()
        for p in parejas:
            p.nombre_jugador_uno = db(db.jugador.id == p.jugador_uno).select().first().nombre                
            p.nombre_jugador_dos = db(db.jugador.id == p.jugador_dos).select().first().nombre
        # print (parejas)
        if (enfrentamientos):
            lista_enfrentamientos.append(enfrentamientos)
            lista_parejas.append(parejas)
            counter+=1
        else:
            counter+=1
    max_group = counter - 1
    return response.json(dict(enfrentamientos = lista_enfrentamientos, parejas = lista_parejas, max_group = max_group))

# def delete():    
    # db(db.pareja.grupo == None).delete()
