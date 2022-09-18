from dataclasses import field
from django.db import IntegrityError
from .models import *
from .responses import *
from django.views import View
from .exceptions import *
import uuid
from django.http import QueryDict
from .decorators import *
from .constants import *
import re
from .utils import *

class AuthorView(View):

    def __init__(self):
        self.response = init_response()

    def get(self, request, *args, **kwargs):
        try: 
            params = request.GET.dict()
            name = params.get('name')
            # authors = Author.objects.filter(a_id= uuid.UUID(params['a_id']).hex)
            if name:
                author = Author.objects.filter(name__icontains=name).exclude(status ="3")
                if not author:
                    raise ObjectDoesNotExist
                self.response['res_data'] = [author.as_dict() for author in author]
                self.response['res_str'] = FIELD_FETCHED_SUCCESSFULLY.format(field_name = AUTHOR)
                return send_200(self.response)
            else:
                limit=int(params.get('limit', LIMIT))
                offset=int(params.get('offset', OFFSET))
                all_authors = Author.objects.filter().exclude(status ="3")[offset:offset+limit]
                self.response['res_data'] = [author.as_dict() for author in all_authors]
                self.response['res_str'] = FIELD_FETCHED_SUCCESSFULLY.format(field_name=AUTHOR)
                return send_200(self.response)

        except ObjectDoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=AUTHOR)
        except Exception as ex:
            self.response['res_str'] = GENERAL_ERROR + str(ex)
        return send_400(self.response)

    # @Validate_JSON(['meta_data'])
    def post(self, request, *args, **kwargs):
        try:
            params = request.POST.dict()
            get_and_validate(params, ['name'])
            name = params.get('name')
            if Author.objects.filter(name=name):
                raise ObjectAlreadyExist
            description = params.get('description')
            meta_data = params.get('meta_data')
            if meta_data and not validateJSON(meta_data):
                raise JSONError
            author_obj = Author.objects.create(name=name, description=description, meta_data=meta_data)
            self.response['res_data'] = author_obj.as_dict()
            self.response['res_str'] = FIELD_CREATED_SUCCESSFULLY.format(field_name = AUTHOR)
            return send_201(self.response)

        except (ValidationError, FieldBlank) as e:
            self.response['res_str'] = str(e)
        except JSONError:
            self.response['res_str'] = INVALID_JSON
        except ObjectAlreadyExist:
            self.response['res_str'] = FIELD_ALREADY_EXISTS.format(field_name = AUTHOR)
        except Exception as ex:
            self.response['res_str'] = GENERAL_ERROR + str(ex)
        return send_400(self.response)
    
    def delete(self, request,*args, **kwargs):
        try:
            # params = QueryDict(request.body)
            params = json.loads(request.body)
            get_and_validate(params, ['a_id'])
            author_to_delete= Author.objects.get(a_id= uuid.UUID(params['a_id']).hex)
            if author_to_delete.status is "3":
                self.response['res_str'] = FIELD_ALREADY_DELETED.format(field_name = AUTHOR)
                return send_400(self.response)
            author_to_delete.status = "3"
            author_to_delete.save()
            self.response['res_str'] = FIELD_DELETED_SUCCESSFULLY.format(field_name = AUTHOR)
            return send_200(self.response) 

        except (ValidationError, FieldBlank) as e:
            self.response['res_str'] = str(e)
        except Author.DoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=AUTHOR)
        except Exception as ex:
            self.response['res_str'] = GENERAL_ERROR + str(ex)
        return send_400(self.response)
	
    def put(self, request, *args, **kwargs):
        try:
            # params = request.POST.dict()
            # params = QueryDict(request.body)
            params = json.loads(request.body)
            get_and_validate(params, ['a_id']) 
            a_id = params.get('a_id')
            author_obj = Author.objects.get(a_id=a_id)	
            description = params.get('description')
            meta_data = params.get('meta_data')
            if description:
                author_obj.description=description
            if meta_data:
                if validateJSON(meta_data):
                    raise JSONError
                else:
                    author_obj.meta_data=meta_data
            author_obj.save()
            self.response['res_data'] = author_obj.as_dict()
            self.response['res_str'] = FIELD_UPDATED_SUCCESSFULLY.format(field_name = AUTHOR)
            return send_201(self.response)

        except (ValidationError, FieldBlank) as e:
            self.response['res_str'] = str(e)
        except JSONError:
            self.response['res_str'] = INVALID_JSON
        except Author.DoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=AUTHOR)
        except Exception as ex:
            self.response['res_str']= GENERAL_ERROR + str(ex)
        return send_400(self.response)

