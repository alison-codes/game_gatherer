from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Game, Played, Adj, Photo
from .forms import PlayedForm
import uuid
import boto3


S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'catcoll2'

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def games_index(request):
  games = Game.objects.all()
  return render(request, 'games/index.html', { 'games': games })
    
def games_detail(request, game_id):
  game = Game.objects.get(id=game_id)
  adjs_not_used = Adj.objects.exclude(id__in = game.adjs.all().values_list('id'))

  played_form = PlayedForm()
  return render(request, 'games/detail.html', {
     'game': game ,
     'played_form': played_form,
     'adjs': adjs_not_used 
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

def assoc_adj(request, game_id, adj_id):
  Game.objects.get(id=game_id).adjs.add(adj_id)
  return redirect('detail', game_id=game_id)


def unassoc_adj(request, game_id, adj_id):
  Game.objects.get(id=game_id).adjs.remove(adj_id)
  return redirect('detail', game_id=game_id)

def add_photo(request, game_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, game_id=game_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', game_id=game_id)