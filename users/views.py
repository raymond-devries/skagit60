from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.edit import UpdateView
from users.forms import *


class Profile(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'users/profile.html', {'user': request.user})


class EditProfile(View):
    form_class = ProfileForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.request.user)
        return render(request, 'users/edit_profile.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated.')
            return redirect('profile')

        else:
            return render(request, 'users/edit_profile.html', {'form': form})




