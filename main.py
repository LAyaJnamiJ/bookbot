import os 
from fuzzywuzzy import process

def main():
    book_name = input("Which book dost thou seek?\n").lower().strip()
    available_books = get_available_books()
    best_match, score = find_best_match(book_name, available_books)
    
    if score > 80:
        match = input(f"Is {best_match} the book you're looking for? (y/n)\n").lower().strip()
        if match == "y":
            path = f"books/{best_match}.txt"
            try:
                book_open(path)
            except FileNotFoundError as e:
                try:
                    book_name_split = book_name.split()
                    book_name_joined = ''.join(book_name_split)
                    path = f"books/{book_name_joined}.txt"
                    book_open(path)
                except FileNotFoundError as e:
                    print("Such book does not exist or the title has been misspelt.")
        else:
            print("Please try again.")
    else:
        print("Such book does not exist or the title has been misspelt.")
        
def book_open(path):
    with open(path) as f:
            file_contents = f.read()
            print(file_contents)

def get_available_books(directory="books"):
    return [file.replace(".txt", "") for file in os.listdir(directory) if file.endswith(".txt")]

def find_best_match(book_name, available_books):
    best_match = process.extractOne(book_name, available_books)
    return best_match

main()