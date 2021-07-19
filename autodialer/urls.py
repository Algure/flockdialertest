
from django.contrib import admin
from django.urls import path

import dialerapp.api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/create/', dialerapp.api_views.UserCreate.as_view(),),
    path('api/user/query/', dialerapp.api_views.UserList.as_view()),
    path('api/user/<int:id>', dialerapp.api_views.UserRetrieveUpdateDestroy.as_view()),
    path('api/company/create/', dialerapp.api_views.CompanyCreate.as_view(),),
    path('api/company/query/', dialerapp.api_views.CompanyList.as_view()),
    path('api/company/<int:id>', dialerapp.api_views.CompanyRetrieveUpdateDestroy.as_view())
]
