import os
import random
import requests
import pandas as pd


BOOKS_FOLDER = "./raw_books"
BOOKS_FILE = "./raw_books/Self Help_3_Books.csv"


def get_countries():
    print("Fetching country data...")
    resp = requests.get("https://restcountries.com/v3.1/independent?status=true")
    resp.raise_for_status()
    return [c["name"]["common"] for c in resp.json()]


def assign_countries(df, countries):
    df["publisher_country"] = [random.choice(countries) for _ in range(len(df))]
    return df


def main():
    df = pd.read_csv(BOOKS_FILE)
    countries = get_countries()
    df = assign_countries(df, countries)
    # Define the path and filename for saving file
    df_name = "books_with_country"
    df_path_csv = os.path.join(BOOKS_FOLDER, f"{df_name}.csv")
    df_path_json = os.path.join(BOOKS_FOLDER, f"{df_name}.json")
    df.to_csv(df_path_csv, index=False, encoding="utf-8")
    df.to_json(df_path_json, orient="records", indent=4, force_ascii=False)
    print("Saving complete!")

if __name__ == "__main__":
    main()