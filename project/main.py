import requests
from bs4 import BeautifulSoup
from requests import Response


def get_html(url: str) -> BeautifulSoup:
    """
    Get html from url
    """
    response: Response = requests.get(url)
    soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
    return soup


def get_url(year: int, month: int) -> str:
    """
    Get url from year and month
    """
    url: str = "https://go2senkyo.com/schedule/{year}?{month}".format(year=year, month=month)
    return url


def main():
    pass


if __name__ == "__main__":
    main()
