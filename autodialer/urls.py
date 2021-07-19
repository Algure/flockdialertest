
from django.contrib import admin
from django.urls import path

import dialerapp.api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/user/create/', dialerapp.api_views.UserCreate.as_view()),
    # path('api/user/query/', dialerapp.api_views.UserList.as_view()),

]
