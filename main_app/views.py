from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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


@login_required
def games_index(request):
    games = Game.objects.filter(user=request.user)
    return render(request, 'games/index.html', {'games': games})


def games_detail(request, game_id):
    game = Game.objects.get(id=game_id)
    adjs_not_used = Adj.objects.exclude(
        id__in=game.adjs.all().values_list('id'))

    played_form = PlayedForm()
    return render(request, 'games/detail.html', {
        'game': game,
        'played_form': played_form,
        'adjs': adjs_not_used
    })


class GameCreate(LoginRequiredMixin, CreateView):
    model = Game
    fields = '__all__'
    success_url = '/games/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class GameUpdate(UpdateView):
    model = Game
    # Let's make it impossible to rename a cat :)
    fields = ['description']


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
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, game_id=game_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', game_id=game_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
