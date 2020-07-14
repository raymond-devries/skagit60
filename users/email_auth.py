from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()

        email_user = user_model.objects.filter(email=username).first()
        username_user = user_model.objects.filter(username=username).first()

        if email_user is not None:
            user = email_user
        elif username_user is not None:
            user = username_user
        else:
            return None

        if user.check_password(password):
            return user

        return None
