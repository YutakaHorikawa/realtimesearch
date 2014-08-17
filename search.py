# -*- encoding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup

TARGET_CLASS_NAME = 'cnt cf'

class RealTimeSearch(object):
    """
    Yahooリアルタイム検索の結果を取得する
    """

    def __init__(self, keyword):
        self._keyword = keyword
        self._host = 'http://realtime.search.yahoo.co.jp/search'
        self._params = {
            'p': self._keyword,
            'fr': 'top_ga1_sa',
            'ei': 'utf-8'
        }
        
        #最新の情報を格納する
        self._new_data = ""

    def search_data(self):
        """
        リアルタイム検索を行う
        """

        try:
            r = requests.get(self._host, params=self._params)
        except:
            pass
        else:
            status_code = r.status_code
            if status_code != 200:
                Exception

            self._soup = BeautifulSoup(r.content)
            divs = self._soup.html.body.findAll('div')
            results = self._get_search_results(divs)

    def _get_search_results(self, divs):
        """
        検索結果を取得する
        """
        
        results = []
        for div in divs:
            for attr in div.attrs: 
                if TARGET_CLASS_NAME in attr:
                    results.append(div)
                    break

        return results


if __name__ == "__main__":
    rs = RealTimeSearch(u'ランサーズ')
    rs.search_data()
