import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView, DeleteView, CreateView
from django.views.generic import ListView
from django.urls import reverse_lazy

from .forms import FileFieldForm
from .models import PDFFile
from .convert import PDFManager


class ConverterView(LoginRequiredMixin, FormView):
    form_class = FileFieldForm
    template_name = 'converter.html'
    success_url = reverse_lazy('files_list')

    def post(self, request):

        form = self.get_form(self.form_class)
        if not form.is_valid():
            print(form.errors)
            return self.form_invalid(form)

        image_previews = request.POST.get('image_previews')
        image_order = json.loads(image_previews)

        # Get the data from the request
        image_files = request.FILES.getlist('file_field')
        name = request.POST.get('name')
        author = request.user

        sorted_list = [0]*len(image_files)
        for image in image_files:
            sorted_list[image_order[image._name]] = image

        # Create pdf_file and save to DB using manager
        manager = PDFManager(name, author)
        pdf_buffer = manager.convert(sorted_list)
        manager.save_file(pdf_buffer)

        return self.form_valid(form)


class FilesList(LoginRequiredMixin, ListView):
    model = PDFFile
    context_object_name = 'files_list'
    template_name = 'file_storage/files_list.html'

    def get_queryset(self):
        return PDFFile.objects.filter(author=self.request.user).order_by('-created_at')


class FileDelete(LoginRequiredMixin, DeleteView):
    model = PDFFile
    success_url = reverse_lazy('files_list')


class PDFFileCreateView(LoginRequiredMixin, CreateView):
    model = PDFFile
    fields = ['name', 'file_field']
    success_url = reverse_lazy('files_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


