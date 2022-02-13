import pandas as pd
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


def get_url(year: int, month: int = 1) -> str:
    """
    Get url from year and month
    """
    url: str = "https://go2senkyo.com/schedule/{year}?{month}".format(year=year, month=month)
    return url


def get_td_tags_from_tr_tag(tr_tag: BeautifulSoup) -> tuple:
    """
    Get td tags from tr tag
    """

    date_td_tag = tr_tag.find("td", class_="circle")
    if date_td_tag is None:
        return None, None, None
    date_div_tag = date_td_tag.find("div")
    if date_div_tag is None:
        return None, None, None

    date: str = date_div_tag.text

    election_name_td_tag = tr_tag.find("td", class_="left")
    if election_name_td_tag is None:
        return None, None, None
    election_name_a_tag = election_name_td_tag.find("a")
    if election_name_a_tag is None:
        return None, None, None

    election_url: str = election_name_a_tag["href"]
    election_name: str = election_name_a_tag.get_text()

    return date, election_name, election_url


def get_urls_from_soup(soup: BeautifulSoup) -> dict:
    """
    Get urls from soup
    """
    urls_by_month: dict = {}
    _month: int = 1
    for table in soup.find_all("table", class_="m_schedule_tab_table m_table"):
        # 1月から12月までのtableを取得
        tbody = table.find("tbody", class_="ttl_long")
        election_data_array: list = []
        if tbody is not None:
            for tr in tbody.find_all("tr"):
                date, election_name, election_url = get_td_tags_from_tr_tag(tr)
                if date is not None and election_name is not None and election_url is not None:
                    election_data_array.append(
                        {"date": date, "election_name": election_name, "election_url": election_url}
                    )
        urls_by_month[_month] = election_data_array
        _month += 1
    return urls_by_month


def main():
    """
    Main function
    """
    year: int = 2019
    url: str = get_url(year)
    soup: BeautifulSoup = get_html(url)
    urls_by_month: dict = get_urls_from_soup(soup)
    for month in range(1, 13):
        df: pd.DataFrame = pd.DataFrame(urls_by_month[month])
        df.to_csv("../out/senkyo_urls_" + str(month) + ".csv", index=False, encoding="utf-8")


if __name__ == "__main__":
    main()
