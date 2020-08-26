from uuid import UUID
from django.test import TestCase
from catalog.models import Author, Book, BookInstance, Genre, Language


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label, 'last name')

    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEquals(field_label, 'date of birth')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label, 'Died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 100)

    def test_last_name_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = '%s, %s' % (author.last_name, author.first_name)
        self.assertEquals(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        #This will also fail if the urlconf is not defined.
        self.assertEquals(author.get_absolute_url(), '/catalog/author/1')


class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Book.objects.create(title='Augotia')

    # title
    def test_title_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    # Author
    def test_author_name_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'author')

    # summary
    def test_summary_length(self):
        book = Book.objects.get(id=1)
        summary_text_field = book._meta.get_field('summary').max_length
        self.assertEquals(summary_text_field, 1000)

    def test_summary_help_text(self):
        book = Book.objects.get(id=1)
        summary_help_text = book._meta.get_field('summary').help_text
        self.assertEquals(summary_help_text, 'Enter a brief description of the book')

    # isbn
    def test_isbn_label(self):
        book = Book.objects.get(id=1)
        isbn_label = book._meta.get_field('isbn').verbose_name
        self.assertEquals(isbn_label, 'ISBN')

    def test_isbn_length(self):
        book = Book.objects.get(id=1)
        isbn_max_length = book._meta.get_field('isbn').max_length
        self.assertEquals(isbn_max_length, 13)

    def test_isbn_help_text(self):
        book = Book.objects.get(id=1)
        isbn_help_text = book._meta.get_field('isbn').help_text
        self.assertEquals(isbn_help_text, '13 Character <a href="https://www.usbn-international.org/content/what-isbn">ISBN number</a>')

    # genre
    def test_genre_model(self):
        book = Book.objects.get(id=1)
        excepted_genre = book.genre.create(name='test_genre')
        self.assertEquals(book.genre.all()[0], excepted_genre)

    def test_genre_help_text(self):
        book = Book.objects.get(id=1)
        genre_help_text = book._meta.get_field('genre').help_text
        self.assertEquals(genre_help_text, 'Select a genre for this book')

    # language
    def test_language_model(self):
        book = Book.objects.get(id=1)
        language_excepted_field = book.language.create(language='English')
        self.assertEquals(book.language.all()[0], language_excepted_field)

    def test_language_help_text(self):
        book = Book.objects.get(id=1)
        excepted_help_text = book._meta.get_field('language').help_text
        self.assertEquals(excepted_help_text, 'Select a language for this book')

    def test_book_title(self):
        book = Book.objects.get(id=1)
        self.assertEquals(book.__str__(), "Augotia")

    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        self.assertEquals(book.get_absolute_url(), "/catalog/book/1")

    def test_display_genre_with_no_params(self):
        book = Book.objects.get(id=1)
        self.assertEquals(book.display_genre(), '')

    def test_display_genre_with_params(self):
        book = Book.objects.get(id=1)
        genre1 = book.genre.create(name='test_genre_1')
        genre2 = book.genre.create(name="test_genre_2")
        genre3 = book.genre.create(name="test_genre_3")
        self.assertEquals(book.display_genre(), 'test_genre_1, test_genre_2, test_genre_3')

    def test_display_genre_short_description(self):
        book = Book.objects.get(id=1)
        self.assertEquals(book.display_genre.short_description, "Genre")

    def test_display_language_with_no_params(self):
        book = Book.objects.get(id=1)
        self.assertEquals(book.display_language(), '')

    def test_display_language_with_params(self):
        book = Book.objects.get(id=1)
        language_set = 'English, Germany, Spain'
        language1 = book.language.create(language='English')
        language2 = book.language.create(language='Germany')
        language3 = book.language.create(language='Spain')
        self.assertEquals(book.display_language(), language_set)

    def test_display_language_short_description(self):
        book = Book.objects.get(id=1)
        self.assertEquals(book.display_language.short_description, "Language")


class BookInstanceTestModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        Book.objects.create(title='Fans')
        BookInstance.objects.create(id=1)

    def test_bookinstance_pk(self):
        bookinstance = BookInstance.objects.get(id=1)
        self.assertEquals(bookinstance.pk, UUID('00000000-0000-0000-0000-000000000001'))

    def test_bookinstance_book_label(self):
        bookinstance = BookInstance.objects.get(id=1)
        self.assertEquals(bookinstance._meta.get_field('book').verbose_name, 'book')

    def test_bookinstance_imprint_max_length(self):
        bookinstance = BookInstance.objects.get(id=1)
        self.assertEquals(bookinstance._meta.get_field('imprint').max_length, 200)

    def test_bookinstance_due_back_param_null(self):
        bookinstance = BookInstance.objects.get(id=1)
        self.assertEquals(bookinstance._meta.get_field('due_back').null, True)

    def test_bookinstance_due_back_param_blank(self):
        bookinstance = BookInstance.objects.get(id=1)
        self.assertEquals(bookinstance._meta.get_field('due_back').blank, True)

    # TODO borrower

    def test_status_max_length(self):
        bookinstance = BookInstance.objects.get(id=1)
        self.assertEquals(bookinstance._meta.get_field('status').max_length, 1)

    def test_status_choices(self):
        bookinstance = BookInstance.objects.get(id=1)
        self.assertEquals(bookinstance._meta.get_field('status').choices, bookinstance.LOAN_STATUS)
        self.assertEquals(bookinstance._meta.get_field('status').blank, True)
        self.assertEquals(bookinstance._meta.get_field('status').default, 'm')
        self.assertEquals(bookinstance._meta.get_field('status').help_text, 'Book availability')

    def test_loan_status(self):
        bookinstance = BookInstance.objects.get(id=1)
        excepted_field = bookinstance.LOAN_STATUS
        self.assertEquals(excepted_field[0], ('m', 'Maintenance'))
        self.assertEquals(excepted_field[1], ('o', 'On loan'))
        self.assertEquals(excepted_field[2], ('a', 'Available'))
        self.assertEquals(excepted_field[3], ('r', 'Reserved'))
        # ???
        self.assertEquals(excepted_field[0][0], 'm')
        self.assertEquals(excepted_field[0][1], 'Maintenance')

    def test_bookinstance_is_overdue_without_dueback(self):
        bookinstance = BookInstance.objects.get(id=1)
        self.assertEquals(bookinstance.is_overdue, False)


class GenreTestModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        Genre.objects.create(name='Science fiction')

    def test_genre_name_max_length(self):
        genre = Genre.objects.get(id=1)
        self.assertEquals(genre._meta.get_field('name').max_length, 200)

    def test_genre_help_test(self):
        genre = Genre.objects.get(id=1)
        self.assertEquals(genre._meta.get_field('name').help_text, "Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def test_genre_name(self):
        genre = Genre.objects.get(id=1)
        self.assertEquals(genre.__str__(), "Science fiction")


class LanguageTestModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        Language.objects.create(language='English')

    def test_language_label(self):
        language = Language.objects.get(id=1)
        self.assertEquals(language._meta.get_field('language').verbose_name, 'Language')

    def test_language_max_length(self):
        language = Language.objects.get(id=1)
        self.assertEquals(language._meta.get_field('language').max_length, 200)

    def test_language_help_text(self):
        language = Language.objects.get(id=1)
        self.assertEquals(language._meta.get_field('language').help_text, "Enter a book language (e.g. English, Japan, Germany)")

    def test_language(self):
        language = Language.objects.get(id=1)
        self.assertEquals(language.__str__(), 'English')

