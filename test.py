import requests

def test_edit_sysprompt():
    url = "http://localhost:5000/api/sysprompt/edit"
    response = requests.post(url)

    if response.status_code == 200:
        print("Success on edit! Response Data:")
        print(response.text)
    else:
        print("Failed to edit sysprompt. Status code:", response.status_code)

def test_reset_sysprompt():
    url = "http://localhost:5000/api/sysprompt/reset"
    response = requests.post(url)

    if response.status_code == 200:
        print("Success on reset! Response Data:")
        print(response.text)
    else:
        print("Failed to reset sysprompt. Status code:", response.status_code)

if __name__ == "__main__":
    #test_edit_sysprompt()
    test_reset_sysprompt()
