from random import choice
from time import time

import requests
from pyquery import PyQuery as pq


class BookSpider:
    def __init__(self):
        self.USER_AGENTS = (
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
            "Opera/8.0 (Windows NT 5.1; U; en)",
            "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
            "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
        )

    def get_book_info(self, isbn):
        try:
            if not self._is_legal_isbn(isbn):
                return {}
            url = self._gen_url(isbn)
            html = self._get_html(url)
            book_info = self._parse_html(html)
            return book_info
        except Exception:
            return {}

    def _is_legal_isbn(self, isbn):
        if len(isbn) > 13:
            return False
        if not isbn.isdigit():
            return False
        return True

    def _get_html(self, url):
        return requests.get(url, headers={"USER-AGENT": self._get_random_user_agent()}).text

    def _get_random_user_agent(self):
        return choice(self.USER_AGENTS)

    def _gen_url(self, isbn):
        return f"https://book.douban.com/isbn/{isbn}"

    def _parse_html(self, html):
        res = {}
        doc = pq(html)
        title = doc("h1 span").text()
        image_urls = doc(".nbg").attr("href")

        res["书名"] = title
        res["image_urls"] = image_urls

        synopsises_div = doc("#link-report .all .intro p")
        if synopsises_div is None or len(synopsises_div) == 0:
            synopsises_div = doc("#link-report .intro p")
        if len(synopsises_div) != 0:
            synopsises = "\n".join(map(lambda x: x.text, synopsises_div))
            res["简介"] = synopsises

        author_info_div = doc("div:not(#link-report)[class='indent '] .all .intro p")
        if author_info_div is None or len(author_info_div) == 0:
            author_info_div = doc("div:not(#link-report)[class='indent '] div .intro p")
        if len(author_info_div) != 0:
            author_info = "\n".join(map(lambda x: x.text or "", author_info_div))
            res["作者简介"] = author_info

        ending = "\n· · · · · · (收起)"
        catalog_div = doc("div[id^='dir_'][id$='_full']")
        if len(catalog_div) != 0:
            catalog = catalog_div.text()
            if catalog.endswith(ending):
                catalog = catalog[:-len(ending)]
            res["目录"] = catalog

        info = doc("#info").text()
        for unit in info.split("\n"):
            key, value = unit.split(":", 1)
            res[key.strip()] = value.strip()

        res["_tm"] = int(time() * 1000)

        for name in ["ISBN", "统一书号", "ISSN"]:
            if name in res.keys():
                res["_id"] = res[name]
                res.pop(name)
                break
        return res


if __name__ == "__main__":
    from pprint import pprint
    s = BookSpider()

    while True:
        choose = input("Please input ISBN: ")
        if choose == "quit":
            break
        start_time = time()
        result = s.get_book_info(choose)
        end_time = time()
        pprint(result)
        print(f"Used Time: {end_time - start_time}")
