from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.views import View
from .models import KirrURL
from django.shortcuts import render,get_object_or_404
# Create your views here.
from .forms import SubmitUrlForm
from analytics.models import ClickEvent

class HomeView(View):
	def get(self,request,*args,**kwargs):
		form=SubmitUrlForm()
		context={
		   "title":"My site",
		   "form":form
		}

		return render(request,"shortener/home.html",context)
	def post(self,request,*args,**kwargs):
		form=SubmitUrlForm(request.POST)
		context={"title":"MY site",
		         "form":form

		}
		template = "shortener/home.html"
		if(form.is_valid()):
			new_url=form.cleaned_data.get('url')
			obj,created=KirrURL.objects.get_or_create(url=new_url)
			context={
			   "object":obj,
			   "created":created,
			}
			if created:
				template = "shortener/success.html"
			else:
				template = "shortener/already-exists.html"

		return render(request,template,context)

def kirr_ridirect_view(request,shortcode=None,*args,**kwargs):
	obj=get_object_or_404(KirrURL,shortcode=shortcode)
	return HttpResponseRedirect(obj.url)

class KirrCBView(View): #class based
	def get(self,request,shortcode=None,*args,**kwargs):
		qs = KirrURL.objects.filter(shortcode__iexact=shortcode)
		if(qs.count() != 1 and not qs.exists()):
			raise Http404
		obj = qs.first()
		print(ClickEvent.objects.create_event(obj))
		if("http" in obj.url):
			return HttpResponseRedirect(obj.url)
		else:
			obj.url="http://"+obj.url
			return HttpResponseRedirect(obj.url)
