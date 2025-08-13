class Book:
    def __init__(self, title, author, ISBN, year):
        self.title = title
        self.author = author
        self.ISBN = ISBN
        self.year = year
        self.is_available = True

    def borrow_book(self):
        if self.is_available:
            self.is_available = False
            return f"You have borrowed '{self.title}' by {self.author}."
        else:
            raise ValueError(f"'{self.title}' is currently borrowed.")

    def return_book(self):
        if not self.is_available:
            self.is_available = True
            return f"You have returned '{self.title}' by {self.author}."
        else:
            raise ValueError(f"'{self.title}' was not borrowed.")

    def __str__(self):
        return f"'{self.title}' by {self.author} (ISBN: {self.ISBN}, Year: {self.year}) - {'Available' if self.is_available else 'Not Available'}"


class Ebook(Book):
    def __init(self, title, author, ISBN, year, file_format, file_size):
        super().__init__(title, author, ISBN, year)
        self.file_format = file_format
        self.file_size = file_size

    def __str__(self):
        return f"'{self.title}' by {self.author} (ISBN: {self.ISBN}, Year: {self.year}, Format: {self.file_format}, Size: {self.file_size}MB) - {'Available' if self.is_available else 'Not Available'}"


class Audiobook(Book):
    def __init__(self, title, author, ISBN, year, duration):
        super().__init__(title, author, ISBN, year)
        self.duration = duration

    def __str__(self):
        return f"'{self.title}' by {self.author} (ISBN: {self.ISBN}, Year: {self.year}, Duration: {self.duration} hours) - {'Available' if self.is_available else 'Not Available'}"


class Comics(Book):
    def __init__(self, title, author, ISBN, year, issue_number):
        super().__init__(title, author, ISBN, year)
        self.issue_number = issue_number

    def __str__(self):
        return f"'{self.title}' by {self.author} (ISBN: {self.ISBN}, Year: {self.year}, Issue: {self.issue_number}) - {'Available' if self.is_available else 'Not Available'}"
