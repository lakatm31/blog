from django.shortcuts import render, redirect
import logging, json
from .utils import read_json_to_list, write_entry_to_json,delete_entry_from_json
from datetime import datetime

logger = logging.getLogger(__name__)

JSON_FILE_PATH = 'C:/Python/2025/blog/Blog/bejegyzesek.json'

def blog_home(request):
    entries = read_json_to_list(JSON_FILE_PATH)
    return render(request, 'blog_home.html', {'entries': entries})

def add_entry(request):
    if request.method == 'POST':
        author = request.POST.get('author')
        content = request.POST.get('content')
        color = request.POST.get('color', '#FFFFFF')

        if not author or not content:
            return render(request, 'add_entry.html', {'error': 'Author and content are required'})

        write_entry_to_json(author, content, color, JSON_FILE_PATH)
        logger.info(f"New entry added by {author} at {datetime.now()}")
        return redirect('blog_home')

    return render(request, 'add_entry.html')

def delete_entry(request, entry_id):
    if request.method == 'POST':  # Ensure only POST requests can delete entries
        try:
           # entry_id = float(entry_id)  
            delete_entry_from_json(entry_id, JSON_FILE_PATH)  # Use the global JSON_FILE_PATH
        except ValueError:
            logger.error(f"Invalid entry ID: {entry_id}")
    return redirect('blog_home')
