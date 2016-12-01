## A crowdsourcing app for AccessMap Project

### Run locally
    For virtual environment (optional):
    virtualenv env 
    source env/bin/activate
    
    Running (localhost:8000):
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    
    How to load interactions from csv file into database (one time):
    python manage.py shell
    from crowdsourcing.utils import get_intersection
    get_intersection()

## Reference

[How to Use Django's Built-in Login System](https://github.com/sibtc/simple-django-login)

[Leaflet.Draw](https://github.com/michaelguild13/Leaflet.draw)

[django-leaflet/example](https://github.com/makinacorpus/django-leaflet/tree/master/example)
