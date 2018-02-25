# -*- coding: utf-8 -*-
from django import forms

from deadtasks.models import DownloadDvachTask, RemoveOldTask


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
        data = self.cleaned_data["video_category"]

        if int(data) not in [item[0] for item in DownloadDvachTask.VIDEO_CATEGORIES]:
            raise forms.ValidationError("Wrong category!")

        return int(data)

    def clean_required_words(self):
        return self.cleaned_data["required_words"].encode("utf8")

    def clean_banned_words(self):
        return self.cleaned_data["banned_words"].encode("utf8")

    def clean(self):
        if not (self.cleaned_data["download_format_webm"] or self.cleaned_data["download_format_mp4"]):
            raise forms.ValidationError("Video formats not set!")

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
        data = int(self.cleaned_data["video_category"])

        if data not in [item[0] for item in DownloadDvachTask.VIDEO_CATEGORIES]:
            raise forms.ValidationError("Wrong category!")

        return data

    def clean_video_age(self):
        data = int(self.cleaned_data["video_age"])

        if not 0 < data < 10000000:
            raise forms.ValidationError("Wrong age(0<age<10000000)!")

        return data

    def clean(self):
        if not (self.cleaned_data["remove_format_webm"] or self.cleaned_data["remove_format_mp4"]):
            raise forms.ValidationError("Video formats not set!")

        return self.cleaned_data
