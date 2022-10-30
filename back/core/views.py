from django.shortcuts import render, HttpResponse
from django.views.generic.base import TemplateView


class Body(TemplateView):
    template_name = 'core/body.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class Face(TemplateView):
    template_name = 'core/face.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
