from django.db.models import When
from .models import *
from .responses import *
from django.views import View
from .exceptions import *
import uuid
import json
from django.http import QueryDict
from .decorators import *
from .constants import *
class AuthorView(View):
    
    def __init__(self):
        self.response = init_response()
    
    def get_and_validate_author(self, params, required_keys=[]):
        keys=params.keys()
        for key in required_keys:
            if key not in keys:
                raise ValidationError("Required Key Missing : " + key)

    def validateJSON(self, meta_data):
        try:
            json.loads(meta_data)
        except:
            return False
        return True

    def get(self, request, *args, **kwargs):
        try: 
            params = request.GET.dict()
            name = params.get('name')
            # authors = Author.objects.filter(a_id= uuid.UUID(params['a_id']).hex)
            if name:
                # self.get_and_validate_author(params, ['name'])
                author = Author.objects.filter(name=name)
                if not author.exists():
                    raise ObjectDoesNotExist
                self.response['res_data'] = [author.as_dict() for author in author]
                self.response['res_str'] = "Authors Successfully Fetched"
                return send_200(self.response)
            else:
                # limit=params.get('limit', LIMIT)
                # offset=params.get('offset', OFFSET)
                limit=LIMIT
                offset=OFFSET
                all_authors = Author.objects.filter(status ="1", status = "2")[offset:offset+limit]
                self.response['res_data'] = [author.as_dict() for author in all_authors]
                self.response['res_str'] = "Authors Successfully Fetched"
                return send_200(self.response)

        except ValidationError as e:
            self.response['res_str'] = str(e)
        except ObjectDoesNotExist:
            self.response['res_str'] = "Author Not Found"
        except Exception as ex:
            self.response['res_str'] = "Unable to process Error : " + str(ex)
        return send_400(self.response)

    # @Validate_JSON(['meta_data'])
    def post(self, request, *args, **kwargs):
        try:
            params = request.POST.dict()
            self.get_and_validate_author(params, ['name'])
            
            name = params.get('name')
            description = params.get('description')
            meta_data = params.get('meta_data')
            if meta_data and not self.validateJSON(meta_data):
                raise JSONError
            author_obj = Author.objects.create(name=name, description=description, meta_data=meta_data)
            self.response['res_data'] = author_obj.as_dict()
            self.response['res_str'] = "Author Successfully Created"
            return send_201(self.response)

        except ValidationError as e:
            self.response['res_str'] = str(e)
        except JSONError:
            self.response['res_str'] = "JSON is not Valid JSON"
        except Exception as ex:
            self.response['res_str'] = "Unable to process Error : " + str(ex)
        return send_400(self.response)
    
    def delete(self, request,*args, **kwargs):
        try:
            # params = QueryDict(request.body)
            params = json.loads(request.body)

            self.get_and_validate_author(params, ['a_id'])
            author_to_delete= Author.objects.get(a_id= uuid.UUID(params['a_id']).hex)
            if author_to_delete.status is "3":
                self.response['res_str'] = "Author Already Deleted"
                return send_400(self.response)
            author_to_delete.status = "3"
            author_to_delete.save()
            self.response['res_str'] = "Author Successfully Deleted"
            return send_200(self.response)     

        except ValidationError as e:
            self.response['res_str'] = str(e)
        except Author.DoesNotExist:
            self.response['res_str'] = "Author Not Found"
        except Exception as ex:
            self.response['res_str'] = "Unable to process Error : " + str(ex)
        return send_400(self.response)



