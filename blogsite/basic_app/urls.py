from django.conf.urls import url
from basic_app import views

app_name ='basic_app'

urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^$',views.greet,name='greets'),
    url(r'^login/$',views.user_login,name='user_login'),
    url(r'^profile/$',views.profile_view,name='profile_view'),
]
