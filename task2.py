import urllib.parse
import urllib.request
from collections import defaultdict


def extract_path_tnp(line):
    start = line.find(HREF) + len(HREF)
    if start == -1 + len(HREF):  # if page is last
        return False
    end = start + line[start:].find('"')
    return line[start:end].replace("&amp;", "&")


LINK_KEYWORD = "Предыдущая страница"
DOMAIN = "https://ru.wikipedia.org"
FIRST_PAGE_PATH = "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83"
HREF = 'href="'


if __name__ == "__main__":
    counts = defaultdict(int)
    path_to_next_page = FIRST_PAGE_PATH

    while path_to_next_page:
        # Fetch page
        url = DOMAIN + path_to_next_page
        response = urllib.request.urlopen(url)
        page = response.read().decode("utf8")

        # Truncate whole page to animal list
        list_start = page.find(LINK_KEYWORD)
        list_end = page.find(LINK_KEYWORD, list_start + 1)
        animal_list = page[list_start:list_end]
 
        # Split by First letter (header)
        splited_list = animal_list.split("<h3>")
        for split in splited_list[1:]:
            letter = split[0]
            occurences = split.count("<li>")
            counts[letter] += occurences

        # Update path
        path_to_next_page = extract_path_tnp(splited_list[0])

    # Out
    for letter, count in counts.items():
        print(f"{letter}: {count}")