class LanguageView(View):

    def __init__(self):
        self.response=init_response()

    def get(self, request, *args, **kwargs):
        try:
            params = request.GET.dict()
            name=params.get('name')
            if name:
                language = Language.objects.filter(name__icontains= name).exclude(status ="3")
                if not language.exists():
                    raise ObjectDoesNotExist
                self.response['res_data'] = [language.as_dict() for language in language]
                self.response['res_str'] = FIELD_FETCHED_SUCCESSFULLY.format(field_name=LANGUAGE)
                return send_200(self.response)
            else:
                limit=int(params.get('limit', LIMIT))
                offset=int(params.get('offset', OFFSET))
                all_languages=Language.objects.filter().exclude(status="3")[offset:offset+limit]
                self.response['res_data'] = [language.as_dict() for language in all_languages]
                self.response['res_str'] = FIELD_FETCHED_SUCCESSFULLY.format(field_name=LANGUAGE)
                return send_200(self.response)
    
        except ObjectDoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=LANGUAGE)
        except Exception as ex:
            self.response['res_str'] = GENERAL_ERROR + str(ex)
        return send_400(self.response)

    def post(self, request, *args, **kwargs):
        try:
            params = request.POST.dict()
            get_and_validate(params, ['name'])
            name = params.get('name')
            script = params.get('script')
            about = params.get('about')
            if Language.objects.filter(name=name):
                raise ObjectAlreadyExist
            language_obj = Language.objects.create(name=name, script=script ,about=about)
            self.response['res_data'] = language_obj.as_dict()
            self.response['res_str'] = FIELD_CREATED_SUCCESSFULLY.format(field_name = LANGUAGE)
            return send_201(self.response)

        except (ValidationError, FieldBlank) as e:
            self.response['res_str'] = str(e)
        except ObjectAlreadyExist:
            self.response['res_str'] = FIELD_ALREADY_EXISTS.format(field_name = LANGUAGE)
        except Exception as ex:
            self.response['res_str'] = GENERAL_ERROR + str(ex)
        return send_400(self.response)

    def delete(self, request,*args, **kwargs):
        try:
            params = json.loads(request.body)
            get_and_validate(params, ['lang_id'])
            language_to_delete= Language.objects.get(lang_id= uuid.UUID(params['lang_id']).hex)
            if language_to_delete.status is "3":
                self.response['res_str'] = FIELD_ALREADY_DELETED.format(field_name = LANGUAGE)
                return send_400(self.response)
            language_to_delete.status = "3"
            language_to_delete.save()
            self.response['res_str'] = FIELD_DELETED_SUCCESSFULLY.format(field_name = LANGUAGE)
            return send_200(self.response)

        except (ValidationError, FieldBlank) as e:
            self.response['res_str'] = str(e)
        except Language.DoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=LANGUAGE)
        except Exception as ex:
            self.response['res_str'] = GENERAL_ERROR + str(ex)
        return send_400(self.response)

    def put(self, request, *args, **kwargs):
        try:
            params = json.loads(request.body)
            get_and_validate(params, ['lang_id']) 
            lang_id = params.get('lang_id')
            language_obj = Language.objects.get(lang_id=lang_id)	
            script = params.get('script')
            about = params.get('about')
            if script:
                language_obj.script=script
            if about:
                language_obj.about=about
            language_obj.save()
            self.response['res_data'] = language_obj.as_dict()
            self.response['res_str'] = FIELD_UPDATED_SUCCESSFULLY.format(field_name = LANGUAGE)
            return send_201(self.response)

        except (ValidationError, FieldBlank) as e:
            self.response['res_str'] = str(e)
        except Language.DoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=LANGUAGE)
        except Exception as ex:
            self.response['res_str']= GENERAL_ERROR + str(ex)
        return send_400(self.response)