class LanguageView(View):

    def __init__(self):
        self.response=init_response()

    def get(self, request, *args, **kwargs):
        params = request.GET.dict()
        lang_id=params.get('lang_id')
        if lang_id:
            language = Language.objects.get(lang_id= lang_id)
            self.response['res_data'] = language.as_dict()  
            self.response['res_str'] = "Language Successfully Fetched"
            return send_200(self.response)
        else:
            all_languages=Language.objects.all()
            res={}
            for language in all_languages:
                res[language.lang_id]=language.as_dict()
            self.response['res_data'] = res
            self.response['res_str'] = "Languages Successfully Fetched"
            return send_200(self.response)
    
    def post(self, request, *args, **kwargs):
        params=request.POST.dict()
        lang_id = params.get('lang_id')
        name = params.get('name')
        script = params.get('script')
        about = params.get('about')
        language_obj = Language.objects.create(lang_id=lang_id, name=name, script=script ,about=about)
        self.response['res_data'] = language_obj.as_dict()
        self.response['res_str'] = "Language Successfully Created"
        return send_201(self.response)

    def delete(self, request,*args, **kwargs):
        try:
            lang_id=request.GET.dict()
            language_to_delete= Language.objects.get(lang_id= uuid.UUID(lang_id['lang_id']).hex)
        except Language.DoesNotExist:
            self.response['res_str'] = "Language Not Found"
            return send_404(self.response)
        language_to_delete.delete()
        self.response['res_data'] = f'Language id was {lang_id}'
        self.response['res_str'] = "Language Successfully Deleted"
        return send_200(self.response)

class PublisherView(View):

    def __init__(self):
        self.response = init_response()

    def get(self, request):
        params = request.GET.dict()
        pub_id=params.get('pub_id')
        if pub_id:
            publisher = Publisher.objects.get(pub_id= pub_id)
            self.response['res_data'] = publisher.as_dict()  
            self.response['res_str'] = "Publisher Successfully Fetched"
            return send_200(self.response)
        else:
            all_publishers = Publisher.objects.all()
            res={}
            for publisher in all_publishers:
                res[publisher.pub_id]=publisher.as_dict()
            self.response['res_data'] = res
            self.response['res_str'] = "Publishers Successfully Fetched"
            return send_200(self.response)

    def post(self, request):
        params = request.POST.dict()
        pub_id = params.get('pub_id')
        name = params.get('name')
        meta_data = params.get('meta_data')
        publisher_obj = Publisher.objects.create(pub_id=pub_id, name=name, meta_data=meta_data)
        self.response['res_data'] = publisher_obj.as_dict()
        self.response['res_str'] = "Publisher Successfully Created"
        return send_201(self.response)

    def delete(self, request,id,*args, **kwargs):
        try:
            publisher_to_delete= Publisher.objects.get(pub_id= id)
        except Publisher.DoesNotExist:
            self.response['res_str'] = "Publisher Not Found"
            return send_404(self.response)
        publisher_to_delete.delete()
        self.response['res_data'] = f'Publisher id was {id}'
        self.response['res_str'] = "Publisher Successfully Deleted"
        return send_200(self.response)

class BookView(View):

    def __init__(self):
        self.response = init_response()

    def get(self, request):
        params = request.GET.dict()
        book_id=params.get('book_id')
        if book_id:
            book = Book.objects.get(book_id= book_id)
            self.response['res_data'] = book.as_dict()
            self.response['res_str'] = "Book Successfully Fetched"
            return send_200(self.response)
        else:
            all_books = Book.objects.all()
            res={}
            # import pdb; pdb.set_trace()
            for book in all_books:
                res[book.book_id]=book.as_dict()
            self.response['res_data'] = res
            self.response['res_str'] = "Books Successfully Fetched"
            return send_200(self.response)

    def post(self, request):
        params = request.POST.dict()
        book_id = params.get('book_id')
        name = params.get('name')

        pub_id = params.get('publisher')
        publisher = Publisher.objects.get(pub_id= pub_id)

        extra_details = params.get('extra_details')
        is_ebook = params.get('is_ebook')
        book_obj = Book.objects.create(book_id=book_id, name=name, publisher=publisher, extra_details=extra_details, is_ebook=is_ebook)

        lang_id = params.get('languages')
        language = Language.objects.get(lang_id=lang_id)
        book_obj.languages.add(language)
        a_id = params.get('authors')
        author = Author.objects.get(a_id=a_id)
        book_obj.authors.add(author)
        self.response['res_data'] = book_obj.as_dict()
        self.response['res_str'] = "Book Successfully Created"
        return send_201(self.response)

    def delete(self, request,id,*args, **kwargs):
        try:
            book_to_delete= Book.objects.get(book_id= id)
        except Book.DoesNotExist:
            self.response['res_str'] = "Book Not Found"
            return send_404(self.response)
        book_to_delete.delete()
        self.response['res_data'] = f'Book id was {id}'
        self.response['res_str'] = "Book Successfully Deleted"
        return send_200(self.response)


