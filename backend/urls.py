"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic.base import TemplateView


from acctz import views as core_views
from shop import views as shop_views
from users import views as users_views
from links import views as link_views

import backend.views as views

urlpatterns = [
    # redirects from old links
    path('project/Snake-Neural-Network-Fusion-in-Python/', lambda request: HttpResponseRedirect('https://jon.network/project/37/Snake-Neural-Network-Fusion-in-Python/')),
    path('programming-projects/', lambda request: HttpResponseRedirect('https://jon.network/programming-articles/')),
    path('programming-projects/<str:p>/', lambda request, p: HttpResponseRedirect('https://jon.network/programming-articles/{}/'.format(p))),
    path('project/<str:s>/', lambda request, s: HttpResponseRedirect('https://jon.network/programming/{}/'.format(s))),
    path('project/<int:i>/<str:s>/', lambda request, i, s: HttpResponseRedirect('https://jon.network/programming/{}/{}/'.format(i, s))),
    path('project/<int:i>/<str:s>/edit/', lambda request, i, s: HttpResponseRedirect('https://jon.network/programming/{}/{}/edit/'.format(i, s))),
    
    #main
    path('', views.index),
    path('links/', link_views.index),
    path('links/<str:catagory>/', link_views.link_share),
    path('programming-articles/', shop_views.items),
    path('acct/', include('allauth.urls')),
    path('programming/', include('shop.urls')),
    path('chat/', include('chatroom.urls')),
    path('forum/', include('forum.urls')),
    path('scriptlytics/', include('scriptlytics.urls')),
    path('programming-articles/<str:langu>/', shop_views.search_by_lang),
    path('user/', users_views.user_page),
    path('users/', users_views.user_index),
    path('user/<str:un>/', core_views.user_profile, name="user"),
    path('edit-profile/', users_views.edit_prof),
    path('ide/', views.ide),
    path('admin/', admin.site.urls),
    path('admin-emails/', users_views.email_addrs),
    
    # apis
    # path('api/', include('api.urls')), <------ Moved to https://ravencoin.herokuapp.com
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
