from django.db import models

from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
import uuid

#Tutorial here: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models
# Create your models here.


class Donor(models.Model):
    '''Model representing a political campaign donor.'''
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=100)
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True)
    #address = models.ManyToManyField('Address', help_text='Input home address')
    #spouse = models.OneToOneField('Donor', primary_key=True, on_delete=models.SET_NULL, null=True, blank=True, related_name='spouse_of')

    class Meta:
        ordering = ['last_name', 'first_name']

    def age(self):
        return date.today().year - self.date_of_birth.year

    def get_absolute_url(self):
        """Returns the url to access a particular Author instance."""
        return reverse('donor-detail', args=[str(self.id)])

    def __str__(self):
            return f'{self.last_name}, {self.first_name}'

    # def display_address(self):
    #     """Create a string for the Address. This is required to display address in Admin."""
    #     primary = self.address.get(primary_address=True)
    #     if primary:
    #         return primary
    #     else:
    #         return self.address.all()[0]

    # display_address.short_description = 'Address'

class Organization(models.Model):
    '''Model representing an organization with multiple Donors'''
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
        constraints = [
        models.UniqueConstraint(fields=['name',], name='unique name')
    ]

    def get_absolute_url(self):
        """Returns the url to access a particular Organization instance."""
        return reverse('organization-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.name}'


class Marriage(models.Model):
    spouse1 = models.ForeignKey(Donor, on_delete=models.CASCADE, blank=False, related_name='spouse1')
    spouse2 = models.ForeignKey(Donor, on_delete=models.CASCADE, blank=False, related_name='spouse2')
    active_marriage = models.BooleanField(default=True, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['spouse1', 'spouse2'],
                name='unique_marriage')
        ]


class Address(models.Model):
    '''Model representing an address.'''

    address1 = models.CharField(
        "Address line 1",
        max_length=1024,
    )

    address2 = models.CharField(
        "Address line 2",
        max_length=1024,
        blank=True,
    )

    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=12,
    )

    city = models.CharField(
        "City",
        max_length=1024,
    )

    state = models.CharField(
        'State', 
        max_length=2,)

    country = models.CharField(
        "Country",
        max_length=3,
        blank=True
    )
    donor = models.ForeignKey('Donor', on_delete=models.SET_NULL, null=True, blank=True)
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=False)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f'''
        {self.address1}\n{self.address2}\n
        {self.city}, {self.state} {self.zip_code}\n
        {self.country}
        '''

class PhoneNumber(models.Model):
    PHONE_TYPE_CHOICES = [
    	('home', 'Home Phone'),
    	('home2', 'Home Phone 2'),
    	('mobile', 'Mobile Phone'),
    	('work', 'Work Phone'),
    ]

    area_code = models.IntegerField(help_text='Enter a 3 digit area code.', validators=[MinValueValidator(100), MaxValueValidator(999)])
    prefix = models.IntegerField(help_text='Enter a 3 phone prefix.', validators=[MinValueValidator(100), MaxValueValidator(999)])
    subscriber_code = models.IntegerField(help_text='Enter a 4 digit subscriber code.', validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    phone_type = models.CharField(max_length=20, choices=PHONE_TYPE_CHOICES, default=PHONE_TYPE_CHOICES[0])
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f'{self.area_code}-{self.prefix}-{self.subscriber_code}'


class Donation(models.Model):
    donor = models.ForeignKey(
        Donor, on_delete=models.SET_NULL, null=True, blank=True
        )

    organization = models.ForeignKey(
        Organization, on_delete=models.SET_NULL, null=True, blank=True
        )

    donation_amount = models.DecimalField(
        verbose_name= 'Donation amount $',
        max_digits=9,
        decimal_places=2
        )

    donation_date = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['donor']

    def get_absolute_url(self):
        """Returns the url to access a particular Author instance."""
        return reverse('donation-detail', args=[str(self.id)])

    def __str__(self):
        name = None
        if self.donor:
            name = self.donor
        elif self.organization:
            name = self.organization
        else:
            name = 'Anonymous'
        return f'Donor: {name}\nAmount: ${self.donation_amount}\nDate: {self.donation_date.strftime("%b/%d/%y")}'



# class Book(models.Model):
#     '''Model representing a book (but not a specific copy of a book).'''
#     title = models.CharField(max_length=200)

#     # Foreign Key used because book can only have one author, but authors can have multiple books
#     # Author as a string rather than object because it hasn't been declared yet in the file
#     author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

#     summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
#     isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

#     # ManyToManyField used because genre can contain many books. Books can cover many genres.
#     # Genre class has already been defined so we can specify the object above.
#     genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

#     language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

#     def __str__(self):
#         '''String rep of Model object.'''
#         return self.title

#     def get_absolute_url(self):
#         '''Returns the url to access a detail record for this book.'''
#         return reverse('book-detail', args=[str(self.id)])

#     def display_genre(self):
#         """Create a string for the Genre. This is required to display genre in Admin."""
#         return ', '.join(genre.name for genre in self.genre.all()[:3])

#     display_genre.short_description = 'Genre'


# class BookInstance(models.Model):
#     '''Model representing a specific copy of a book (i.e. that can be borrowed from the libary).'''
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across the whole library')
#     book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
#     imprint = models.CharField(max_length=200)
#     due_back = models.DateField(null=True, blank=True)
#     borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

#     LOAN_STATUS = (
#         ('m', 'Maintenance'),
#         ('o', 'On loan'),
#         ('a', 'Available'),
#         ('r', 'Reserved'),
#     )

#     status = models.CharField(
#         max_length=1,
#         choices=LOAN_STATUS,
#         blank=True,
#         default='m',
#         help_text='Book availability',
#     )

#     class Meta:
#         ordering = ['due_back']
#         permissions = (('can_mark_returned', 'Set book as returned'),)

#     def __str__(self):
#         return f'{self.id} ({self.book.title})'

#     '''Admin site view configurations.'''
#     def display_due_date(self):
#         return self.due_back

#     def is_overdue(self):
#         if self.due_back and date.today() > self.due_back:
#             return True
#         return False


#     def display_status(self):
#         for row in self.LOAN_STATUS:
#             if row[0] == self.status:
#                 return row[1]

#     '''Admin site view headers.'''
#     display_due_date.short_description = 'Due Date'

#     display_status.short_description = 'Status'



# class Author(models.Model):
#     '''Model representing an author'''
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     date_of_birth = models.DateField(null=True, blank=True)
#     date_of_death = models.DateField('died', null=True, blank=True)

#     class Meta:
#         ordering = ['last_name', 'first_name']

#     def get_absolute_url(self):
#         """Returns the url to access a particular Author instance."""
#         return reverse('author-detail', args=[str(self.id)])

#     def __str__(self):
#         return f'{self.last_name}, {self.first_name}'