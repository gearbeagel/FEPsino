from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/user/', include('user.urls')),
    # path('api/blackjack/', include('blackjack.urls')),
    # path('api/dice/', include('dice.urls')),
    # path('api/slots/', include('slots.urls')),
]
