#!/usr/bin/env python3
#
# Copyright © 2018 Arthur Pinheiro
#
# MIT Licence. See http://opensource.org/licenses/MIT

import http.client
import json
import sys
import urllib.parse
from workflow import Workflow


def main(wf):
    """Run workflow."""
    query = wf.args[0]

    param = {'term': query}
    query_string = urllib.parse.urlencode(param)
    url = '/v0/define?' + query_string
    conn = http.client.HTTPSConnection('api.urbandictionary.com')
    conn.request('GET', url)
    res = conn.getresponse()
    data = json.loads(res.read())

    for result in data['list']:
        word = result['word']
        thumbs_up_cnt = result['thumbs_up']
        thumbs_down_cnt = result['thumbs_down']
        thumbs_up_sign = u'\U0001F44D'
        thumbs_down_sign = u'\U0001F44E'
        title = '{} • {} {} | {} {}'.format(
            word,
            thumbs_up_sign,
            thumbs_up_cnt,
            thumbs_down_sign,
            thumbs_down_cnt
        )
        wf.add_item(
            valid=True,
            title=title,
            subtitle=result['definition'],
            arg=result['permalink']
        )

    return wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
