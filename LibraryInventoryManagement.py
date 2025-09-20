import textwrap

def checkValidCount(entryMethod, selectedLibrary=None, title=None, author=None):
    ## Stays in the menu until they enter a valid amount of copies to donate
    validCopiesCount = False
    while validCopiesCount == False:
        userInputCopies = input(textwrap.dedent("""
                               Copies donating: 
                               """)).strip() if entryMethod == "donation" else input(textwrap.dedent("""
                               Copies stealing: 
                               """)).strip() if entryMethod == "stealing" else input(textwrap.dedent("""
                               Copies to move: 
                               """)).strip()
        if userInputCopies.isdigit() and int(userInputCopies) > 0:
            if entryMethod in ["theft", "movement"]:
                for book in selectedLibrary.books:
                    if book.title.lower() == title.lower() and book.author.lower() == author.lower() and int(userInputCopies) > book.copies:
                        copiesString = f"{book.copies} copies" if book.copies > 1 else f"{book.copies} copy"
                        if entryMethod == "theft":
                            print(f"\n{selectedLibrary.name} only has {copiesString} of {book.title}. You aren't physically able to steal that many. What kind of lousy criminal are you? Have mercy, scumbag.")
                        else:
                            print(f"\n{selectedLibrary.name} only has {copiesString} of {book.title}. It's not possible to move that many. Please choose a number between 1 and {book.copies}.")
                        return "tooManyCopies"
            validCopiesCount = True
            return userInputCopies
        else:
            print("Please enter a valid positive integer.")

def inputBookDetails():
    ## Allows the user to input a book title and author
    title = input(textwrap.dedent("""
                    Book's title: 
                    """))
    author = input(textwrap.dedent("""
                    Book's author: 
                    """))
    return title, author

def listAllLibraries(entryMethod):
    ## User chooses specific library
    validLibrary = False
    while validLibrary == False:
        counter = 1
        for library in libraryList:
            print(f"    {counter}. {library.name}")
            counter += 1
        if entryMethod == "inventory":
            print(f"    {counter}. All of them!")
            counter += 1
        print(f"    {counter}. Return to previous menu ↵")
        userInputLocation = input(textwrap.dedent("""
                       Please enter a number:
                       """)).strip()
        ## Makes sure they entered a valid number
        if userInputLocation.isdigit() and int(userInputLocation) <= len(libraryList) + 2:
            ## If they selected exit, quit
            if int(userInputLocation) == counter:
                return "Backout"
            ## If they selected all, acknowledge that
            elif entryMethod == "inventory" and int(userInputLocation) == counter - 1:
                return "All"
            validLibrary = True
            return int(userInputLocation) - 1

## Creates the Book class, used for adding new books
class Book:
    def __init__(self, title, author, copies):
        self.title = title
        self.author = author
        self.copies = copies

## Creates a library class, this allows for the storing of created books + other methods
class Library:
    def __init__(self, name):
        self.books = []
        self.name = name

    def addBook(self, newBook):
        if self.books:
            ## If the book already exists in the library, just add it to the total copies count
            for book in self.books:
                if book.title.lower() == newBook.title.lower() and book.author.lower() == newBook.author.lower():
                    book.copies += newBook.copies
                    return
            self.books.append(newBook)
        ## Handles when there are no books in the library
        else:
            self.books.append(newBook)

    def checkAvailability(self, title, author):
        possibilities = []
        for book in self.books:
            if book.title.lower() == title.lower() and book.author.lower() == author.lower():
                return book.copies
            ## If either name or author correct, but not both, add to a list of "possible alternatives"
            elif (book.title.lower() == title.lower()) ^ (book.author.lower() == author.lower()):
                possibilities.append((book.title, book.author))
        return possibilities

    def removeBook(self, title, author, copies):
        for book in self.books:
            if book.title.lower() == title.lower() and book.author.lower() == author.lower():
                book.copies -= int(copies)
                ## If they get rid of the last copy, remove the book entirely
                if book.copies == 0:
                    self.books.remove(book)
                    print(f"\nWell, congratulations. You've purloined every last copy of {title} that {self.name} had. I hope you're happy with yourself. Your parents certainly aren't.")
                else:
                    copiesString = f"{book.copies} copies" if book.copies > 1 else f"{book.copies} copy"
                    print(f"\nI can't believe you've stolen our {title} books from {self.name}... They only have {copiesString} left...")
                return book.copies

    def searchForTitle(self, title):
        ## lambda function to search for all books of a title. Not necessarily how I'd do it normally, but demonstrates lambda functions
        search_title = lambda bookTitle: [book.author for book in self.books if book.title.lower() == bookTitle.lower()]
        return search_title(title)

    def searchForAuthor(self, author):
        ## lambda function to search for all books by an author. Not necessarily how I'd do it normally, but demonstrates lambda functions
        search_title = lambda bookAuthor: [book.title for book in self.books if book.author.lower() == bookAuthor.lower()]
        return search_title(author)


