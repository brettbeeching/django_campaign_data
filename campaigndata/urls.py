from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('donations/', views.DonationListView.as_view(), name='donations'),
    path('donation/<int:pk>', views.DonationDetailView.as_view(), name='donation-detail'),
    path('donors/', views.DonorListView.as_view(), name='donors'),
    path('donor/<int:pk>', views.DonorDetailView.as_view(), name='donor-detail'),
    path('organizations/', views.OrganizationListView.as_view(), name='organizations'),
    path('organization/<int:pk>', views.OrganizationDetailView.as_view(), name='organization-detail'),
    path('donor/create/', views.DonorCreate.as_view(), name='donor-create'),
    path('donation/create/', views.DonationCreateDefault.as_view(), name='donation-create'),
    path('donation/create/<int:pk>', views.DonationCreateDefault.as_view(), name='donation-create-default'),
    path('organization/create/', views.OrganizationCreate.as_view(), name='organization-create'),
    path('donor/update/<int:pk>', views.DonorUpdate.as_view(), name='donor-update'),
    path('organization/update/<int:pk>', views.OrganizationUpdate.as_view(), name='organization-update'),
    path('donor/delete/<int:pk>', views.DonorDelete.as_view(), name='donor-delete'),
    path('organization/delete/<int:pk>', views.OrganizationDelete.as_view(), name='organization-delete'),
]

'''
urlpatterns += [
	path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]

urlpatterns += [

	path('borrowedbooks/', views.LoanedBooksListView.as_view(), name='borrowed-books'),
]

urlpatterns += [
	path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [
	path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
	path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
	path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name = 'author-delete')
]

urlpatterns += [
	path('book/create/', views.BookCreate.as_view(), name='book-create'),
	path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
	path('book/<int:pk>/delete/', views.BookDelete.as_view(), name = 'book-delete')
]
'''