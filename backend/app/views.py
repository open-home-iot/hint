from django.views.generic.base import TemplateView


class AppView(TemplateView):

    template_name = "index.html"

#    def get_context_data(self, **kwargs):
#        contex = super().get_context_data(**kwargs)
#        Do shit with context
#        return context
