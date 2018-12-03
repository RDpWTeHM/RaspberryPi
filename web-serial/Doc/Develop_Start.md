# Develop Start

  --

## *Overview*

[TOC]

## Contents

  ```
README
    Overview
    Contents
    TODO
    Note
    Change Log(2018)
        --
        
  ```



## TODO



## Note



## Change Log(2018)

### Dec/01


#### 23:xx create (django) server

```shell
web-serial/ $ django-admin startproject source
web-serial/ $ 
web-serial/ $ cd source && ./manage.py startapp serialcom
web-serial/ $ 
web-serial/ $ ./manage.py runserver
### test django could work ###
# !!! use "http://localhost:8000" on browser to check django server
# whether is running or not.
Ctrl+C  # quit django server
```



### Dec/02

#### 11:38 basic url setting

`source/ $ vim source/settings.py` :

```python
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', ]


# Application definition
[...]
```

`vim source/urls.py` :

```python
--- a/web-serial/source/source/urls.py
+++ b/web-serial/source/source/urls.py
@@ -16,6 +16,13 @@ Including another URLconf
 from django.contrib import admin
 from django.urls import path
 
+from django.urls import include
+from django.http import HttpResponse
+
 urlpatterns = [
     path('admin/', admin.site.urls),
+
+    path("", lambda request: HttpResponse("-> /serialcom/ app is
 avaliable!")),
+
+    path("serialcom/", include("serialcom.urls")),
 ]
```

`vim serialcom/urls.py` :

```python
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
```

`vim serialcom/views.py` :

```python
--- a/web-serial/source/serialcom/views.py
+++ b/web-serial/source/serialcom/views.py
@@ -1,3 +1,8 @@
 from django.shortcuts import render
 
 # Create your views here.
+from django.http import HttpResponse
+
+
+def index(request):
+    return HttpResponse("Hello World!")
```

