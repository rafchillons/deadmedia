from django import forms
from .models import Video, BotTask
from django.contrib.auth.forms import AuthenticationForm
from deadmedia import settings


class VideoDeleteForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = (
            'storage_name',
        )

    def clean_storage_name(self):
        try:
            data = self.cleaned_data['storage_name']

            video_id = str(data).rsplit('/', 1)[1].rsplit('.', 1)[0]

            if not Video.objects.get(id=video_id):
                raise forms.ValidationError('Can not find video!')

            return video_id
        except Exception as e:
            raise forms.ValidationError('Wrong url({})!'.format(e))


class BotTaskForm(forms.Form):

    interval = forms.IntegerField()
    with_words = forms.CharField(required=False)
    without_words = forms.CharField(required=False)

    is_max_time = forms.BooleanField(required=False)
    working_time = forms.IntegerField(required=False)
    is_max_iter = forms.BooleanField(required=False)
    iters_to_do = forms.IntegerField(required=False)

    is_music = forms.BooleanField(required=False)
    is_adult = forms.BooleanField(required=False)
    is_webm = forms.BooleanField(required=False)
    is_hot = forms.BooleanField(required=False)
    is_mp4 = forms.BooleanField(required=False)

    video_formats = forms.CharField(required=True)

    max_videos_count = forms.IntegerField(required=False)

    def clean_interval(self):
        data = self.cleaned_data['interval']

        if type(data) is not int:
            raise forms.ValidationError('Interval mast be number!')

        if data < 0:
            raise forms.ValidationError('Interval can not be negative!')

        return data

    def clean_with_words(self):
        data = self.cleaned_data['with_words']
        return data.split()

    def clean_without_words(self):
        data = self.cleaned_data['without_words']
        return data.split()

    def clean_is_max_time(self):
        if self.cleaned_data['is_max_time']:
            return True
        return False

    def clean_working_time(self):
        data = self.cleaned_data['working_time']

        if type(data) is not int:
            if self.cleaned_data['is_max_time']:
                raise forms.ValidationError('Working time mast be number!')
            else:
                data = 1

        if not data > 0:
            raise forms.ValidationError('Working time mast be more then 0!')

        return data

    def clean_is_max_iter(self):
        if self.cleaned_data['is_max_iter']:
            return True
        return False

    def clean_iters_to_do(self):
        data = self.cleaned_data['iters_to_do']

        if type(data) is not int:
            if self.cleaned_data['is_max_iter']:
                raise forms.ValidationError('Max iters mast be number!')
            else:
                data = 1

        if not data > 0:
            raise forms.ValidationError('Max iters mast be more then 0!')

        return data

    def clean_is_music(self):
        if self.cleaned_data['is_music']:
            return True
        return False

    def clean_is_adult(self):
        if self.cleaned_data['is_adult']:
            return True
        return False

    def clean_is_webm(self):
        if self.cleaned_data['is_webm']:
            return True
        return False

    def clean_is_hot(self):
        if self.cleaned_data['is_hot']:
            return True
        return False

    def clean_is_mp4(self):
        if self.cleaned_data['is_mp4']:
            return True
        return False

    def clean_max_videos_count(self):
        data = self.cleaned_data['max_videos_count']

        if type(data) is not int:
            if data:
                raise forms.ValidationError('Max videos per iter mast be number!')
            else:
                data = False

        else:
            if not data > 0:
                raise forms.ValidationError('Max videos per iter mast be more then 0!')

        return data

    def clean_video_formats(self):
        wrong_formats = []
        data = []
        allowed_formats = {x[1]:x[0] for x in Video.VIDEO_FORMATS}

        for elem in self.cleaned_data['video_formats'].split():
            if elem in allowed_formats:
                if allowed_formats[elem] in data:
                    raise forms.ValidationError("Stop writing formats twice, you stupid fuck!")
                data.append(allowed_formats[elem])
            else:
                wrong_formats.append(elem)

        if wrong_formats:
            str_errors = " '{}'"*(wrong_formats.__len__())
            str_errors = str_errors.format(*wrong_formats)
            str_formats = " '{}'"*(Video.VIDEO_FORMATS.__len__())
            str_formats = str_formats.format(*allowed_formats)
            raise forms.ValidationError('Wrong formats:{}! These are allowed:{}.'.format(str_errors, str_formats))

        print(data)
        return data


