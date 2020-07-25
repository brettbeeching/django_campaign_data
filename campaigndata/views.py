import datetime
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Max, Sum, Avg
from campaigndata.models import Donor, Organization, Donation
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required #decorator for view functions
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin #class mixin for class based views
from django.http import HttpResponseRedirect
from django.urls import reverse
#from catalog.forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.forms import inlineformset_factory

# Create your views here.

def index(request):
    '''View function for home page of site.'''

    # Generate counts of some of the main objects
    num_donations = Donation.objects.all().count()
    num_donors = Donor.objects.all().count()
    total_amount_donated = round(Donation.objects.all().aggregate(sum_donations=Sum('donation_amount'))['sum_donations'],2)
    donors_with_total_donations = Donor.objects.annotate(max_value=Sum('donation__donation_amount'))
    max_donor = donors_with_total_donations[0]
    #Guarantee the first donor's record total donation value is not None.
    max_donor.max_value = max_donor.max_value if (max_donor.max_value is not None) else 0.00
    for donor in donors_with_total_donations[1:]:
        try:
            if donor.max_value > max_donor.max_value:
                max_donor = donor
        except TypeError:
            #Error handling for case where donor has not donated yet.
            pass

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_donations': num_donations,
        'num_donors': num_donors,
        'total_amount_donated': total_amount_donated,
        'max_donor': max_donor,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class DonationListView(LoginRequiredMixin, generic.ListView):
    model = Donation
    paginate_by = 5


class DonorListView(generic.ListView):
    queryset = Donor.objects.annotate(total_donations=Sum('donation__donation_amount'))
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        #Donor.objects.annotate(total_donations=Sum('donation__donation_amount'))
        #context['total_donations'] = total_donations
        return context


class OrganizationListView(generic.ListView):
    queryset = Organization.objects.annotate(total_donations=Sum('donation__donation_amount'))
    paginate_by = 10


class DonationDetailView(generic.DetailView):
    model = Donation
    paginate_by = 10


class DonorDetailView(generic.DetailView):
    queryset = Donor.objects.annotate(total_donations=Sum('donation__donation_amount'))
    paginate_by = 10


class OrganizationDetailView(generic.DetailView):
    queryset = Organization.objects.annotate(total_donations=Sum('donation__donation_amount'))
    paginate_by = 10

class DonorCreate(PermissionRequiredMixin, CreateView):
    model = Donor
    fields = "__all__"
    #initial = {'date_of_death': '05/25/1998'}
    permission_required = ''


class DonationCreateDefault(CreateView):
    model = Donation
    fields = "__all__"

    def get_initial(self):
        '''Initializes default value for donor box on donation page if
        the link to the donation page is from a donor page.'''
        try:
            _donor = get_object_or_404(Donor, pk=self.kwargs['pk'])
            return {'donor': _donor,}
        except KeyError:
            return


class OrganizationCreate(PermissionRequiredMixin, CreateView):
    model = Organization
    fields = "__all__"
    permission_required = ''

    def get_success_url(self):
        '''Example of how to redirect on success'''
        return reverse('organization-detail', kwargs={'pk': self.object.pk})


class DonorUpdate(UpdateView):
    model = Donor
    fields = '__all__'
    template_name_suffix = '_update_form'


class OrganizationUpdate(UpdateView):
    model = Organization
    fields = '__all__'
    template_name_suffix = '_update_form'


class DonorDelete(DeleteView):
    model = Donor
    success_url = reverse_lazy('donors')


class OrganizationDelete(DeleteView):
    model = Organization
    success_url = reverse_lazy('organizations')
#AddressFormSet = inlineformset_factory(Donor, Address, field=('__all__'), formset=CustomInlineFormset)




# @permission_required('catalog.can_mark_returned')
# def renew_book_librarian(request, pk):
#     book_instance = get_object_or_404(BookInstance, pk=pk)

#     # If this is a POST request then process the Form data
#     if request.method == 'POST':

#         # Create a form instance and populate it with data from the request (binding):
#         form = RenewBookForm(request.POST)

#         # Check if the form is valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
#             book_instance.due_back = form.cleaned_data['renewal_date']
#             book_instance.save()

#             # redirect to a new URL:
#             return HttpResponseRedirect(reverse('borrowed-books'))

#     # If this is a GET (or any other method) create the default form.
#     else:
#         proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
#         form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

#     context = {
#     'form': form,
#     'book_instance': book_instance
#     }

#     return render(request, 'catalog/book_renew_librarian.html', context)


#


# class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
#     '''Generic class-based view listing books on loan to current user.'''
#     model = BookInstance
#     template_name = 'catalog/bookinstance_list_borrowed_user.html'
#     paginate_by = 10

#     def get_queryset(self):
#         return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


# class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):
#     model = BookInstance
#     template_name = 'catalog/bookinstance_list_borrowed_all.html'
#     paginate_by = 10
#     permission_required = 'catalog.can_mark_returned'


# class AuthorCreate(PermissionRequiredMixin, CreateView):
#     model = Author
#     fields = "__all__"
#     initial = {'date_of_death': '05/25/1998'}
#     permission_required = 'catalog.can_mark_returned'


# class AuthorUpdate(PermissionRequiredMixin, UpdateView):
#     model = Author
#     fields = ['first_name' , 'last_name', 'date_of_birth', 'date_of_death']
#     permission_required = 'catalog.can_mark_returned'


# class AuthorDelete(PermissionRequiredMixin, DeleteView):
#     model = Author
#     success_url = reverse_lazy('authors')
#     permission_required = 'catalog.can_mark_returned'


# class BookCreate(PermissionRequiredMixin, CreateView):
#     model = Book
#     fields = '__all__'
#     permission_required = 'catalog.can_mark_returned'


# class BookUpdate(PermissionRequiredMixin, UpdateView):
#     model = Book
#     fields = '__all__'
#     permission_required = 'catalog.can_mark_returned'


# class BookDelete(PermissionRequiredMixin, DeleteView):
#     model = Book
#     success_url = reverse_lazy('')
#     permission_required = 'catalog.can_mark_returned'
