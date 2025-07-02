from django.contrib import admin
from .models import Location, Place, PlaceImage, Vote
from django.utils.html import format_html

class PlaceImageInline(admin.TabularInline):
    model = PlaceImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.image.url)
        return "(無圖片)"
    image_preview.short_description = "圖片預覽"

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'average_score_display', 'vote_count', 'total_votes')
    readonly_fields = ('total_votes', 'vote_count', 'average_score_display')
    ordering = ['location', 'name']
    inlines = [PlaceImageInline]

    def average_score_display(self, obj):
        if obj.vote_count == 0:
            return "尚無評分"
        avg = obj.total_votes / obj.vote_count
        return f"{avg:.1f}"
    average_score_display.short_description = "平均分數"

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'place', 'score', 'voted_at')
    list_filter = ('place', 'score', 'voted_at')
    search_fields = ('user__username', 'place__name')
    ordering = ('-voted_at',)