class PublisherView(View):

    def __init__(self):
        self.response = init_response()

    def get(self, request):
        try:
            params = request.GET.dict()
            name=params.get('name')
            if name:
                publisher = Publisher.objects.filter(name__icontains= name).exclude(status ="3")
                if not publisher.exists():
                    raise ObjectDoesNotExist
                self.response['res_data'] = [publisher.as_dict() for publisher in publisher]
                self.response['res_str'] = FIELD_FETCHED_SUCCESSFULLY.format(field_name=PUBLISHER)
                return send_200(self.response)
            else:
                limit=int(params.get('limit', LIMIT))
                offset=int(params.get('offset', OFFSET))
                all_publishers=Publisher.objects.filter().exclude(status="3")[offset:offset+limit]
                self.response['res_data'] = [publisher.as_dict() for publisher in all_publishers]
                self.response['res_str'] = FIELD_FETCHED_SUCCESSFULLY.format(field_name=PUBLISHER)
                return send_200(self.response)

        except ObjectDoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=PUBLISHER)
        except Exception as ex:
            self.response['res_str'] = GENERAL_ERROR + str(ex)
        return send_400(self.response)
        
    def post(self, request):
        try:
            params = request.POST.dict()
            get_and_validate(params, ['name'])
            name = params.get('name')
            if Publisher.objects.filter(name=name):
                raise ObjectAlreadyExist
            meta_data = params.get('meta_data')
            if meta_data and not validateJSON(meta_data):
                raise JSONError
            publisher_obj = Publisher.objects.create(name=name, meta_data=meta_data)
            self.response['res_data'] = publisher_obj.as_dict()
            self.response['res_str'] = FIELD_CREATED_SUCCESSFULLY.format(field_name = PUBLISHER)
            return send_201(self.response)

        except (ValidationError, FieldBlank) as e:
            self.response['res_str'] = str(e)
        except JSONError:
            self.response['res_str'] = INVALID_JSON
        except ObjectAlreadyExist:
            self.response['res_str'] = FIELD_ALREADY_EXISTS.format(field_name = PUBLISHER)
        except Exception as ex:
            self.response['res_str'] = GENERAL_ERROR + str(ex)
        return send_400(self.response)

    def delete(self, request,*args, **kwargs):
        try:
            params = json.loads(request.body)
            get_and_validate(params, ['pub_id'])
            publisher_to_delete= Publisher.objects.get(pub_id= uuid.UUID(params['pub_id']).hex)
            if publisher_to_delete.status is "3":
                self.response['res_str'] = FIELD_ALREADY_DELETED.format(field_name = PUBLISHER)
                return send_400(self.response)
            publisher_to_delete.status = "3"
            publisher_to_delete.save()
            self.response['res_str'] = FIELD_DELETED_SUCCESSFULLY.format(field_name = PUBLISHER)
            return send_200(self.response)

        except (ValidationError, FieldBlank) as e:
            self.response['res_str'] = str(e)
        except Publisher.DoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=PUBLISHER)
        except Exception as ex:
            self.response['res_str'] = GENERAL_ERROR + str(ex)
        return send_400(self.response)
	
    def put(self, request, *args, **kwargs):
        try:
            params = json.loads(request.body)
            get_and_validate(params, ['pub_id']) 
            pub_id = params.get('pub_id')
            publisher_obj = Publisher.objects.get(pub_id=pub_id)	
            meta_data = params.get('meta_data')
            if meta_data and not validateJSON(meta_data):
                    raise JSONError
            else:
                publisher_obj.meta_data=meta_data
            publisher_obj.save()
            self.response['res_data'] = publisher_obj.as_dict()
            self.response['res_str'] = FIELD_UPDATED_SUCCESSFULLY.format(field_name = PUBLISHER)
            return send_201(self.response)

        except (ValidationError, FieldBlank) as e:
            self.response['res_str'] = str(e)
        except JSONError:
            self.response['res_str'] = INVALID_JSON
        except Publisher.DoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=PUBLISHER)
        except Exception as ex:
            self.response['res_str']= GENERAL_ERROR + str(ex)
        return send_400(self.response)