class EbookView(View):
    
    def __init__(self):
        self.response = init_response()

    def get(self, request, *args, **kwargs):
        ebook_id = request.GET.dict()
        # ebook_id=params.get(uuid.UUID(params['ebook_id']).hex)
        # import pdb
        # pdb.set_trace()
        if ebook_id:
            ebook = Ebook.objects.get(ebook_id= uuid.UUID(ebook_id['ebook_id']).hex)
            if ebook.approved is True:
                ebook = ebook.as_dict()
                self.response['res_data'] = ebook  
                self.response['res_str'] = "Ebook Successfully Fetched"
                return send_200(self.response)
            else:
                self.response['res_str'] = "Ebook not yet approved"
                return send_200(self.response)
        else:
            all_ebooks = Ebook.objects.filter(approved=True)
            res=[]
            for ebook in all_ebooks:
                res.append(ebook.as_dict())
            self.response['res_data'] = res
            self.response['res_str'] = "Ebooks Successfully Fetched"
            return send_200(self.response)


    def post(self, request, *args, **kwargs):
        params = request.POST.dict()
        book_id = params.get('book_id')
        book = Book.objects.get(book_id=book_id)
        
        ebook_id = params.get('ebook_id')
        book_location = params.get('book_location')
        ebook_obj = Ebook.objects.create(book=book, ebook_id=ebook_id, book_location=book_location)
        self.response['res_data'] = ebook_obj.as_dict()
        self.response['res_str'] = "Ebook Submitted for approval"
        return send_201(self.response)

    def delete(self, request,id,*args, **kwargs):
        try:
            ebook_to_delete= Ebook.objects.get(ebook_id= id)
        except Ebook.DoesNotExist:
            self.response['res_str'] = "Ebook Not Found"
            return send_404(self.response)
        ebook_to_delete.delete()
        self.response['res_data'] = f'Ebook id was {id}'
        self.response['res_str'] = "Ebook Successfully Deleted"
        return send_200(self.response)

    def put(self,request):
        params= request.GET.dict()
        role= params.get('user_type')
        
        try:
            ebook = Ebook.objects.get(ebook_id= uuid.UUID(params['ebook_id']).hex)
            if(role is "1" or role is "2"):
                # ebook_obj = Ebook.objects.get(ebook_id=ebook)
                ebook.approved = True
                ebook.save()
                self.response['res_data'] = ebook.as_dict()
                self.response['res_str'] = "Ebook was Successfully approved"
                return send_200(self.response)
            else:
                self.response['res_str'] = "Login to Admin or Librarian to approve the ebook"
                return send_200(self.response)
        except Ebook.DoesNotExist:
            self.response['res_str'] = "Ebook Not Found"
            return send_404(self.response)