## Sets up global variables and initializes some books / libraries so the user already has some to interact with
userQuit = False

## If you create book objects (Book1 = Book(title, author, copies)) instead of directly creating a new one every time, it breaks because you are referencing the same instances of objects
## So when I update the copies property, it updates the Book1 object's copies count, which affects every library, not just the current one.
## Also shows how it handles adding multiple copies of the same book
libraryList = []
library1 = Library("Belfast Bookstore")
libraryList.append(library1)
library1.addBook(Book("IT", "Stephen King", 3))
library1.addBook(Book("Assassin's Apprentice", "Robin Hobb", 1))
library1.addBook(Book("IT", "Stephen King", 2))

library2 = Library("Madagascar Magazines")
libraryList.append(library2)
library2.addBook(Book("IT", "Stephen King", 2))
library2.addBook(Book("Pet Sematary", "Stephen King", 2))
library2.addBook(Book("The Anarchist Cookbook", "William Powell", 1))
library2.addBook(Book("The Three Investigators - The Secret of the Haunted Mirror", "M. V. Carey", 4))
library2.addBook(Book("The Stranger", "Albert Camus", 1))
library2.addBook(Book("The Stranger", "Harlan Coben", 1))

library3 = Library("Newcastle Novels")
libraryList.append(library3)
library3.addBook(Book("IT", "Stephen King", 2))
library3.addBook(Book("IT", "Stephen King", 1))
library3.addBook(Book("IT", "Stephen King", 7))
library3.addBook(Book("Pet Sematary", "Stephen King", 5))
library3.addBook(Book("Doctor Sleep", "Stephen King", 1))
library3.addBook(Book("The Anarchist Cookbook", "William Powell", 1))
library3.addBook(Book("Dr. No", "Ian Fleming", 80))

library4 = Library("Manchurian Mangas")
libraryList.append(library4)

