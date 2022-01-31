from django.contrib import admin
from .models import Client, MonitoringPage, Tweet, Tweeter
from base.admin import BaseModelAdmin
from django import forms



@admin.register(Client)
class ClientAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'site')
    list_display_links = ('name',)
    list_per_page = 20
    
# admin.site.register(Client, ClientAdmin)
class MonitoringPageAdmin(BaseModelAdmin):
    list_display = ('client', 'type','text')
    search_fields = ("type", "text",)
    list_per_page = 20

admin.site.register(MonitoringPage, MonitoringPageAdmin)

@admin.register(Tweet)
class TweetAdmin(BaseModelAdmin):
    list_display = ('who', 'how', 'what', 'whom', 'when', 'estimation_label', 'action',\
        'monitor_time', 'where', 'replies', \
        'retweets', 'likes', 'bot')
    list_display_links = ('what',)
    readonly_fields = ('who', 'how', 'what', 'whom', 'when', 'where', 'replies',\
        'retweets', 'likes', 'bot', 'monitor_time', 'estimation_label', 'action')
    list_select_related = ('bot',)
    date_hierarchy = 'monitor_time'
    ordering = ['monitor_time']
    list_filter = ("how",)
    search_fields = ("what", "who",)

class TweeterAdminForm(forms.ModelForm):
    class Meta:
        model = Tweeter
        fields = "__all__"

    def clean_handle(self):
        if not self.cleaned_data["handle"].startswith("@"):
            raise forms.ValidationError("No startwith @")

        return self.cleaned_data["handle"]

@admin.register(Tweeter)
class TweeterAdmin(BaseModelAdmin):
    list_display = ('handle', 'client', 'total_tweets', 'support', 'offense',\
       'unbiased', 'score', 'show_average', 'category', 'add_time')
    readonly_fields = ('support', 'offense', 'total_tweets', 'unbiased', 'score',)
    ordering = ['score', 'category']
    list_per_page = 20
    search_fields = ("handle", "category",) 
    list_filter = ("category", )

    def show_average(self, obj):
        from django.utils.html import format_html
        # from django.db.models import Avg
        # result = Tweet.objects.filter(who=obj).aggregate(Avg("hates"))
        # return result["grade__avg"]
        return  format_html("<b><i>{}</i></b>", "grade__avg")

    show_average.short_description = "Average Grade"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["handle"].label = "Handle Name (only indicator):"
        return form

