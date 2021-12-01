from django.urls import path

from . import views

from . views import (
    ChatListView,
    ChatDetailView,
    ChatCreateView,
    ChatUpdateView,
    ChatDeleteView,
)

app_name = 'Chat'

urlpatterns = [
    path('', ChatListView.as_view()),
    path('create/', ChatCreateView.as_view()),
    path('<pk>/', ChatDetailView.as_view()),
    path('<pk>/update/',ChatUpdateView.as_view()),
    path('<pk>/delete/', ChatDeleteView.as_view()),
    path('profile',views.UserView.as_view()),
    path('profile/<str:username>',views.UserViewPk.as_view()),
]
