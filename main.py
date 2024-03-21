def main():
    book_name = input("Which book dost thou seek?\n").lower().strip()
    path = f"books/{book_name}.txt"
    try:
        with open(path) as f:
            file_contents = f.read()
            print(file_contents)
    except FileNotFoundError as e:
        print("such book does not exist")

main()