class BotTaskRemoveForm(forms.Form):
    ignore_time = forms.IntegerField()
    interval = forms.IntegerField()
    with_words = forms.CharField(required=False)
    without_words = forms.CharField(required=False)

    is_max_time = forms.BooleanField(required=False)
    working_time = forms.IntegerField(required=False)
    is_max_iter = forms.BooleanField(required=False)
    iters_to_do = forms.IntegerField(required=False)

    is_music = forms.BooleanField(required=False)
    is_adult = forms.BooleanField(required=False)
    is_webm = forms.BooleanField(required=False)
    is_hot = forms.BooleanField(required=False)
    is_mp4 = forms.BooleanField(required=False)

    max_videos_count = forms.IntegerField(required=False)

    def clean_ignore_time(self):
        data = self.cleaned_data['ignore_time']

        if type(data) is not int:
            raise forms.ValidationError('Ignore time mast be number!')

        if data <= 0:
            raise forms.ValidationError('Ignore time can not be negative!')

        return data

    def clean_interval(self):
        data = self.cleaned_data['interval']

        if type(data) is not int:
            raise forms.ValidationError('Interval mast be number!')

        if data < 0:
            raise forms.ValidationError('Interval can not be negative!')

        return data

    def clean_is_max_time(self):
        if self.cleaned_data['is_max_time']:
            return True
        return False

    def clean_working_time(self):
        data = self.cleaned_data['working_time']

        if type(data) is not int:
            if self.cleaned_data['is_max_time']:
                raise forms.ValidationError('Working time mast be number!')
            else:
                data = 1

        if not data > 0:
            raise forms.ValidationError('Working time mast be more then 0!')

        return data

    def clean_is_max_iter(self):
        if self.cleaned_data['is_max_iter']:
            return True
        return False

    def clean_iters_to_do(self):
        data = self.cleaned_data['iters_to_do']

        if type(data) is not int:
            if self.cleaned_data['is_max_iter']:
                raise forms.ValidationError('Max iters mast be number!')
            else:
                data = 1

        if not data > 0:
            raise forms.ValidationError('Max iters mast be more then 0!')

        return data

    def clean_is_music(self):
        if self.cleaned_data['is_music']:
            return True
        return False

    def clean_is_adult(self):
        if self.cleaned_data['is_adult']:
            return True
        return False

    def clean_is_webm(self):
        if self.cleaned_data['is_webm']:
            return True
        return False

    def clean_is_hot(self):
        if self.cleaned_data['is_hot']:
            return True
        return False

    def clean_is_mp4(self):
        if self.cleaned_data['is_mp4']:
            return True
        return False

    def clean_max_videos_count(self):
        data = self.cleaned_data['max_videos_count']

        if type(data) is not int:
            if data:
                raise forms.ValidationError('Max videos per iter mast be number!')
            else:
                data = False

        else:
            if not data > 0:
                raise forms.ValidationError('Max videos per iter mast be more then 0!')

        return data




"""
    def clean_downloaded_url(self):
        data = self.cleaned_data['downloaded_url']

        if get_status_code(data) != 200:
            raise forms.ValidationError('Wrong url!')

        return data
"""

"""
def get_status_code(host, path="/"):
     This function retreives the status code of a website by requesting
        HEAD data from the host. This means that it only requests the headers.
        If the host cannot be reached or something else goes wrong, it returns
        None instead.
    
    try:
        conn = httplib.HTTPConnection(host)
        conn.request("HEAD", path)
        return conn.getresponse().status
    except StandardError:
        return None
"""