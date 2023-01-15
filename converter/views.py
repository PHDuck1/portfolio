from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView, DeleteView, CreateView
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .forms import FileFieldForm
from .models import PDFFile
from .convert import make_pdf


class ConverterView(LoginRequiredMixin, FormView):
    form_class = FileFieldForm
    template_name = 'converter.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        files = request.FILES.getlist('file_field')
        # UserModel = get_user_model()
        user = request.user

        if form.is_valid():
            make_pdf(files=files, name=request.POST.get('name'), author=user)
            self.success_url = reverse_lazy('files_list')
            return self.form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)


class FilesList(LoginRequiredMixin, ListView):
    model = PDFFile
    context_object_name = 'files_list'
    template_name = 'files_list.html'

    def get_queryset(self):
        return PDFFile.objects.filter(author=self.request.user).order_by('-created_at')


class FileDelete(LoginRequiredMixin, DeleteView):
    model = PDFFile
    success_url = reverse_lazy('files_list')


class FileCreate(LoginRequiredMixin, CreateView):
    model = PDFFile
    fields = ['name', 'file_field']
