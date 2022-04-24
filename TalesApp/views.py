from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView,ListView
from .models import *
from .forms import *
from django.core.files.storage import FileSystemStorage
from django.db.models import Q

def main(request):
    return render(request,'Main.html',{'user':request.user,'genres':Genre.objects.all(),
                                       'title':'DjangoTales'})

class TaleView(DetailView):
    model = Tale
    context_name_object = 'tale'
    template_name = 'Tale.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['comms'] = self.object.comments.all()
        context['genres'] = Genre.objects.all()
        return context

class TaleList(ListView):
    model = Tale
    template_name = 'TaleList.html'
    paginate_by = 10
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        if 'title' in self.kwargs.keys():
            data = Genre.objects.get(title=self.kwargs['title']).tales.all()
        try:
            self.kwargs['pg']
        except:
            self.kwargs['pg'] = 1
        context['tales'] = Paginator(data,self.paginate_by).page(self.kwargs['pg'])
        context['genres'] = Genre.objects.all()
        return context

@login_required
def LoadTale(request):
    if request.method == 'POST':
        form = TaleForm()
        if form.is_valid():
            form.save()
            for n,i in enumerate(request.FILES.values()):
                fs = FileSystemStorage() #defaults to   MEDIA_ROOT  
                filename = fs.save(i.name, i)
                file_url = fs.url(filename)
                new = new.replace(f'input type="file" name="fle{n+1}"',f'img src="media/{i.name}" width=300 height=500')
            return redirect('tale',pk=new.pk)
    return render(request,'TaleForm.html',{'user':request.user,'genres':Genre.objects.all()})

@login_required
def comment(request,pk):
    if request.method == 'POST':
        new = Comment(user=request.user,tale=Tale.objects.get(pk=pk),
                content=request.POST['content'])
        new.save()
    return redirect('tale',pk=pk)

@login_required
def reply(request,pk):
    c = Comment.objects.get(pk=pk)
    if request.method == 'POST':
        new = Comment(user=request.user,tale=c.tale,parent=c,
                content=request.POST['content'])
        new.save()
    return redirect('tale',pk=pk)

@login_required
def mark(request,pk):
    if request.method == 'POST':
        new = Mark(user=request.user,tale=Tale.objects.get(pk=pk))
        new.save()
        tale = Tale.objects.get(pk=pk)
        tale.mark = tale.marks.aggregate(Avg('meaning'))
        tale.save()
    return redirect('tale',pk=pk)

def search(request):
    if request.method == 'POST':
        return redirect('search_res',query=request.POST['query'])

def search_result(request,query,pg=None):
    if not pg:
        pg = 1
    data = Tale.objects.filter(
            Q(title__icontains=query) | Q(title__icontains=query.capitalize())
            )
    return render(request,'Search.html',{'user':request.user,'genres':Genre.objects.all()})
