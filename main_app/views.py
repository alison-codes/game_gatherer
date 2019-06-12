from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Game, Played
from .forms import PlayedForm

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def games_index(request):
  games = Game.objects.all()
  return render(request, 'games/index.html', { 'games': games })
    
def games_detail(request, game_id):
  game = Game.objects.get(id=game_id)
  played_form = PlayedForm()
  return render(request, 'games/detail.html', {
     'game': game ,
     'played_form': played_form
     })

class GameCreate(CreateView):
  model = Game
  fields = '__all__'
  success_url = '/games/'

class GameUpdate(UpdateView):
  model = Game
  # Let's make it impossible to rename a cat :)
  fields = [ 'description']

class GameDelete(DeleteView):
  model = Game
  success_url = '/games/'


def add_played(request, game_id):
  form = PlayedForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    new_played = form.save(commit=False)
    new_played.game_id = game_id
    new_played.save()
  return redirect('detail', game_id=game_id)
