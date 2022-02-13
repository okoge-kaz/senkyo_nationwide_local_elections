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


def get_election_data_from_url(url: str) -> dict:
    """
    Get election data from url
    """
    soup: BeautifulSoup = get_html(url)
    election_data: dict = {}

    # 選挙概観
    election_data_header_div_tag = soup.find("div", class_="p_local_senkyo_ttl_wrapp white column_ttl_wrapp")
    if election_data_header_div_tag is not None:
        election_data_header_p_tag = election_data_header_div_tag.find("p")
        if election_data_header_p_tag is not None:
            election_data["prefecture"] = election_data_header_p_tag.text.strip(" ")
        election_data_header_h1_tag = election_data_header_div_tag.find("h1")
        if election_data_header_h1_tag is not None:
            election_data["election_name"] = election_data_header_h1_tag.text.strip(" ")
            election_data_header_h1_tag_span_tag = election_data_header_h1_tag.find("span")
            if election_data_header_h1_tag_span_tag is not None:
                election_data["election_date"] = election_data_header_h1_tag_span_tag.text.strip(" ")

    # 選挙結果
    election_result_table_tag = soup.find("table", class_="m_senkyo_data")
    if election_result_table_tag is not None:
        election_result_table_tbody_tag = election_result_table_tag.find("tbody")
        if election_result_table_tbody_tag is not None:
            election_result_table_tr_tag_list = election_result_table_tbody_tag.find_all("tr")
            if election_result_table_tr_tag_list is not None:

                # 1行目
                election_result_table_tr_tag = election_result_table_tr_tag_list[0]
                election_result_table_tr_tag_th_tag_list = election_result_table_tr_tag.find_all("th")
                election_result_table_tr_tag_td_tag_list = election_result_table_tr_tag.find_all("td")

                # 投票日
                election_data["vote_date"] = election_result_table_tr_tag_td_tag_list[0].text.strip(" ")
                # 投票率
                election_data["vote_rate"] = election_result_table_tr_tag_td_tag_list[1].text.strip(" ")
                # 定数/ 候補者数
                election_data["constituency_candidate_number"] = election_result_table_tr_tag_td_tag_list[
                    2
                ].text.strip(" ")

                # 2行目
                election_result_table_tr_tag = election_result_table_tr_tag_list[1]
                election_result_table_tr_tag_th_tag_list = election_result_table_tr_tag.find_all("th")
                election_result_table_tr_tag_td_tag_list = election_result_table_tr_tag.find_all("td")

                # 告示日
                election_data["announce_date"] = election_result_table_tr_tag_td_tag_list[0].text.strip(" ").strip(" ")
                # 前回投票率
                election_data["last_vote_rate"] = election_result_table_tr_tag_td_tag_list[1].text.strip(" ")

                # 3行目
                election_result_table_tr_tag = election_result_table_tr_tag_list[2]
                election_result_table_tr_tag_th_tag_list = election_result_table_tr_tag.find_all("th")
                election_result_table_tr_tag_td_tag_list = election_result_table_tr_tag.find_all("td")

                # 事由・ポイント
                election_data["reason_point"] = election_result_table_tr_tag_td_tag_list[0].text.strip(" ")

    # 選挙結果（当選者）
    election_result_winner_table_tag = soup.find("table", class_="m_senkyo_result_table")
    # print(election_result_winner_table_tag)
    if election_result_winner_table_tag is not None:
        election_result_winner_table_tag_tbody_tag = election_result_winner_table_tag
        if election_result_winner_table_tag_tbody_tag is not None:
            election_result_winner_table_tag_tr_tag_list = election_result_winner_table_tag_tbody_tag.find_all("tr")
            if election_result_winner_table_tag_tr_tag_list is not None:
                for index, election_result_winner_table_tag_tr_tag in enumerate(
                    election_result_winner_table_tag_tr_tag_list
                ):
                    if index == 0:
                        election_result_winner_table_tag_tr_tag_td_tag_list = (
                            election_result_winner_table_tag_tr_tag.find_all("td")
                        )
                        if election_result_winner_table_tag_tr_tag_td_tag_list is not None:
                            # 当選/落選
                            election_result_winner_table_tag_tr_tag_td_tag_img = (
                                election_result_winner_table_tag_tr_tag_td_tag_list[0].find("img")
                            )
                            # 人物データ
                            election_result_winner_table_tag_tr_tag_td_tag_section_tag = (
                                election_result_winner_table_tag_tr_tag_td_tag_list[1].find("section")
                            )
                            if election_result_winner_table_tag_tr_tag_td_tag_section_tag is not None:
                                election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_list = (
                                    election_result_winner_table_tag_tr_tag_td_tag_section_tag.find_all("div")
                                )
                                if election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_list is not None:
                                    # 当選者氏名
                                    election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_h2_tag = (
                                        election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_list[
                                            1
                                        ].find("h2")
                                    )
                                    if (
                                        election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_h2_tag
                                        is not None
                                    ):
                                        # 漢字氏名
                                        election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_h2_tag_a_tag = election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_h2_tag.find(
                                            "a"
                                        )
                                        election_data[
                                            "winner_name"
                                        ] = election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_h2_tag_a_tag.get_text().strip(
                                            " "
                                        )
                                        # url
                                        election_data[
                                            "url"
                                        ] = election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_h2_tag_a_tag.get(
                                            "href"
                                        )
                                        # カナ氏名
                                        election_data[
                                            "winner_name_kana"
                                        ] = election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_h2_tag.find(
                                            "span"
                                        ).text.strip(
                                            " "
                                        )
                                    # 詳細情報
                                    election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_div_tag = (
                                        election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_list[
                                            1
                                        ].find("div")
                                    )
                                    if (
                                        election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_div_tag
                                        is not None
                                    ):
                                        election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_div_tag_div_tag_list = election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_div_tag.find_all(
                                            "div"
                                        )
                                        # 個人情報
                                        election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_div_tag_div_tag = election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_div_tag_div_tag_list[
                                            1
                                        ]
                                        if (
                                            election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_div_tag_div_tag
                                            is not None
                                        ):
                                            election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_div_tag_div_tag_p_tag_list = election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_div_tag_div_tag.find_all(
                                                "p"
                                            )

                                            election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_div_tag_div_tag_p_tag_span_tag_list = election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_div_tag_div_tag_p_tag_list[
                                                0
                                            ].find_all(
                                                "span"
                                            )
                                            # 年齢-性別
                                            election_data[
                                                "winner_age_sex"
                                            ] = election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_div_tag_div_tag_p_tag_span_tag_list[
                                                0
                                            ].text.strip(
                                                " "
                                            )
                                            # 現職
                                            election_data[
                                                "winner_info"
                                            ] = election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_div_tag_div_tag_p_tag_span_tag_list[
                                                1
                                            ].text.strip(
                                                " "
                                            )
                                            # 職業
                                            election_data[
                                                "winner_job"
                                            ] = election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_div_tag_div_tag_p_tag_list[
                                                1
                                            ].text.strip(
                                                " "
                                            )
                                        # 所属
                                        election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_div_tag_div_tag = election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_div_tag_div_tag_list[
                                            0
                                        ]
                                        election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_div_tag_div_tag_p_tag = election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_div_tag.find(
                                            "p"
                                        )
                                        election_data[
                                            "affiliation"
                                        ] = election_result_winner_table_tag_tr_tag_td_tag_section_tag_div_tag_div_tag_div_tag_p_tag.text.strip(
                                            " "
                                        )
                            # 票数
                            election_data["winner_votes"] = election_result_winner_table_tag_tr_tag_td_tag_list[
                                2
                            ].text.strip(" ")
                    else:
                        pass
    return election_data


def main():
    """
    Main function
    """
    year: int = 2019
    url: str = get_url(year)
    soup: BeautifulSoup = get_html(url)
    urls_data_by_month: dict = get_urls_from_soup(soup)

    for month in range(1, 13):
        urls_data: list = urls_data_by_month[month]
        election_data_array: list = []
        for url_data in urls_data:
            url = url_data["election_url"]
            election_data: dict = get_election_data_from_url(url)
            election_data_array.append(election_data)
        df = pd.DataFrame(election_data_array)
        df.to_csv(f"../out/{month}/{year}_{month}.csv", index=False, encoding="utf-8")




if __name__ == "__main__":
    main()
