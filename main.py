def main():
    book_name = input("Which book dost thou seek?\n").lower().strip()
    path = f"books/{book_name}.txt"
    try:
        book_open(path)
    except FileNotFoundError as e:
        try:
            book_name_split = book_name.split()
            book_name_joined = ''.join(book_name_split)
            path = f"books/{book_name_joined}.txt"
            book_open(path)
        except FileNotFoundError as e:
            print("such book does not exist")
        
def book_open(path):
    with open(path) as f:
            file_contents = f.read()
            print(file_contents)

main()