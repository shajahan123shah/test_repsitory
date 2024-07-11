from django.shortcuts import render, redirect, get_object_or_404
from .models import MovieInfo, CensorInfo, Director, Actor
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
# from .models import Profile
from django.contrib import messages

def movie_list(request):
    movies = MovieInfo.objects.all().order_by('-id').select_related('censor_info', 'director').prefetch_related('actors')
    return render(request, 'movie_list.html', {'movies': movies})

def create_movie(request):
    if request.method == 'POST':
        try:
            title = request.POST['title']
            year = request.POST['year']
            description = request.POST['description']
            image = request.FILES.get('image')
            censor_info_id = request.POST['censor_info']
            director_id = request.POST['director']
            actor_ids = request.POST.getlist('actors')
            
            censor_info = CensorInfo.objects.get(id=censor_info_id)
            director = Director.objects.get(id=director_id)
            
            new_movie = MovieInfo(
                title=title, 
                year=year, 
                description=description, 
                image=image, 
                censor_info=censor_info,
                director=director
            )
            new_movie.save()
            
            actors = Actor.objects.filter(id__in=actor_ids)
            new_movie.actors.add(*actors)
            
            return redirect('movie_list')
        
        except (KeyError, ValueError, CensorInfo.DoesNotExist, Director.DoesNotExist, Actor.DoesNotExist) as e:
            # Handle errors (e.g., invalid form data, missing objects)
            # You can render the form again with an error message or redirect to an error page
            return render(request, 'create_movie.html', {'error': str(e)})
    
    censor_infos = CensorInfo.objects.all()
    directors = Director.objects.all()
    actors = Actor.objects.all()
    return render(request, 'create_movie.html', {
        'censor_infos': censor_infos,
        'directors': directors,
        'actors': actors
    })


def edit_movie(request, id):
    movie = get_object_or_404(MovieInfo, id=id)
    if request.method == 'POST':
        movie.title = request.POST['title']
        movie.year = request.POST['year']
        movie.description = request.POST['description']
        if 'image' in request.FILES:
            movie.image = request.FILES['image']
        
        censor_info_id = request.POST['censor_info']
        director_id = request.POST['director']
        actor_ids = request.POST.getlist('actors')
        
        movie.censor_info = CensorInfo.objects.get(id=censor_info_id)
        movie.director = Director.objects.get(id=director_id)
        movie.actors.set(actor_ids)
        
        movie.save()
        return redirect('movie_list')
    
    censor_infos = CensorInfo.objects.all()
    directors = Director.objects.all()
    actors = Actor.objects.all()
    return render(request, 'edit_movie.html', {
        'movie': movie,
        'censor_infos': censor_infos,
        'directors': directors,
        'actors': actors
    })

def delete_movie(request, id):
    movie = get_object_or_404(MovieInfo, id=id)
    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')
    return render(request, 'confirm_delete.html', {'movie': movie})



# signals.py


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

# views.py


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        
        if password == password_confirm:
            try:
                user = User.objects.create_user(username=username, password=password)
                messages.success(request, 'Your account has been created successfully!')
                return redirect('login')
            except Exception as e:
                messages.error(request, str(e))
        else:
            messages.error(request, 'Passwords do not match')
    
    return render(request, 'signup.html')