if __name__ == '__main__':
    ## Keeps them in the menu until they decide to quit
    while userQuit == False:
        userInputMain = input(textwrap.dedent("""
        Welcome to the Online Library Service! What would you like to do today?
            1. Check which library has a book in stock
            2. Check the inventory of a specific library
            3. Search for all books of a specific title
            4. Search for all books by a specific author
            5. Donate books to a library
            6. Steal books from a library
            7. Move a book from one library to another
            8. Quit
            
        Please enter your choice:
        """)).strip()
        match userInputMain:
            case "1":
                print("Which book would you like to check availability for?")
                ## User determines which book to search for
                userInputOneTitle, userInputOneAuthor = inputBookDetails()
                inStockAtAll = False
                possibilities = []
                for library in libraryList:
                    bookCount = library.checkAvailability(userInputOneTitle.lower(), userInputOneAuthor.lower())
                    if type(bookCount) == int:
                        print(f"{library.name} has {bookCount} copies in stock.")
                        inStockAtAll = True
                    ## If they only returned possible matches, add those to a list
                    elif type(bookCount) == list:
                        possibilities += bookCount
                if not inStockAtAll:
                    print(f"\nUnfortunately, none of our libraries have any copies of {userInputOneTitle} by {userInputOneAuthor} in stock.")
                    ## If any other possibilities were found, suggest them
                    if possibilities:
                        print("However, we did find other books you could have meant. Did you mean any of these?")
                        for suggestion in set(possibilities):
                            print(f"    >{suggestion}")

            case "2":
                print("\nWhich library would you like to check inventory for?")
                librariesChoice = listAllLibraries("inventory")
                if librariesChoice == "Backout":
                    continue
                elif librariesChoice == "All":
                    for library in libraryList:
                        print("")
                        print(f"{library.name}:")
                        if library.books:
                            for book in library.books:
                                print(f"Title: {book.title}, Author: {book.author}, Copies: {book.copies}")
                        else:
                            print("No books currently in stock.")
                else:
                    selectedLibrary = libraryList[librariesChoice]
                    print(f"\n{selectedLibrary.name}:")
                    for book in selectedLibrary.books:
                        print(f"Title: {book.title}, Author: {book.author}, Copies: {book.copies}")

            case "3":
                allAuthorsOfTitle = []
                userInputThreeTitle = input("\nSearch for all books of with this specific title:\n")
                for library in libraryList:
                    foundAuthors = library.searchForTitle(userInputThreeTitle)
                    allAuthorsOfTitle += foundAuthors
                allAuthorsOfTitle = set(allAuthorsOfTitle)
                if not allAuthorsOfTitle:
                    print(f"\nNo books found by the name of: {userInputThreeTitle}.")
                else:
                    print(f"\nAuthors who have penned books by the name of {userInputThreeTitle}:")
                    for author in allAuthorsOfTitle:
                        print(author)

            case "4":
                allBooksByAuthor = []
                userInputThreeTitle = input("\nSearch for all books by this specific author:\n")
                for library in libraryList:
                    foundTitles = library.searchForAuthor(userInputThreeTitle)
                    allBooksByAuthor += foundTitles
                allBooksByAuthor = set(allBooksByAuthor)
                if not allBooksByAuthor:
                    print(f"\nUnable to find any books authored by: {userInputThreeTitle}.")
                else:
                    print(f"\nAll found books by {userInputThreeTitle}:")
                    for title in allBooksByAuthor:
                        print(title)

            case "5":
                ## Lists all libraries
                print("Which library would you like to donate to?")
                ## Lists all libraries
                librariesChoice = listAllLibraries("donation")
                if librariesChoice == "Backout":
                    continue
                else:
                    selectedLibrary = libraryList[librariesChoice]
                ## User determines which book to search for
                userInputTwoTitle, userInputTwoAuthor = inputBookDetails()

                ## Stays in the menu until they enter a valid amount of copies to donate
                userInputTwoCopies = checkValidCount("donation")
                selectedLibrary.addBook(Book(userInputTwoTitle, userInputTwoAuthor, int(userInputTwoCopies)))
                print(f"\nThank you for your donation to {selectedLibrary.name}!")

            case "6":
                print("\nWait, you're stealing from us? From which library?")
                ## Lists all libraries
                librariesChoice = listAllLibraries("theft")
                if librariesChoice == "Backout":
                    continue
                else:
                    selectedLibrary = libraryList[librariesChoice]
                ## User determines which book to steal
                userInputThreeTitle, userInputThreeAuthor = inputBookDetails()

                ## Stays in the menu until they enter a valid amount of copies to steal
                userInputThreeCopies = checkValidCount("theft", selectedLibrary, userInputThreeTitle, userInputThreeAuthor)
                if userInputThreeCopies == "tooManyCopies":
                    continue
                else:
                    selectedLibrary.removeBook(userInputThreeTitle, userInputThreeAuthor, userInputThreeCopies)

            case "7":
                ## Checks which libraries the user wants to move books between
                transferChosen = False
                transferFromChosen = False
                transferToChosen = False
                while transferChosen == False:
                    ## Lists all libraries
                    if transferFromChosen == False:
                        print("\nWhich store would you live to move books from?")
                        librariesChoice = listAllLibraries("movement")
                        if librariesChoice == "Backout":
                            break
                        else:
                            selectedLibraryFrom = libraryList[librariesChoice]
                            transferFromChosen = True
                        if not selectedLibraryFrom.books:
                            print(f"\n{selectedLibraryFrom.name} has no books to transfer!")
                            transferFromChosen = False
                            continue

                    ## Lists all libraries
                    if transferToChosen == False:
                        print("\nWhich store would you live to move the books to?")
                        librariesChoice = listAllLibraries("movement")
                        if librariesChoice == "Backout":
                            transferFromChosen = False
                            continue
                        elif libraryList[librariesChoice].name == selectedLibraryFrom.name:
                            print("\nYou have to choose two different libraries to be able to move books.")
                            continue
                        else:
                            selectedLibraryTo = libraryList[librariesChoice]
                            transferToChosen = True
                            transferChosen = True

                    ## Lets them choose a book based on the library they selected to move from
                    bookChosen = False
                    while bookChosen == False:
                        print("\nWhich book would you like to move?")
                        counter = 1
                        for book in selectedLibraryFrom.books:
                            print(f"    {counter}. {book.title} by {book.author}")
                            counter += 1
                        print(f"    {counter}. Return to previous menu ↵")
                        userInputBookChoice = input(textwrap.dedent("""
                                              Please enter a number:
                                              """)).strip()
                        ## Makes sure they entered a valid number
                        if userInputBookChoice.isdigit() and int(userInputBookChoice) <= len(selectedLibraryFrom.books) + 1:
                            ## If they selected back out, go up one layer
                            if int(userInputBookChoice) == counter:
                                transferToChosen = False
                                transferChosen = False
                                break
                            bookChosen = True
                            selectedBook = selectedLibraryFrom.books[int(userInputBookChoice)-1]
                            copiesChosen = False
                            while copiesChosen == False:
                                print(f"\nHow many copies of {selectedBook.title} would you like to move from {selectedLibraryFrom.name} to {selectedLibraryTo.name}?")
                                userInputSevenCopies = checkValidCount("movement", selectedLibraryFrom, selectedBook.title, selectedBook.author)
                                if userInputSevenCopies == "tooManyCopies":
                                    continue
                                copiesChosen = True
                            selectedLibraryFrom.removeBook(selectedBook.title, selectedBook.author, int(userInputSevenCopies))
                            selectedLibraryTo.addBook(Book(selectedBook.title, selectedBook.author, int(userInputSevenCopies)))
                            print(f"\nSuccessfully moved {userInputSevenCopies} copies of {selectedBook.title} from {selectedLibraryFrom.name} to {selectedLibraryTo.name}.")
                        else:
                            print("\nPlease enter a valid number.")

            case "8":
                print("\nThank you for choosing to use the Online Library Service!")
                userQuit = True

            case _:
                print("Invalid choice. Please only enter a number from 1-8.\n")

