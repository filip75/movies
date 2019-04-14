#Movies API
This application utilizes OMDb API (http://www.omdbapi.com/). Application is deployed here https://movies999.herokuapp.com/
###Instalation
python pip install  
You should set following environment variables:
* MOVIES_SECRET_KEY
* MOVIES_DEBUG
* MOVIES_APIKEY  

Also while running on local machine add localhost to movies.settings.ALLOWED_HOSTS
###Endpoints
* GET /movies
* GET /movies/[id]
* POST /movies format=json {"title": _}
* GET /comments
* GET /comments/movie/[id]
* POST /comments format=json {"movie": _, "content": _}
* GET /top optional arguemnts:
    * start_date yyyy-mm-dd
    * end_date yyyy-mm-dd  
    example: http://127.0.0.1:8000/top/?start_date=2018-01-01&end_date=2018-01-02
### Unittests
To run unittests run pytest command in root directory.
### Modules used
* django
* djangorestframework - makes it really easy to build rest api (especially serializing and deserializing). As far as 
I know it's a way to go while building rest api with djanfo.
* pytest - I am most familiar with pytest.
* pytest-django - required to use pytest with django
* requests
* gunicorn - server used on Heroku
* django-heroku - needed to setup deployment to Heroku
### Things to do/imporve
* data from external api is stored as a string. Movie data should be returned as flat json
* /top endpoint unittests only test returned status, while they could also test returned data