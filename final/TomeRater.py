class User:
    '''User class holds information about users

    To create user you have to state Name and email address.
    Users have methods:
    get_email
    change_email
    read_book
    get_average_rating'''

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        return "User's e-mail has been succesfully updated"

    def __repr__(self):
        return "User {name}, e-mail: {email}, books read: {books}".format(
                    name = self.name, email = self.email, 
                    books = len(self.books.keys()))

    def __eq__(self, other_user):
        return self.email == other_user.email and self.name == other_user.name 

    def __ne__(self, other_user):
        return self.email != other_user.email and self.name != other_user.name

    def read_book(self, book, rating = None):
        self.books[book.title] = rating

    def get_average_rating(self):
        sum = 0
        count = len(self.books.values())
        if count <= 0:
            avg_rating = 0
        else:
            for book in self.books.keys():
                if self.books[book] == None:
                    pass
                else:
                    sum += self.books.get(book, 0)
            avg_rating = sum / count
        return avg_rating


class Book:
    '''Holds info on Books
    
    To create book you have to input title and uniqe isbn number.
    Book object is hashable.
    Available methods:
    get_title
    get_isbn
    set_isbn
    add_rating
    get_average_rating'''
    
    def __init__(self, title, isbn):
        self.title = title #string
        self.isbn = isbn #number
        self.ratings = []

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.title == other.title and self.isbn == other.isbn
        return False
            
    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.title != other.title and self.isbn != other.isbn
        return True

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        return "Book titled {}".format(self.title)

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print("ISBN number has been updated")

    def add_rating(self, rating):
        if rating > 4 or rating < 0:
            print("Invalid Rating")
        else:
            self.ratings.append(rating)

    def get_average_rating(self):
        sum = 0 #sum of ratings
        count = len(self.ratings) #number of ratings added
        if count <= 0:
            avg_rating = 0
        else:
            for rating in self.ratings:
                sum += rating
            avg_rating = sum /count
        return avg_rating



class Fiction(Book):
    '''Holds information about books that are literature works

    Fiction is a subclass of Book.
    To create finction you have to give additionally an author.
    Available methods:
    get_author'''

    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title = self.title, 
                                            author = self.author)


class Non_Fiction(Book):
    '''Holds information about books that are not literature pieces
    
    Non_Fiction is a subclass of Book.
    Additional info needed: subject and level.
    Available methods:
    get_subject
    get_level'''

    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level        

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title} - a {level} manual on {subject}".format(
                    title = self.title, 
                    level = self.level, 
                    subject = self.subject
                    )


class TomeRater:
    '''TomeRater is application for binding users with book they read and ratings.
    
    TomeRater has dictionaries of users and books.
    Available methods and explanation:
    create_book - creates Book object
    create_novel - creates Fiction object
    create_non_fiction - creates Non_Fiction object
    add_user - creates User object
    add_book_to_user - attributes book to a user with possible rating (default None)
    print_catalog - prints list of books
    print_users - prints list of users
    print_users_names - prints list of only user names
    most_read_book - returns book that was read te most_positive
    highest_rated_book - returns book that has highest average rating
    most_positive_user - returns user that has highest average rating
    '''
    def __init__(self):
        self.users = {} #maps users emails to user objects
        self.books = {} #maps book object to number of users that read it
        self.isbn = []  # for checking that every book has unique isbn

    def __repr__(self):
        return '''This is a TomeRater app for managing users and books, 
        that currently holds {} users and {} books.'''.format(len(self.users),
         len(self.books))

    def __eq__(self, other):
        return self.users == other.users and self.books == other.books

    def __ne__(self, other):
        return self.users != other.users and self.books != other.books

        # creates Book object
    def create_book(self, title, isbn):
        if isbn in self.isbn:
            print("Book with such isbn:{} has already been created".format(isbn))
        else:
            new_book = Book(title, isbn)
            self.isbn.append(isbn)
            return new_book
    
    # creates Fiction object
    def create_novel(self, title, author, isbn):
        if isbn in self.isbn:
            print ("Book with such isbn:{} has already been created".format(isbn))
        else:
            new_novel = Fiction(title, author, isbn)
            self.isbn.append(isbn)
            return new_novel

    # creates Non_Fiction object
    def create_non_fiction(self, title, subject, level, isbn):
        if isbn in self.isbn:
            print ("Book with such isbn:{} has already been created".format(isbn))
        else:
            new_manual = Non_Fiction(title, subject, level, isbn)
            self.isbn.append(isbn)
            return new_manual

            # attributes book to a user
    def add_book_to_user(self, book, email, rating = None):
        if email in self.users.keys():
            self.users.get(email).read_book(book, rating)
            if rating != None:
                book.add_rating(rating)
            if book in self.books:
                self.books[book] += 1
            else:
                self.books[book] = 1
        else:
            print("No user with email {}".format(email))

        
    def add_user(self, name, email, user_books = None):
        # list of accepted domain suffixes
        checklist = ['.com','.edu','.org','.pl','co.uk']
        endings_count = 0
        
        #checking email validity
        if '@' in email:
            for check in checklist:
                if check in email:
                    endings_count +=1
        if endings_count <= 0:
            print("Provided e-mail: {} is invalid.".format(email))
        
        #adding new user
        else:
            if email in self.users:
                print("User with such e-mail: {} already exists".format(email))
            else:
                new_user = User(name, email)
                self.users[email] = new_user
                if user_books != None:
                    for book in user_books:
                        TomeRater.add_book_to_user(self, book, email)

    def print_catalog(self):
        for bk in self.books:
            print(bk)

    def print_users(self):
        for usr in self.users.values():
            print(usr)

    def print_users_names(self):
        for usr in self.users.values():
            print(usr.name)

    def most_read_book(self):
        curent_read_count = 0
        for book in self.books:
            if self.books[book] > curent_read_count:
                curent_read_count = self.books[book]
                most_read = book
            else:
                pass
        return most_read

    def highest_rated_book(self):
        highest_avg_rating = 0
        for book in self.books:
            if book.get_average_rating() > highest_avg_rating:
                highest_avg_rating = book.get_average_rating()
                highest_rated = book
        return highest_rated

    def most_positive_user(self):
        highest_avg_rating = 0
        for usr in self.users.values():
            if usr.get_average_rating() > highest_avg_rating:
                highest_avg_rating = usr.get_average_rating()
                most_positive = usr
        return most_positive

    def get_n_most_read_books(self, number): 
        if number > 0:
            lista = []
            most_read = self.most_read_book()
            current_count = self.books[most_read]
            while current_count > 0:
                for b in self.books:
                    if self.books[b] == current_count and len(lista) < number:
                        lista.append(b)
                    else:
                        pass
                current_count -= 1
            return lista
        else:
            return 0

