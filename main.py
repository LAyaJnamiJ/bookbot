import os 
import string
import json
from fuzzywuzzy import process

class Book:
    def __init__(self, title, author, publisher, publishing_date, title_variations):
        self.title = title
        self.author = author
        self.publisher = publisher
        self.publishing_date = publishing_date
        self.title_variations = title_variations

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "publisher": self.publisher,
            "publishing_date": self.publishing_date,
            "title_variations": self.title_variations
        }

def main():
    book_list = get_available_books()
    book_list_copy = book_list.copy()
    metadata = json_calling(book_entry())

    variation_to_title_map = {}  # Our magical mapping!

    for book in metadata:
        original_title = book.title.lower()
        variations = [v.lower() for v in book.title_variations]
        for variation in variations:
            variation_to_title_map[variation] = original_title 
        book_list.extend(variations)

    book_list_return(book_list_copy)

    user_input = input("Which book dost thou seek?\n")
    book_name = normalize_input(user_input)

    # first check with original normalized input
    best_match, score = find_best_match(book_name, book_list)
    
    # second check with spaces removed, only if necessary
    book_name_split = book_name.split()
    if len(book_name_split) > 1:
        book_name_joined = ''.join(book_name_split)
        best_match_no_spaces, score_no_spaces = find_best_match(book_name_joined, book_list)
    else:
        best_match_no_spaces = None
        score_no_spaces = float('-inf')
   
    # Decide which result to use
    if score_no_spaces > score:
        final_match = best_match_no_spaces
        final_score = score_no_spaces
    else:
        final_match = best_match
        final_score = score

    final_title = variation_to_title_map.get(final_match.lower(), final_match)

    title_matching(final_title, final_score) # Proceed with the best match
    
def title_matching(best_match, score):
    # matches raw input to the best match gotten from find_best_match with a score > 80
    if score > 80:
        match = input(f"Is {best_match} the book you're looking for? (y/n)\n").lower().strip()
        if match == "y":
            try:
                path = f"books/{best_match}.txt"
                book_open(path)
            except FileNotFoundError as e:
                print("Such book does not exist or the title has been misspelt.")
        elif match == "n":
            print("Understood. You may try searching again with a different title.")
    else:
        print("Please search again with a different title.")

def book_entry():
    ask = input("Do you want to enter a new book into the library? (y/n)\n").lower().strip()
    if ask =="y":
        title = input("Please enter the book title. ").strip()
        author_input = input("Please enter the author's name(s). Separate individual authors by commas. ")
        raw_author = author_input.split(',')
        author = [entry.strip() for entry in raw_author if entry.strip()]
        publisher = input("Please enter the publisher's name. ").strip()
        publishing_date = input("Please enter the publishing date. ").strip()
        title_variations_input = input("Are there any alternate titles for this book? Please enter them in order separated by commas. ")
        raw_title_variations = title_variations_input.split(',')
        title_variations = [entry.strip() for entry in raw_title_variations if entry.strip()]
        
        new_book = [Book(title, author, publisher, publishing_date, title_variations)]

    elif ask == "n":
        new_book = []

    return new_book        

def json_calling(new_books):
    filename = "metadata.json"
    # Attempt to open and read existing data
    try:
        with open(filename, "r") as f:
            existing_books = json.load(f)
    except FileNotFoundError:
        existing_books = []
    # Combine the existing books with the new ones
    combined_books = existing_books + [book.to_dict() for book in new_books]
    
    # Now, inscribe the combined tales into the scroll
    with open(filename, "w") as f:
        json.dump(combined_books, f, indent=4)
    
    # Transforming the JSON back into Book instances
    loaded_books = [Book(**data) for data in combined_books]
    return loaded_books

def book_list_return(book_list_copy):
    # asks if the user needs the entire book list
    ask = input("Do you need the entire book list? (y/n)\n").lower().strip()
    if ask == "y":
        for title in book_list_copy:
            print(title)

def normalize_input(input_str):
    # Remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    normalized_str = input_str.translate(translator)

    # Convert to lowercase and strip whitespace
    normalized_str = normalized_str.lower().strip()

    return normalized_str

def book_open(path):
    # opens the file and prints the contents
    with open(path) as f:
            file_contents = f.read()
            print(file_contents)

def get_available_books(directory="books"):
    # gets all the book titles by replacing their .txt extension with an empty string
    return [file.replace(".txt", "") for file in os.listdir(directory) if file.endswith(".txt")]

def find_best_match(book_name, book_list):
    # uses a method from fuzzywuzzy's process to compute the edit distance and returns the match with highest score
    best_match = process.extractOne(book_name, book_list)
    return best_match

main()