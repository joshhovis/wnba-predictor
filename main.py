from predictor.logger import init_db

def main():
    print("Initializing database...")
    init_db()
    print("Done.")

if __name__ == "__main__":
    main()