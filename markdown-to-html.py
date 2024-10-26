import sys

if len(sys.argv) != 3:
    print("Usage: ./markdown_to_html.py markdown_to_change.md output.html")
    sys.exit(1)

input_filename = sys.argv[1]
output_filename = sys.argv[2]

with open(input_filename, 'r') as input_file:
    text = input_file.read()

markdown = {
    "#": ["<h1>", "</h1>"],
    "##": ["<h2>", "</h2>"],
    "###": ["<h3>", "</h3>"],
    "####": ["<h4>", "</h4>"],
    "#####": ["<h5>", "</h5>"],
    "######": ["<h6>", "</h6>"]
}

markdown_list = ["#","##","###","####","#####","######"]
words = []
lines = text.split("\n")

for i in range(len(lines)):
    list_item = lines[i].split(" ")
    words.append(list_item)

def heading_markdown(words: list,index: int, list_number:int):
    for key in markdown:
        if words[list_number][index] == key:
            words[list_number][index] = markdown[key][0]
            words[list_number].append(markdown[key][1])


def bold_italic_quote_markdown(lists: list, index: int):
    element = lists[index]
    to_replace = {"***":("strong","em"), "**": "strong", "*": "em"}
    
    if element.startswith((",", ".", "`", ":", ";")):
        element = element[1:]
    if element.endswith((".", ":", ";", "`")):
        element = element[:-1]

    for marker, tag in to_replace.items():
        if element.startswith(marker) and element.endswith(marker):
            stripped_text = element[len(marker):-len(marker)]
            lists[index] = f"<{tag}>{stripped_text}</{tag}>"
            return
        elif element.startswith(marker):
            stripped_text = element[len(marker):]
            lists[index] = f"<{tag}>{stripped_text}"
            return
        elif element.endswith(marker):
            stripped_text = element[:-len(marker)]
            lists[index] = f"{stripped_text}</{tag}>"
            return

started = False    
started_2 = False
def code_quote_markdown(lists: list, index: int, list_number: int):
    global started
    global started_2
    element = lists[index]
    to_replace = {"```": "code", "~~~": "blockquote"}
    for marker, tag in to_replace.items():
        if marker == "~~~":
            # Special case for blockquote (wrap whole element)
            if element.startswith(marker) and element.endswith(marker) and started_2 is not True:
                stripped_text = element[len(marker):-len(marker)]
                lists[index] = f"<blockquote>{stripped_text}</blockquote>"
                started_2 = False
                return
            if element.startswith(marker) and started_2 is not True or element == marker and started_2 is not True:
                lists[index] = f"<{tag}>"
                started_2 = True
                return
            elif element == marker and started_2 is True:
                lists[index] = f"</blockquote>"
                started_2 = False
                return
        else:
            if  element.startswith(marker) and started is not True:
                stripped_text = element[len(marker):]
                lists[index] = f"<pre><{tag}>{stripped_text}"
                started = True
            elif element.startswith(marker) and started is True:
                stripped_text = element[:-len(marker)]
                lists[index] = f"{stripped_text}</{tag}></pre>"
                started = False
        

def find_link(word :str, list_number ):
    if "](https://" in word:
        print("link present")
        return list_number
    return 9999

def get_link_text(word_list: list):
    new_word_list =[]
    for items in word_list:
        last_word = ""
        if "](https://" not in items:
            new_word_list.append(items) 
        else:
            for letters in items:
                if letters != "(":
                    last_word += letters
                else:
                    break
            new_word_list.append(last_word)
    return new_word_list


def extract_link(words_list: list, list_number: int) -> str:
    for items in words_list[list_number]:
        j = 0
        if "https://" in items:
            for letter in items:
                if letter == "/":
                    break
                j += 1
            link = items[j:-1]        
            return link
    return ""
    
def link_markdown(word_list: list, list_number: int, extracted_link: str, extracted_text: list,index: int):
    # Create the string for the HTML anchor tag
    for i, items in enumerate(extracted_text):
        # Remove starting "[" if present
        if items.startswith("["):
            extracted_text[i] = items[1:]
        # Remove ending "]" if present
        if items.endswith("]"):
            extracted_text[i] = extracted_text[i][:-1]
    text = " ".join(extracted_text)
    string = f'<a href="https:{extracted_link}">{text}</a>'
    parts = string.split(" ")
    word_list[list_number].clear()
    for i in range(len(parts)):
        word_list[list_number].append(parts[i])

list_with_link = 9999
found_link= False

for list_number, lists in enumerate(words):
    for index, element in enumerate(lists):
        heading_markdown(words, index, list_number)
        bold_italic_quote_markdown(lists, index)            
        list_with_link = find_link(lists[index], list_number)                        
        code_quote_markdown(lists, index, list_number)
        if list_with_link != 9999:
            extracted_text = get_link_text(words[list_with_link])
            extracted_link = extract_link(words, list_number)
            print(extracted_text, extracted_link)
            link_markdown(words, list_number, extracted_link, extracted_text, index)
                                      
def write_output_to_html(output_filename):
    with open(output_filename, 'w') as output_file:
        for lists in words:
            output_file.write(" ".join(lists) + "\n")
write_output_to_html(output_filename)

print(f"Markdown has been converted to HTML and written to {output_filename}.")
