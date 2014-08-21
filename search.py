# -*- encoding: utf-8 -*-
import os
import requests
from BeautifulSoup import BeautifulSoup
#from apscheduler.schedulers.background import BackgroundScheduler

TARGET_CLASS_NAME = 'cnt cf'

def notify(cmd):
    """
    macの通知機能を利用して通知
    """

    os.system(cmd)

class RealTimeSearch(object):
    """
    Yahooリアルタイム検索の結果を取得する
    """

    def __init__(self, keyword, is_debug=False):
        self._keyword = keyword
        self._host = 'http://realtime.search.yahoo.co.jp/search'
        self._params = {
            'p': self._keyword,
            'fr': 'top_ga1_sa',
            'ei': 'utf-8'
        }
        
        #最新の情報を格納する
        self._new_data = ""
        
        #アップデートが発生したか
        self.is_update = False

        #デバッグ用Flag
        self._is_debug = is_debug

    def _search_data(self):
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
                return 

            self._soup = BeautifulSoup(r.content)
            divs = self._soup.html.body.findAll('div')
            #最新１件だけを取得
            results = self._get_search_results(divs)
            return results

    def get_recent_result(self):
        results = self._search_data()
        #検索結果が空
        if not results:
            return

        is_set = False 

        try:
            result_time = results[0]._getAttrMap()['data-time']
        except KeyError:
            return
        else:
            if self._new_data and int(result_time) > int(self._new_data._getAttrMap()['data-time']):
                is_set = True
            elif not self._new_data and result_time:
                is_set = True

            if is_set or self._is_debug:
                self._set_new_data(results[0])
                notify_command = self._make_notify_command()
                notify(notify_command)
            
    def _make_notify_command(self):
        """
        通知用のコマンドを作成
        """
        
        message = self._new_data.find('h2').text
        message = message.replace('"', '\\"')
        open_url = "http://realtime.search.yahoo.co.jp/search?p=%s&ei=UTF-8" % self._keyword
        notify_command = u"terminal-notifier -title 検索ワード%s -message \"%s\" -group tokyo -open %s" % (self._keyword, message, open_url)
        notify_command = notify_command.encode('utf-8')
        return notify_command


    def _set_new_data(self, result):
        """
        _new_dataに最新の検索結果をセット
        """

        self._new_data = result

    def _get_search_results(self, divs, is_new=True):
        """
        検索結果を取得する
        """
        
        results = []
        for div in divs:
            for attr in div.attrs: 
                if TARGET_CLASS_NAME in attr:
                    results.append(div)
                    break
                
                if results and is_new:
                   return results 

        return results


if __name__ == "__main__":
    #scheduler = BackgroundScheduler()
    #scheduler.add_job(job_test, 'trigger', seconds=3)
    #scheduler.start()
    rs = RealTimeSearch(u'ランサーズ', True)
    rs.get_recent_result()
