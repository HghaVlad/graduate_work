from .models import FilmWork
from .forms import FilmworkForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
 
def create_view(request):
    if request.method == 'POST':
        form = FilmworkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = FilmworkForm()
        context = {
            'form': form
        }
        return render(request, 'create.html', context)

def update_view(request, id):
    try:
        old_data = get_object_or_404(FilmWork, id=id)
    except Exception:
        raise Http404
    if request.method =='POST':
        form = FilmForm(request.POST, instance=old_data)
        if form.is_valid():
            form.save()
            return redirect(f'/{id}')
    else:
        form = FilmForm(instance = old_data)
        context ={
            'form':form
        }
        return render(request, 'update.html', context)

def delete_view(request, id):
    try:
        data = get_object_or_404(FilmWork, id=id)
    except Exception:
        raise Http404
 
    if request.method == 'POST':
        data.delete()
        return redirect('/')
    else:
        return render(request, 'delete.html')
