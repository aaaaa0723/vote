from collections import defaultdict
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Place, Vote


@login_required
def index(request):
    # 首頁：純顯示一些簡單內容，不帶投票功能
    return render(request, 'voteapp/index.html')

@login_required
def voting(request):
    # 投票頁面
    places = Place.objects.select_related('location').prefetch_related('images')
    location_groups = defaultdict(list)
    for place in places:
        location_groups[place.location].append(place)
    location_groups = sorted(location_groups.items(), key=lambda x: x[0].name)
    return render(request, 'voteapp/voting.html', {'location_groups': location_groups})

@login_required
def vote_all(request):
    if request.method == 'POST':
        user = request.user
        for place in Place.objects.all():
            key = f'score_{place.id}'
            if key in request.POST:
                if Vote.objects.filter(user=user, place=place).exists():
                    continue  # 已投過票就跳過

                try:
                    score = int(request.POST[key])
                except ValueError:
                    continue

                Vote.objects.create(user=user, place=place, score=score)
                place.total_votes += score
                place.vote_count += 1
                place.save()
        return redirect('voteapp:result')
    return redirect('voteapp:index')

@login_required
def result(request):
    places = Place.objects.select_related('location').order_by('-total_votes')
    return render(request, 'voteapp/result.html', {'places': places})
