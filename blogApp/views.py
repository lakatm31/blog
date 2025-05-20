from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import read_json_to_list, write_entry_to_json, delete_entry_from_json
from datetime import datetime

JSON_FILE_PATH = r'C:\Python\2025\blog\Blog\bejegyzesek.json'

def home(request):
    entries = read_json_to_list(JSON_FILE_PATH)
    return render(request, 'home.html', {'entries': entries})

# Blog home page, visible only to logged-in users
@login_required
def blog_home(request):
    entries = read_json_to_list(JSON_FILE_PATH)
    return render(request, 'blog_home.html', {'entries': entries})

# Add entry, visible only to logged-in users
@login_required
def add_entry(request):
    if request.method == 'POST':
        author = request.user.username  # Use the logged-in user's username
        content = request.POST.get('content')
        color = request.POST.get('color', '#FFFFFF')

        if not content:
            return render(request, 'add_entry.html', {'error': 'Content is required'})

        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Write entry to JSON file with timestamp
        write_entry_to_json(author, content, color, timestamp, JSON_FILE_PATH)
        return redirect('blog_home')

    return render(request, 'add_entry.html')

def ellenorzes(password):
    if len(password) < 6:
        return False
    nagybetu = False
    szam = False
    for betu in password:
        if betu.isupper():
            nagybetu = True
        if betu.isdigit():
            szam = True
    return nagybetu and szam        




# Log in view
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user) # Authenticate the user
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('blog_home')  # Redirect to blog home after successful login
        else:
            return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Log out view
def user_logout(request):
    logout(request)
    return redirect('home')  # Redirect to login page after logging out

# Sign-up view for creating a new user
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        password = form.data.get("password1")
        password_confirm = form.data.get("password2")

        if password != password_confirm:
            return render(request, 'signup.html', {
                'form': form,
                'error': 'A jelszavak nem egyeznek.'  # Passwords do not match
            })

        if not ellenorzes(password):
            return render(request, 'signup.html', {
                'form': form,
                'error': 'A jelszónak legalább 6 karakter hosszúnak kell lennie, tartalmaznia kell nagybetűt és számot.'
            })

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
# Delete entry, visible only to logged-in users
@login_required

def delete_entry(request, entry_id):
    entries = read_json_to_list(JSON_FILE_PATH)
    try:
        entry = entries[int(entry_id)]
        # Check ownership here 
        if entry['author'] != request.user.username:
            messages.error(request, "You can only delete your own entries.")
            return redirect('blog_home')
        
        delete_entry_from_json(entry, JSON_FILE_PATH)
        messages.success(request, "Entry deleted successfully.")
    except (ValueError, IndexError):
        messages.error(request, "Invalid entry ID or entry not found.")
    
    return redirect('blog_home')