class BookView(View):

    def __init__(self):
        self.response = init_response()

    def get(self, request, *args, **kwargs):
        try: 
            params = request.GET.dict()
            name = params.get('name')
            if name:
                book = Book.objects.filter(name__icontains=name).exclude(status ="3")
                if not book.exists():
                    raise ObjectDoesNotExist
                self.response['res_data'] = [book.as_dict() for book in book]
                self.response['res_str'] = FIELD_FETCHED_SUCCESSFULLY.format(field_name=BOOK)
                return send_200(self.response)
            else:
                limit=int(params.get('limit', LIMIT))
                offset=int(params.get('offset', OFFSET))
                all_books = Book.objects.filter().exclude(status ="3")[offset:offset+limit]
                self.response['res_data'] = [book.as_dict() for book in all_books]
                self.response['res_str'] = FIELD_FETCHED_SUCCESSFULLY.format(field_name=BOOK)
                return send_200(self.response)

        except ObjectDoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=BOOK)
        except Exception as ex:
            self.response['res_str'] = GENERAL_ERROR + str(ex)
        return send_400(self.response)

    def post(self, request):
        try:
            params = request.POST.dict()
            get_and_validate(params, ['name','publisher','languages','authors'])
            name = params.get('name')
            is_ebook = params.get('is_ebook')
            
            pub_id = params.get('publisher')
            if not pub_id:
                raise PublisherError
            publisher = Publisher.objects.filter(pub_id=pub_id)
            
            if not publisher:
                raise PublisherDoesNotExist

            extra_details = params.get('extra_details')
            if extra_details and not validateJSON(extra_details):
                raise JSONError
            
            lang_ids = params.get('languages').split(',')
            if not lang_ids:
                raise LanguageError
            languages = Language.objects.filter(lang_id__in=lang_ids)
            if not languages:
                raise LanguageDoesNotExist

            a_ids = params.get('authors').split(',')
            if not a_ids:
                raise AuthorError
            authors = Author.objects.filter(a_id__in=a_ids)
            if not authors:
                raise AuthorDoesNotExist
            
            book_obj = Book.objects.create(name=name, publisher=publisher.first(), extra_details=extra_details, is_ebook=is_ebook)
            book_obj.languages.add(*languages)
            book_obj.authors.add(*authors)
            self.response['res_data'] = book_obj.as_dict()
            self.response['res_str'] = FIELD_CREATED_SUCCESSFULLY.format(field_name = BOOK)
            return send_201(self.response)

        except (ValidationError, FieldBlank) as e:
            self.response['res_str'] = str(e)
        except PublisherError:
            self.response['res_str'] = ONE_FEILD_NEEDED.format(field_name=AUTHOR, field_name2 = BOOK)
        except PublisherDoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=PUBLISHER)
        except LanguageError:
            self.response['res_str'] = ONE_FEILD_NEEDED.format(field_name=LANGUAGE, field_name2 = BOOK)
        except LanguageDoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=LANGUAGE)
        except AuthorError:
            self.response['res_str'] = ONE_FEILD_NEEDED.format(field_name=AUTHOR, field_name2 = BOOK)
        except AuthorDoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=AUTHOR)
        except JSONError:
            self.response['res_str'] = INVALID_JSON
        except Exception as ex:
            self.response['res_str'] = GENERAL_ERROR + str(ex)
        return send_400(self.response)

    def delete(self, request,*args, **kwargs):
        try:
            params = json.loads(request.body)
            get_and_validate(params, ['book_id'])
            book_to_delete= Book.objects.get(book_id= uuid.UUID(params['book_id']).hex)
            if book_to_delete.status is "3":
                self.response['res_str'] = FIELD_ALREADY_DELETED.format(field_name = BOOK)
                return send_400(self.response)
            book_to_delete.status = "3"
            book_to_delete.save()
            self.response['res_str'] = FIELD_DELETED_SUCCESSFULLY.format(field_name = BOOK)
            return send_200(self.response)

        except (ValidationError, FieldBlank) as e:
            self.response['res_str'] = str(e)
        except Book.DoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=BOOK)
        except Exception as ex:
            self.response['res_str'] = GENERAL_ERROR + str(ex)
        return send_400(self.response)

    def put(self, request, *args, **kwargs):
        try:
            params = json.loads(request.body)
            get_and_validate(params, ['book_id']) 
            book_id = params.get('book_id')
            book_obj = Book.objects.get(book_id=book_id)	
            extra_details = params.get('extra_details')
            if extra_details:
                if validateJSON(extra_details):
                    raise JSONError
                else:
                    book_obj.extra_details=extra_details

            lang_ids = params.get('languages').split(',')
            if lang_ids:
                languages = Language.objects.filter(lang_id__in=lang_ids)
                if languages:
                    book_obj.languages.add(*languages)
                else:
                    raise LanguageDoesNotExist

            a_ids = params.get('authors').split(',')
            if a_ids:
                authors = Author.objects.filter(a_id__in=a_ids)
                if authors:
                    book_obj.authors.add(*authors)
                else:
                    raise AuthorDoesNotExist
            
            book_obj.save()
            self.response['res_data'] = book_obj.as_dict()
            self.response['res_str'] = FIELD_UPDATED_SUCCESSFULLY.format(field_name = BOOK)
            return send_201(self.response)

        except (ValidationError, FieldBlank) as e:
            self.response['res_str'] = str(e)
        except JSONError:
            self.response['res_str'] = INVALID_JSON
        except LanguageDoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=LANGUAGE)
        except AuthorDoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=AUTHOR)
        except Book.DoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=BOOK)
        except Exception as ex:
            self.response['res_str']= GENERAL_ERROR + str(ex)
        return send_400(self.response)

