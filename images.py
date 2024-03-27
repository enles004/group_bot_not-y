import chromedriver_autoinstaller
from pinterest.pinterest import Pinterest


def download_image(directory = "gaixinh"):
    email = "phuoccle537@gmail.com"
    password = "4648351155az#Phuoc"
    directory = directory
    link = "https://www.pinterest.com/search/pins/?q=g%C3%A1i%20c%E1%BB%B1c%20ph%E1%BA%A9m&rs=typed"
    pages = 1000

    # Check chromedriver exists
    chromedriver_autoinstaller.install()

    print("Open selenium...")
    p = Pinterest(email, password)

    print("Download Image")
    p.single_download(pages, link, directory)


if __name__ == "__main__":
    download_image()