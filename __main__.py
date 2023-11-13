import json    
import tkinter
from tkinter import filedialog    
import pandas as pd

# Create a tkinter root object and hide it (for the file explorer)
root = tkinter.Tk()
root.withdraw()

def main():
    print("pick a html file : ")
    json_data = select_html_file()
    
    if (json_data):
       squad_data = calculate_fm_values(json_data)
    else:
        print(f"field data couldn't be read: ", {json_data})
        
    if (squad_data):
        json_to_html_table(squad_data)
    else:
        print(f"field data couldn't be read: ", {squad_data})
    
def select_html_file():
    while True:
        html_file = filedialog.askopenfilename(filetypes=[("HTML files", "*.html")], initialdir="./", title="Select a file")   
        
        if html_file.endswith(".html"):
            break # exit the loop when a valid file is chosen
        else:
            print("Please select an HTML file.")
            continue
        
    print(f"file picked : {html_file}")
    try:
        json_data = html_to_json(html_file)
        if json_data and isinstance(json_data, str) and not json_data.isspace():
            return json_data
        else:
            print(f"An error has occurred. File data is null or empty: {html_file}")
            select_html_file()
            
    except Exception as e:
        print(f"An error has occurred. File data is not a valid HTML: {html_file}")
        print(e)
        select_html_file()

def html_to_json(html_file):
    import requests 
    file_content = requests.get(html_file).text
    soup = BeautifulSoup(file_content, "html.parser")
    json_data = json.dumps(soup.prettify())
    if json_data and not json_data.isspace():
        return json_data
    else:
        print(f"an error has occured file data is null or empty: ", {json_data})

def calculate_fm_values(json_data):
    from pos_score_calc import calculate_scores 
    calculate_scores(json_data)

def json_to_html_table(squad_data):    
    import uuid
    filename = str(uuid.uuid4()) + ".html"
    filename
        
    html = generate_html(squad_data)
    open(filename, "w", encoding="utf-8").write(html)

def generate_html(dataframe: pd.DataFrame):
    table_html = dataframe.to_html(table_id="table", index=False)
    html = f"""
    <html>
    <header>
        <link href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css" rel="stylesheet">
    </header>
    <body>
    {table_html}
    <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js" integrity="sha256-u7e5khyithlIdTpu22PHhENmPcRdFiHRjhAuHcs05RI=" crossorigin="anonymous"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
    <script>
        $(document).ready( function () {{
            $('#table').DataTable({{
                paging: false,
                order: [[12, 'desc']],
                // scrollY: 400,
            }});
        }});
    </script>
    </body>
    </html>
    """
    # return the html
    return html


if __name__ == "__main__":
    main() 