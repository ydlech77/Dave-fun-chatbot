from django.urls import path
from . import views  # ✅ relative import

urlpatterns = [
    path('', views.chat_view, name='chat'),  # main chat page
]