class UserView(View):
    
    def __init__(self):
        self.response = init_response()

    def get(self, request, *args, **kwargs):
        try: 
            params = request.GET.dict()
            first_name = params.get('first_name')
            email = params.get('email')
            if first_name:
                users = User.objects.filter(first_name__icontains=first_name).exclude(status ="3")
                if not users:
                    raise ObjectDoesNotExist
                self.response['res_data'] = [user.as_dict() for user in users]
                self.response['res_str'] = FIELD_FETCHED_SUCCESSFULLY.format(field_name=USER)
                return send_200(self.response)
            elif email:
                user = User.objects.filter(email=email).exclude(status ="3")
                if not user:
                    raise ObjectDoesNotExist
                self.response['res_data'] = [user.as_dict() for user in user]
                self.response['res_str'] = FIELD_FETCHED_SUCCESSFULLY.format(field_name=USER)
                return send_200(self.response)
            else:
                limit=int(params.get('limit', LIMIT))
                offset=int(params.get('offset', OFFSET))
                all_users = User.objects.filter().exclude(status ="3")[offset:offset+limit]
                self.response['res_data'] = [user.as_dict() for user in all_users]
                self.response['res_str'] = FIELD_FETCHED_SUCCESSFULLY.format(field_name=USER)
                return send_200(self.response)

        except ObjectDoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=USER)
        except Exception as ex:
            self.response['res_str'] = GENERAL_ERROR + str(ex)
        return send_400(self.response)    

    def post(self, request):
        try:
            params = request.POST.dict()
            books=None
            get_and_validate(params, ['first_name','email'])
            first_name = params.get('first_name')
            middle_name = params.get('middle_name')
            last_name = params.get('last_name')
            mobile = params.get('mobile')
            email = params.get('email') 
            pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'
            if not re.fullmatch(pattern, email):
                raise ValidationError("Email Id is not valid")

            role= params.get('role')
            meta_data = params.get('meta_data')
            if meta_data and not validateJSON(meta_data):
                raise JSONError

            subscription = params.get('subscription')
            book_ids = params.get('favorites')
            if book_ids:
                book_ids =book_ids.split(',')
                books = Book.objects.filter(book_id__in=book_ids)
                if not books:
                    raise BookDoesNotExist
            
            user_obj = User.objects.create(first_name=first_name, middle_name=middle_name, last_name=last_name, mobile=mobile, email=email, meta_data =meta_data, role=role, subscription=subscription)
            user_obj.status="1"
            if books:
                user_obj.favorites.add(*books)
            user_obj.save()
            self.response['res_data'] = user_obj.as_dict()
            self.response['res_str'] = FIELD_CREATED_SUCCESSFULLY.format(field_name = USER)
            return send_201(self.response)

        except (ValidationError, FieldBlank) as e:
            self.response['res_str'] = str(e)
        except IntegrityError:
            self.response['res_str'] = INTEGRITY_ERROR
        except BookDoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=BOOK)
        except JSONError:
            self.response['res_str'] = INVALID_JSON
        except Exception as ex:
            self.response['res_str'] = GENERAL_ERROR + str(ex)
        return send_400(self.response)

    def delete(self, request,*args, **kwargs):
        try:
            params = json.loads(request.body)
            get_and_validate(params, ['user_id'])
            user_to_delete= User.objects.get(user_id= uuid.UUID(params['user_id']).hex)
            if user_to_delete.status is "3":
                self.response['res_str'] = FIELD_ALREADY_DELETED.format(field_name = USER)
                return send_400(self.response)
            user_to_delete.status = "3"
            user_to_delete.save()
            self.response['res_str'] = FIELD_DELETED_SUCCESSFULLY.format(field_name = USER)
            return send_200(self.response)

        except (ValidationError, FieldBlank) as e:
            self.response['res_str'] = str(e)
        except User.DoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=USER)
        except Exception as ex:
            self.response['res_str'] = GENERAL_ERROR + str(ex)
        return send_400(self.response)

    def put (self, request, *args, **kwargs):
        try:
            params = json.loads(request.body)
            get_and_validate(params,['email_id'])
            user_obj=User.objects.get(email_id=params.get('email_id'))
            mobile=params.get('mobile')
            meta_data = params.get('meta_data')
            if meta_data and not validateJSON(meta_data):
                raise JSONError
            else:
                user_obj.meta_data=meta_data
            subscription=params.get('subscription')
            if subscription:
                user_obj.subscription=True
            user_obj.mobile=mobile
            user_obj.save()
            self.response['res_data'] = user_obj.as_dict()
            self.response['res_str'] = FIELD_UPDATED_SUCCESSFULLY.format(field_name = AUTHOR)
            return send_201(self.response)

        except (ValidationError,FieldBlank) as ex:
            self.response['res_str'] = str(ex)
        except JSONError:
            self.response['res_str'] = INVALID_JSON
        except User.DoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=USER)
        except Exception as ex:
            self.response['res_str'] = GENERAL_ERROR + str(ex)
        return send_400(self.response)

