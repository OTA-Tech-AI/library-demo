import requests

def get_csv_data():
    url = "http://localhost:5000/api/csv"
    response = requests.get(url)

    if response.status_code == 200:
        print("Success! Response Data:")
        print(response.text)
    else:
        print("Failed to retrieve data. Status code:", response.status_code)

if __name__ == "__main__":
    get_csv_data()
