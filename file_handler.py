
from colorama import init, Fore
init()

# ------------------------------------------------------------------------------------------------------

def clear_file():
    choice = input("Are you sure? type yes to confirm: ").lower()
    if choice == "yes":
        with open("ytlinks.txt", "w") as f:
            f.write("")
        return True
    else:
        return False
    
# ------------------------------------------------------------------------------------------------------

def save_links_to_text_file():
    print(f"\n\t\t{Fore.YELLOW}*****You can type (Q) to quit adding*****")
    getLink = ""
    while getLink not in ["Q", "q"]:
        getLink = input("Enter the Youtube video link: ").strip()
        if getLink not in ["q", "Q"]:
            with open("ytlinks.txt", "a+") as f:
                f.write(getLink + "\n")

# ------------------------------------------------------------------------------------------------------
    
def fetch_links_from_text_file():
    links = []
    with open("ytlinks.txt", "r+") as f:
        for line in f.readlines():
            links.append(line.rstrip())
    return links