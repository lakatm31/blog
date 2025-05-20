from django.urls import path
from .views import blog_home, add_entry, delete_entry, user_login, user_logout, user_signup, home

urlpatterns = [
    path('blog_home/', blog_home, name='blog_home'),
    path('',home, name='home'),  # Home URL'),
    path('add_entry/', add_entry, name='add_entry'),
    path('delete_entry/<str:entry_id>/', delete_entry, name='delete_entry'),
    path('login/', user_login, name='login'),  # Login URL
    path('logout/', user_logout, name='logout'),  # Logout URL
    path('signup/', user_signup, name='signup'),  # Sign-up URL
]
