from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid

class BaseModel(models.Model):
    status_choices = {
        ("1", "Active"),
        ("2", "Inactive"),
        ("3", "Deleted"),
    }
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices = status_choices, default="2")

    class Meta:
        abstract = True


class Author(BaseModel):
    readonly_fields = ('a_id')
    a_id = models.UUIDField(primary_key = True, default = uuid.uuid4(), editable = False)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    meta_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return str(self.a_id)

    def as_dict(self):
        return {
            'a_id':self.a_id,
            'name':self.name,
            'description':self.description,
            'meta_data':self.meta_data,
        }


class Language(BaseModel):
    readonly_fields = ('lang_id')
    lang_id = models.UUIDField(primary_key = True, default = uuid.uuid4(), editable = False)
    name = models.CharField(max_length=200)
    script = models.TextField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.lang_id)

    def as_dict(self):
        return {
            'lang_id':self.lang_id,
            'name':self.name,
            'script':self.script,
            'about':self.about,
        }

class Publisher(BaseModel):
    pub_id = models.UUIDField(primary_key = True, default = uuid.uuid4(), editable = False)
    name = models.CharField(max_length=100)
    meta_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            'pub_id':self.pub_id,
            'name':self.name,
            'meta_data':self.meta_data,
        }
        
class Book(BaseModel):
    BOOL_CHOICES = ((True, 'Yes, there exist an EBook'), (False, 'No, not an Ebook'))

    book_id = models.UUIDField(primary_key = True, default = uuid.uuid4(), editable = False)
    name = models.CharField(max_length=200)
    languages = models.ManyToManyField(Language,null=True, blank=True)
    authors = models.ManyToManyField(Author,null=True, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    extra_details = models.JSONField(null=True, blank=True)
    is_ebook = models.BooleanField(choices=BOOL_CHOICES,null=True, blank=True)

    def __str__(self):
        return str(self.book_id)
    
    def as_dict(self):
        return {
            'book_id':self.book_id,
            'name':self.name,
            'languages':[language.as_dict() for language in self.languages.all()],
            'authors':[author.as_dict() for author in self.authors.all()],
            'publisher':self.publisher.name,
            'extra_details':self.extra_details,
            'is_ebook':self.is_ebook,
        }


class User(BaseModel):
    type_choices = {
        ("1", "Super Admin"),
        ("2", "Librarian"),
        ("3", "User"),
    }

    user_id = models.UUIDField(primary_key = True, default = uuid.uuid4(), editable = False),
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    mobile = PhoneNumberField()
    email = models.EmailField(max_length = 254, unique=True)
    meta_data = models.JSONField(null=True, blank=True)
    role = models.CharField(max_length=1, choices = type_choices, default="3")
    subscription = models.BooleanField(default=False)
    favorites = models.ManyToManyField(Book, null=True, blank=True)
    
    def __str__(self):
        return self.first_name

    def as_dict(self):
        return {
            'user_id':self.user_id,
            'first_name':self.first_name,
            'middle_name':self.middle_name,
            'last_name':self.last_name,
            'mobile': str(self.mobile),
            'email':self.email,
            'meta_data':self.meta_data,
            'role':self.role,
            'subscription':self.subscription,
            'favorites':[book.as_dict() for book in self.favorites.all()],
        }

    
class Ebook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="ebook")
    ebook_id = models.UUIDField(primary_key = True, default = uuid.uuid4(), editable = False)
    book_location = models.CharField(max_length=200, null=True, blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.ebook_id)

    def as_dict(self):
        return {
            'book':self.book.name,
            'ebook_id':self.ebook_id,
            'book_location':self.book_location,
            'approved': self.approved,
        }


class HardCopy(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    hardCopy_id = models.UUIDField(primary_key = True, default = uuid.uuid4(), editable = False)
    isLent = models.BooleanField(default=False)
    lentTo = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.hardCopy_id)

    def as_dict(self):
        return {
            'book_id':self.book_id.name,
            'hardCopyId':self.hardCopy_id,
            'isLent':self.isLent,
            'lentTo':self.lentTo.first_name + " " + self.lentTo.last_name,
        }