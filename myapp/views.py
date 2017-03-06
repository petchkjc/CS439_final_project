from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from forms import PersonForm
from models import Person, Image

from django.shortcuts import render

def home(request):
	return render(request, 'home.html', {'key': "value" })

class CreatePersonView(CreateView):
	queryset = Person()
	template_name='person.html'
	form_class = PersonForm
	success_url = '/'
	def form_valid(self, form):
		#if not self.request.session.exists(self.request.session.session_key):
		self.request.session.create()
		# print type(self.request.session)
		form.instance.session=Session.objects.get(session_key=self.request.session.session_key)
		print form.instance.session
		return super(CreatePersonView, self).form_valid(form)

class UpdatePersonView(UpdateView):
	queryset = Person.objects.all()
	template_name='person.html'
	form_class = PersonForm
	success_url = '/'

class ListPersonView(ListView):
	model = Person
	template_name='person_list.html'

def Gallery(request):
	image_list = Image.objects.all().order_by('?')[:259]
	session_list = Session.objects.all()
	return render(request, 'my_gallery.html', {'image_list': image_list,'session_list': session_list })

def Sessions(request,imageid="1"):
	image_list = Image.objects.all().order_by('?')[:259]
	print type(request.session.session_key)
	print request.session.session_key

	if request.session.session_key:
		person_id=Person.objects.get(session__pk=request.session.session_key).id
	else:
		return redirect('person')

	request.session["person_id"]=person_id
	listdb = request.session.get("image_id",[])
	print listdb
	print type(listdb)

	if len(listdb)==1:
		request.session.set_expiry(10)
	listdb.append(imageid)

	request.session["image_id"] = listdb

	for i in Session.objects.all():
		print SessionStore().decode(i.session_data)

	return render(request, 'image.html', {'image_show': Image.objects.get(id=imageid),'listdb': listdb,'user_id': person_id, 'image_list': image_list })

def Clear(request):
	try:
		# del request.session["key"]
		request.session.flush()
	except KeyError:
		pass
	return redirect('person')