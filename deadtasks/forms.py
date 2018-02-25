from django import forms
from django.contrib.auth.forms import AuthenticationForm
from deadmedia import settings

from django.shortcuts import render, redirect, get_object_or_404
from deadtasks.models import DownloadDvachTask, RemoveOldTask

"""
class BotTaskForm(forms.Form):

    with_words = forms.CharField(required=False)
    without_words = forms.CharField(required=False)

    format_webm = forms.BooleanField(required=False)
    format_mp4 = forms.BooleanField(required=False)

    video_category = forms.ChoiceField(choices=DvachDownloadTask.VIDEO_CATEGORIES)

    def clean_video_category(self):
        data = self.cleaned_data['video_category']

        if int(data) not in [item[0] for item in DvachDownloadTask.VIDEO_CATEGORIES]:
            raise forms.ValidationError('Wrong category!')

        return data

    def clean_with_words(self):
        return self.cleaned_data['with_words'].split()

    def clean_without_words(self):
        return self.cleaned_data['without_words'].split()

    def clean(self):

        if not (self.cleaned_data['format_webm'] or self.cleaned_data['format_mp4']):
            raise forms.ValidationError('Video formats not set!')
"""


class DvachDownloadTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DvachDownloadTaskForm, self).__init__(*args, **kwargs)

        self.fields["required_words"].required = False
        self.fields["banned_words"].required = False
        self.fields["video_category"].choices = DownloadDvachTask.VIDEO_CATEGORIES

    class Meta:
        model = DownloadDvachTask
        fields = [
            "required_words",
            "banned_words",
            "download_format_webm",
            "download_format_mp4",
            "video_category",
        ]

    def clean_video_category(self):
        data = self.cleaned_data['video_category']

        if int(data) not in [item[0] for item in DownloadDvachTask.VIDEO_CATEGORIES]:
            raise forms.ValidationError('Wrong category!')

        return int(data)

    def clean_required_words(self):
        return self.cleaned_data['required_words'].encode()

    def clean_banned_words(self):
        return self.cleaned_data['banned_words'].encode()

    def clean(self):
        if not (self.cleaned_data['download_format_webm'] or self.cleaned_data['download_format_mp4']):
            raise forms.ValidationError('Video formats not set!')

        return self.cleaned_data


class OldRemoveTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OldRemoveTaskForm, self).__init__(*args, **kwargs)

        self.fields["video_category"].choices = DownloadDvachTask.VIDEO_CATEGORIES

    class Meta:
        model = RemoveOldTask
        fields = [
            "remove_format_webm",
            "remove_format_mp4",
            "video_category",
            "video_age",
        ]

    def clean_video_category(self):
        data = int(self.cleaned_data['video_category'])

        if data not in [item[0] for item in DownloadDvachTask.VIDEO_CATEGORIES]:
            raise forms.ValidationError('Wrong category!')

        return data

    def clean_video_age(self):
        data = int(self.cleaned_data['video_age'])

        if not 0 < data < 10000000:
            raise forms.ValidationError('Wrong age(0<age<10000000)!')

        return data

    def clean(self):
        if not (self.cleaned_data['remove_format_webm'] or self.cleaned_data['remove_format_mp4']):
            raise forms.ValidationError('Video formats not set!')

        return self.cleaned_data