class UserView(View):
    
    def __init__(self):
        self.response = init_response()

    def get(self, request, *args, **kwargs):
        params = request.GET.dict()
        user_id=params.get('user_id')
        if user_id:
            user = User.objects.get(user_id = user_id)
            self.response['res_data'] = user.as_dict()  
            self.response['res_str'] = "User Successfully Fetched"
            return send_200(self.response)
        else:
            all_users = User.objects.all()
            res={}
            for user in all_users:
                res[user.user_id]=user.as_dict()
            self.response['res_data'] = res
            self.response['res_str'] = "Users Successfully Fetched"
            return send_200(self.response)


    def post(self, request, *args, **kwargs):
        params = request.POST.dict()
        user_id = params.get('user_id')
        first_name = params.get('first_name')
        middle_name = params.get('middle_name')
        last_name = params.get('last_name')
        mobile = params.get('mobile')
        email = params.get('email')
        meta_data = params.get('meta_data')
        role = params.get('role')
        subscription = params.get('subscription')

        user_obj = User.objects.create(user_id=user_id, first_name=first_name, middle_name=middle_name, last_name=last_name, mobile=mobile, email=email, meta_data =meta_data, role=role, subscription=subscription)
        book_id = params.get('favorites')
        book = Book.objects.get(book_id=book_id)
        user_obj.favorites.add(book)

        self.response['res_data'] = user_obj.as_dict()
        self.response['res_str'] = "User Successfully Created"
        return send_201(self.response)

    def delete(self, request,id,*args, **kwargs):
        try:
            user_to_delete= User.objects.get(user_id= id)
        except User.DoesNotExist:
            self.response['res_str'] = "User Not Found"
            return send_404(self.response)
        user_to_delete.delete()
        self.response['res_data'] = f'User id was {id}'
        self.response['res_str'] = "User Successfully Deleted"
        return send_200(self.response)


class HardCopyView(View):
    
    def __init__(self):
        self.response = init_response()

    def get(self, request, *args, **kwargs):
        params = request.GET.dict()
        hardCopy_id=params.get('hardCopy_id')
        if hardCopy_id:
            hardCopy = HardCopy.objects.get(hardCopy_id= hardCopy_id)
            self.response['res_data'] = hardCopy.as_dict()  
            self.response['res_str'] = "HardCopy Successfully Fetched"
            return send_200(self.response)
        else:
            all_hardCopys = HardCopy.objects.all()
            res={}
            for hardCopy in all_hardCopys:
                res[hardCopy.hardCopy_id]=hardCopy.as_dict()
            self.response['res_data'] = res
            self.response['res_str'] = "HardCopys Successfully Fetched"
            return send_200(self.response)


    def post(self, request, *args, **kwargs):
        params = request.POST.dict()
        id = params.get('book_id')
        book_id = Book.objects.get(book_id=id)
        hardCopy_id = params.get('hardCopy_id')
        isLent = params.get('isLent')
        user_id= params.get('lentTo')
        lentTo = User.objects.get(user_id=user_id)

        hardCopy_obj = HardCopy.objects.create(book_id=book_id, hardCopy_id=hardCopy_id, isLent=isLent, lentTo=lentTo)
        self.response['res_data'] = hardCopy_obj.as_dict()
        self.response['res_str'] = "HardCopy Successfully Created"
        return send_201(self.response)

    def delete(self, request,id,*args, **kwargs):
        try:
            hardCopy_to_delete= HardCopy.objects.get(hardCopy_id = id)
        except HardCopy.DoesNotExist:
            self.response['res_str'] = "HardCopy Not Found"
            return send_404(self.response)
        hardCopy_to_delete.delete()
        self.response['res_data'] = f'HardCopy id was {id}'
        self.response['res_str'] = "HardCopy Successfully Deleted"
        return send_200(self.response)

# class Search(View):
#     def get(self, request,*args, **kwargs):
#         params=request.GET.dict()
#         category =params.get('category')
#         name=params.get('name')
#         if category is "author" or "Author":
#             self.search(Author,name)
#         elif category is "book" or "Book":
#             self.search(Book,name)
#         else:
#             self.response['res_str'] = f'{category} is not a valid category'
#             return send_404(self.response)

#     def search(self, request, category, name):
#         search_class= category
#         name=name
#         all_obj = search_class.objects.filter(name = name)
#         if all_obj:
#             res=[]
#             for obj in all_obj:
#                 res.append(obj.as_dict())
#             self.response['res_data'] = res
#             self.response['res_str'] = f'{category}s Successfully Fetched'
#             return send_200(self.response)
#         else: 
#             self.response['res_str'] = f'No {category} found'
#             return send_404(self.response)
