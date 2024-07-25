from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, get_user_model, login 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from .forms import UserRegistirationForm, InventoryItemForm
from .models import InventoryItem, Category, Profile, Warehouse
from inventory_management.settings import LOW_QUANTITY
from django.contrib import messages


def register(request):
	if request.method == 'POST':
		user_form = UserRegistirationForm(request.POST)
		if user_form.is_valid:
			new_user = user_form.save(commit=False)
			new_user.set_password(
				user_form.cleaned_data['password']
			)
			new_user.username = new_user.first_name  + ' ' + new_user.last_name
			new_user.save()
			Profile.objects.create(user=new_user)
			#create_action(new_user, 'has created an account')
			return render(
				request,
				'registration/registration_done.html',
				{'new_user': new_user},

			)
	else:
		user_form = UserRegistirationForm()
	return render(
		request,
		'registration/register.html',
		{'user_form': user_form}
	)


class Home(TemplateView):
	template_name = 'inventory/home.html'


class Dashboard(LoginRequiredMixin, View):
	def get(self, request):
		items = InventoryItem.objects.order_by('id')

		low_inventory = InventoryItem.objects.filter(
			user=self.request.user.id,
			quantity__lte=LOW_QUANTITY
		)

		if low_inventory.count() > 0:
			if low_inventory.count() > 1:
				messages.error(request, f'{low_inventory.count()} items have low inventory')
			else:
				messages.error(request, f'{low_inventory.count()} item has low inventory')

		low_inventory_ids = InventoryItem.objects.filter(
			user=self.request.user.id,
			quantity__lte=LOW_QUANTITY
		).values_list('id', flat=True)

		return render(request, 'inventory/dashboard.html', {'items': items, 'low_inventory_ids': low_inventory_ids})
	

class AddItem(LoginRequiredMixin, CreateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('dashboard')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		context['warehouses'] = Warehouse.objects.all()
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)


class EditItem(LoginRequiredMixin, UpdateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('dashboard')


class DeleteItem(LoginRequiredMixin, DeleteView):
	model = InventoryItem
	template_name = 'inventory/delete_item.html'
	success_url = reverse_lazy('dashboard')
	context_object_name = 'item'



