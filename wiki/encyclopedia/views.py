from random import choice
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from markdown import markdown
from django import forms

from . import util

class SearchForm(forms.Form):
    q = forms.CharField(required=True)

class NewPageForm(forms.Form):
    title = forms.CharField(required=True)
    text = forms.CharField(required=True)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def wiki(request, title):
    text = util.get_entry(title)
    if text:
        final_text = markdown(text)
        return render(request, "encyclopedia/wiki.html", {
        "title":title, 
        "text": final_text,
        "raw_text": text,
        "found": True
    })
    return render(request, "encyclopedia/wiki.html", {
        "title": title, 
        "text": "<h1>404 Not Found</h1> <p>The page you are looking for doesn't exist</p><a href='/'>Back to home</a>"
    })

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data["q"]
            text = util.get_entry(q)
            if text:
                return HttpResponseRedirect(f"/wiki/{q}")
        else:
            return render(request, "encyclopedia/msg.html", {"text": "Invalid data. Try again"})
            
        entries = util.list_entries()
        options = []
        for entry in entries:
            if q.lower() in entry.lower():
                options.append(entry)
        return render(request, "encyclopedia/search_results.html", {
            "options": options,
            "query": q
        })


def random(request):
    options = util.list_entries()
    title = choice(options)
    return HttpResponseRedirect(f"/wiki/{title}")

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")

    form = NewPageForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data.get("title")
        text = form.cleaned_data.get("text")
        util.save_entry(title, text)
        return render(request, "encyclopedia/msg.html", {"text": "Page created!"})

def edit_page(request):
    if request.method == "GET":
        form = NewPageForm(request.GET)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            text = form.cleaned_data.get("text")
            return render(request, "encyclopedia/edit.html", {"title": title, "text": text})
    
    form = NewPageForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data.get("title")
        text = form.cleaned_data.get("text")
        util.save_entry(title, text)
        return render(request, "encyclopedia/msg.html", {"text": "Page edited!"})
    else:
        return render(request, "encyclopedia/msg.html", {"text": "Invalid data. Try again"})