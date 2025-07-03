from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="地區名稱")

    def __str__(self):
        return self.name

class Place(models.Model):
    name = models.CharField(max_length=100, verbose_name="景點名稱")
    description = models.TextField(verbose_name="介紹")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name="所屬地區", related_name='places', null=True, blank=True)
    image = models.CharField(max_length=255, blank=True, null=True, verbose_name="圖片路徑")  # 存 static/images/xxx.jpg 路徑字串
    total_votes = models.IntegerField(default=0, verbose_name="總投票分數")
    vote_count = models.IntegerField(default=0, verbose_name="投票人數")

    def average_score(self):
        if self.vote_count == 0:
            return "尚無評分"
        return round(self.total_votes / self.vote_count, 1)

    def __str__(self):
        return f"{self.name}（{self.location}）"

class PlaceImage(models.Model):
    place = models.ForeignKey(Place, related_name="images", on_delete=models.CASCADE)
    image = models.CharField(max_length=255, verbose_name="圖片路徑")  # 存 static/images/xxx.jpg 路徑字串

    def __str__(self):
        return f"{self.place.name} 的圖片 {self.id}"

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    score = models.IntegerField()
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'place')

    def __str__(self):
        return f"{self.user.username} → {self.place.name}：{self.score}分"
