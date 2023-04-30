from django.shortcuts import render
from django.shortcuts import redirect

from . import util
from markdown import Markdown
from django import forms
import random



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def CSS(request):
    return general(request,"CSS")

def Django(request):
    return general(request,"Django")

def Git(request):
    return general(request,"Git")

def HTML(request):
    return general(request,"HTML")

def Python(request):
    return general(request,"Python")

def general(request,name):
    #to convert markdown to html
    markdowner = Markdown()
    content = util.get_entry(name)

    #if entry name does not exist
    if content is None:
        Error = 'Error! Entry Name does not exist'
        return render(request,"encyclopedia/error.html",{
            "Error":Error
        })
    
    return render(request, "encyclopedia/"+name+".html",{
        "convertedcontent":markdowner.convert(content),
        "title":name
    })

def search(request):
    #getting the query that user typed in the form
    query = request.POST['q']

    #if user typed a query 
    if query:
        #if query is one of the entries, redirect to page for that query
        if query in util.list_entries():
            return redirect('general', name=query)
        
        #if query is not any of the entries but is substring of any of entries
        else:
            entries = util.list_entries()
            matches = [entry for entry in entries if query.upper() in entry.upper()]
            return render(request, "encyclopedia/index.html",{
                "entries":matches
            })
        
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

class NewTaskForm(forms.Form):
    Title = forms.CharField(label="Enter Title")

def newpage(request):
    if request.method=="POST":
        #filling a new form with the user's input
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["Title"]
            #if title already exists, return error message
            if title in util.list_entries():
                Error = "Error! Title already exists"
                return render(request,"encyclopedia/error.html",{
                    "Error":Error
                })
            
            #if title does not exist, then save it as a new entry
            else:
                mdcontent = request.POST["mdcontent"]
                util.save_entry(title, mdcontent)
                return redirect('newentry', title=title)
    
    if request.method == "GET":
        return render(request,"encyclopedia/newpage.html",{
            "form":NewTaskForm()
        })
                
def newentry(request,title):
    markdowner = Markdown()
    mdcontent = util.get_entry(title)
    return render(request,"encyclopedia/newentry.html",{
                "Title": title,
                "MDcontent": markdowner.convert(mdcontent)
            })

def editmdcontent(request,title):
    if request.method == "GET":
        mdcontent = util.get_entry(title)
        return render(request,"encyclopedia/editmdcontent.html",{
            "title":title,
            "mdcontent":mdcontent
        })
    #if request method is POST
    else: 
        editedmdcontent = request.POST['editedmdcontent']
        markdowner = Markdown()
        util.save_entry(title,editedmdcontent)
        return render(request,"encyclopedia/"+title+".html",{
            "title":title,
            "convertedcontent":markdowner.convert(editedmdcontent)
        })

def randompage(request):
    randomentry = random.choice(util.list_entries())
    markdowner = Markdown()
    content = util.get_entry(randomentry)
    return render(request,"encyclopedia/randompage.html",{
        "title":randomentry,
        "convertedcontent":markdowner.convert(content)

    })





    








