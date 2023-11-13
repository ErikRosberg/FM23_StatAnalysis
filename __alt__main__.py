import os
import json
import requests

def choose_html_file():
    # get a list of html files in the current directory
    html_files = [f for f in os.listdir() if f.endswith(".html")]
    # if there are no html files, return None
    if not html_files:
        return None
    # otherwise, choose a random html file
    file = random.choice(html_files)
    return file

def check_file_ok(file):
    # check if the file exists and is readable
    if not os.path.exists(file) or not os.access(file, os.R_OK):
        return False
    # check if the file is a valid html file
    # by looking for the <html> tag in the first line
    with open(file, "r") as f:
        first_line = f.readline()
        if "<html>" not in first_line:
            return False
    return True

def get_json_data(file):
    # convert the html file to json using requests
    # this is based on one of the web search results [^1^][2]
    html_content = requests.get(file)
    json_data = json.dumps(html_content.text)
    return json_data

def check_json_data_ok(json_data):
    # check if the json data is valid and has some content
    # by trying to parse it and get the length
    try:
        data = json.loads(json_data)
        if len(data) > 0:
            return True
    except:
        return False
    return False

def main():
    # choose a html file
    file = choose_html_file()
    # if there is no html file, print a message and exit
    if file is None:
        print("No html file found.")
        return
    # check if the file is ok
    file_ok = check_file_ok(file)
    # if the file is not ok, choose another file
    while not file_ok:
        print(f"{file} is not a valid html file. Choosing another file.")
        file = choose_html_file()
        file_ok = check_file_ok(file)
    # get the json data from the file
    json_data = get_json_data(file)
    # check if the json data is ok
    json_data_ok = check_json_data_ok(json_data)
    # if the json data is not ok, choose another file
    while not json_data_ok:
        print(f"{file} does not have valid json data. Choosing another file.")
        file = choose_html_file()
        file_ok = check_file_ok(file)
        json_data = get_json_data(file)
        json_data_ok = check_json_data_ok(json_data)
    # print the file name and the json data
    print(f"Chosen file: {file}")
    print(f"Json data: {json_data}")

if __name__ == "__main__":
    main()
