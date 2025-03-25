from django.urls import path
from .views import blog_home, add_entry,delete_entry

urlpatterns = [
    path('blog_home/', blog_home, name='blog_home'),
    path('add_entry/', add_entry, name='add_entry'),
    path('delete_entry/<str:entry_id>/', delete_entry, name='delete_entry'),  # Commented out
]