class EbookView(View):
    
    def __init__(self):
        self.response = init_response()

    def get(self, request, *args, **kwargs):
        try: 
            params = request.GET.dict()
            book_name = params.get('book_name')
            if book_name:
                ebook = Ebook.objects.filter(book__in=Book.objects.filter(name__icontains=book_name))
                if not ebook.exists():
                    raise ObjectDoesNotExist
                self.response['res_data'] = [ebook.as_dict() for ebook in ebook]
                self.response['res_str'] = FIELD_FETCHED_SUCCESSFULLY.format(field_name=EBOOK)
                return send_200(self.response)
            else:
                limit=int(params.get('limit', LIMIT))
                offset=int(params.get('offset', OFFSET))
                all_ebooks = Ebook.objects.filter(approved =True)[offset:offset+limit]
                self.response['res_data'] = [ebook.as_dict() for ebook in all_ebooks]
                self.response['res_str'] =FIELD_FETCHED_SUCCESSFULLY.format(field_name=EBOOK)
                return send_200(self.response)

        except ObjectDoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=EBOOK)
        except Exception as ex:
            self.response['res_str'] = GENERAL_ERROR + str(ex)
        return send_400(self.response)

    def post(self, request):
        try:
            params = request.POST.dict()
            get_and_validate(params, ['book'])
            book = params.get('book')
            if not book:
                raise BookError
            book = Book.objects.filter(book_id=book)
            if not book:
                raise BookDoesNotExist
            book_location = params.get('book_location')
            ebook_obj = Ebook.objects.create(book=book.first(), book_location=book_location)            
            self.response['res_data'] = ebook_obj.as_dict()
            self.response['res_str'] = FIELD_CREATED_SUCCESSFULLY.format(field_name = EBOOK)
            return send_201(self.response)

        except (ValidationError, FieldBlank) as e:
            self.response['res_str'] = str(e)
        except BookError:
            self.response['res_str'] = ONE_FEILD_NEEDED.format(field_name=BOOK, field_name2 = EBOOK)
        except BookDoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=BOOK)
        except Exception as ex:
            self.response['res_str'] = GENERAL_ERROR + str(ex)
        return send_400(self.response)

    def delete(self, request,*args, **kwargs):
        try:
            params = json.loads(request.body)
            get_and_validate(params, ['ebook_id'])
            ebook_to_delete= Ebook.objects.get(ebook_id= uuid.UUID(params['ebook_id']).hex)
            ebook_to_delete.delete()
            self.response['res_str'] = FIELD_DELETED_SUCCESSFULLY.format(field_name = EBOOK)
            return send_200(self.response)

        except (ValidationError, FieldBlank) as e:
            self.response['res_str'] = str(e)
        except Ebook.DoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=EBOOK)
        except Exception as ex:
            self.response['res_str'] = GENERAL_ERROR + str(ex)
        return send_400(self.response)

    def put(self,request):
        try:
            params = json.loads(request.body)
            get_and_validate(params, ['role', 'ebook_id'])
            role= params.get('role')
            ebook = Ebook.objects.get(ebook_id= uuid.UUID(params['ebook_id']).hex)
            if(role is "1" or role is "2"):
                ebook.approved = True
                ebook.save()
                self.response['res_data'] = ebook.as_dict()
                self.response['res_str'] = FIELD_APPROVED_SUCCESSFULLY.format(field_name = EBOOK)
                return send_200(self.response)
            else:
                self.response['res_str'] = LOGIN_ERROR
                return send_200(self.response)
        except Ebook.DoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=EBOOK)
        except (ValidationError, FieldBlank) as e:
            self.response['res_str'] = str(e)
        return send_400(self.response)

