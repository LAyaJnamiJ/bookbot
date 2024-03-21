import os 
import string
import json
from fuzzywuzzy import process

def main():
    user_input = input("Which book dost thou seek?\n")
    book_name = normalize_input(user_input)
    book_list = get_available_books()
    book_list_copy = book_list.copy()
    metadata = get_book_metadata()

    variation_to_title_map = {}  # Our magical mapping!

    for book in metadata:
        original_title = book["title"].lower()
        variations = [v.lower() for v in book.get("title_variations", [])]
        for variation in variations:
            variation_to_title_map[variation] = original_title 
        book_list.extend(variations)

    book_list_return(book_list_copy)

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

def book_list_return(book_list_copy):
    ask = input("Do you need the entire book list? (y/n)\n").lower().strip()
    if ask == "y":
        for title in book_list_copy:
            print(title)

def get_book_metadata():
    # fetches metadata from json file
    with open('metadata.json') as f:
        return json.load(f)

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