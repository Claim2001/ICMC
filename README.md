# ICMC
Информационная система маломерных судов для Министерства по чрезвычайным ситуациям. (rus desc)

Project that makes ship registration easier for government and shipowners.

# Gettings started

First of all you need to copy the repository to your machine
```
git clone https://github.com/DilsMatchanov/ICMC.git

cd ./ICMC
```

Activate the virtual environment
```
source projectenv/bin/activate
```

Install all packages
```
pip install -r requirements.txt
```

Migrate the database
```
python manage.py migrate
```

And finally run the server
```
python manage.py runserver
```
