from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

@login_required  # Ensures only logged-in users can access this view
def index(request): 
    # Fetch folders for the logged-in user
    folders = Folder.objects.filter(folderuser=request.user)
    context = {'folders': folders}
    
    # Render the appropriate template with the context
    return render(request, 'cloud_drive_app/index.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from .models import Folder,File
from django.contrib.auth.decorators import login_required

@login_required
def folder(request, folderid):
    # Get the folder object or return a 404 if not found
    folder_user = get_object_or_404(Folder, id=folderid, folderuser=request.user)
    files = File.objects.filter(folder=folder_user)
    context = {'folderid': folderid, 'files': files, 'folder': folder_user}

    if request.method == 'POST':
        file_user = request.FILES.get('file')
        file_title = request.POST.get('filetitle')

        if file_user and file_title:
            try:
                File.objects.create(
                    filetitle=file_title,
                    file=file_user,
                    folder=folder_user
                )
                messages.success(request, "File uploaded successfully!")
                return redirect('folder', folderid=folderid)  # Refresh to show the uploaded file
            except Exception as e:
                messages.error(request, f"Error uploading file: {e}")
        else:
            messages.error(request, "File title and file are required.")

    return render(request, 'cloud_drive_app/folder.html', context)
# Add Folder View
@login_required  # Ensure only logged-in users can create folders
def addfolder(request):
    if request.method == 'POST':
        folder_name = request.POST.get('foldername')
        folder_desc = request.POST.get('desc')

        if folder_name:  # Ensure the folder name is not empty
            try:
                folder = Folder.objects.create(
                    foldername=folder_name,
                    folderdesc=folder_desc,
                    folderuser=request.user
                )
                messages.success(request, "Folder created successfully!")
                return redirect("index")
            except Exception as e:
                messages.error(request, f"Error creating folder: {e}")
        else:
            messages.error(request, "Folder name cannot be empty.")
        
        return redirect("index")
    else:
        return redirect("index")
    
    
from .models import Folder
@login_required
def folder_list(request):
    if request.user.is_authenticated:
        folders = Folder.objects.filter(folderuser=request.user)
        context = {'folders': folders}
        return render(request, 'folder_manager/folder_list.html', context)
    else:
        return redirect('login')  # Redirect to login if user is not authenticated

        
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout       

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            cpassword = request.POST['cpassword']
            firstname = request.POST['fname']
            lname = request.POST['lname']
            if username and password and email and cpassword and firstname and lname:
                if password == cpassword:
                    user = User.objects.create_user(username,email,password)
                    user.first_name = firstname
                    user.last_name = lname
                    user.save()
                    if user:
                        messages.success(request,"User Account Created")
                        return redirect("login")
                    else:
                        messages.error(request,"User Account Not Created")
                else:
                    messages.error(request,"Password Not Matched")
                    redirect("register")
        return render(request,'cloud_drive_app/register.html')
 
# View For Log in the user
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Correct way to call login with the user argument
            return redirect('home')  # Redirect to a home or desired page
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    else:
        return render(request, 'cloud_drive_app/login.html')
# User logout function
def Logout(request):
    logout(request)
    return redirect("index")