class HardCopyView(View):
    
    def __init__(self):
        self.response = init_response()

    def get(self, request, *args, **kwargs):
        try: 
            params = request.GET.dict()
            book_name = params.get('book_name')
            if book_name:
                hardCopy = HardCopy.objects.filter(book__in=Book.objects.filter(name__icontains=book_name))
                if not hardCopy.exists():
                    raise ObjectDoesNotExist
                self.response['res_data'] = [hardCopy.as_dict() for hardCopy in hardCopy]
                self.response['res_str'] = FIELD_FETCHED_SUCCESSFULLY.format(field_name=HARDCOPY)
                return send_200(self.response)
            else:
                limit=int(params.get('limit', LIMIT))
                offset=int(params.get('offset', OFFSET))
                all_hardCopys = HardCopy.objects.filter()[offset:offset+limit]
                self.response['res_data'] = [hardCopy.as_dict() for hardCopy in all_hardCopys]
                self.response['res_str'] = FIELD_FETCHED_SUCCESSFULLY.format(field_name=HARDCOPY)
                return send_200(self.response)

        except ObjectDoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=HARDCOPY)
        except Exception as ex:
            self.response['res_str'] = GENERAL_ERROR + str(ex)
        return send_400(self.response)

    def post(self, request):
        try:
            params = request.POST.dict()
            get_and_validate(params, ['book'])
            book_id = params.get('book')
            if not book_id:
                raise BookError
            book = Book.objects.filter(book_id=book_id)
            if not book:
                raise BookDoesNotExist
            isLent = params.get('isLent')
            user_id= params.get('lentTo')
            if isLent:
                user_lentTo = User.objects.filter(user_id=user_id)
                hardCopy_obj = HardCopy.objects.create(book=book.first(), isLent=isLent,lentTo= user_lentTo.first())
            else:
                hardCopy_obj = HardCopy.objects.create(book=book.first(), isLent=isLent)
            self.response['res_data'] = hardCopy_obj.as_dict()
            self.response['res_str'] = FIELD_CREATED_SUCCESSFULLY.format(field_name = HARDCOPY)
            return send_201(self.response)

        except (ValidationError, FieldBlank) as e:
            self.response['res_str'] = str(e)
        except BookError:
            self.response['res_str'] = ONE_FEILD_NEEDED.format(field_name=BOOK, field_name2 = HARDCOPY)
        except BookDoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=BOOK)
        except Exception as ex:
            self.response['res_str'] = GENERAL_ERROR + str(ex)
        return send_400(self.response)

    def delete(self, request,id,*args, **kwargs):
        try:
            params = json.loads(request.body)
            get_and_validate(params,['hardCopy_id'])
            hardCopy_id=params.get('hardCopy_id')
            hardCopy_to_delete= HardCopy.objects.get(hardCopy_id = hardCopy_id)
            hardCopy_to_delete.delete()
            self.response['res_data'] = f'HardCopy id was {id}'
            self.response['res_str'] = FIELD_DELETED_SUCCESSFULLY.format(field_name = HARDCOPY)
            return send_200(self.response)

        except (ValidationError, FieldBlank) as e:
            self.response['res_str'] = str(e)
        except HardCopy.DoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=HARDCOPY)
            return send_404(self.response)

    def put (self, request, *args, **kwargs):
        try:
            params = json.loads(request.body)
            get_and_validate(params,['hardCopy_id'])
            hardCopy_id=params.get('hardCopy_id')
            hardcopy_obj=HardCopy.objects.get(hardCopy_id=hardCopy_id)
            
            is_lent=params.get('is_lent')
            if is_lent is False:
                lent_to=params.get('lent_to')
                user_obj= User.objects.filter(email_id=lent_to)
            if lent_to and not User.objects.filter(email_id=lent_to).exists():
                raise ObjectDoesNotExist("User with this "+str(lent_to)+" does not exist")
            elif lent_to:
                user_obj=User.objects.get(email_id=lent_to)
            
            hardcopy_obj.is_lent=True
            hardcopy_obj.lent_to=user_obj
            hardcopy_obj.save()
            self.response['res_data'] = hardcopy_obj.as_dict()
            self.response['res_str'] = FIELD_UPDATED_SUCCESSFULLY.format(field_name = HARDCOPY)
            return send_201(self.response)
        
        except (ValidationError, FieldBlank) as e:
            self.response['res_str'] = str(e)
        except HardCopy.DoesNotExist:
            self.response['res_str'] = OBJECT_NOT_FOUND.format(field_name=HARDCOPY)
        except Exception as ex:
            self.response['res_str']= GENERAL_ERROR + str(ex)
        return send_400(self.response)