from django import forms
from .models import Video
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import ReCaptchaField
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


class AuthenticationCaptchaForm(forms.Form):
    captcha = ReCaptchaField(
        public_key=settings.RECAPTCHA_PUBLIC_KEY,
        private_key=settings.RECAPTCHA_PRIVATE_KEY,
    )




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