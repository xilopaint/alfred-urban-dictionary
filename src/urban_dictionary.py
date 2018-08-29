#!/usr/bin/env python
# encoding: utf-8
#
# Copyright © 2018 Arthur Pinheiro
#
# MIT Licence. See http://opensource.org/licenses/MIT

import sys
from urllib import urlencode

from workflow import Workflow3, web

UPDATE_SETTINGS = {'github_slug': 'xilopaint/alfred-urban-dictionary'}


def update_workflow():
    """Update and install workflow if a newer version is available."""
    if wf.update_available:
        wf.add_item(title='A newer version of Urban Dictionary is available.',
                    subtitle='Action this item to install the update.',
                    autocomplete='workflow:update',
                    icon='update.png')


def get_data(query, url):
    """Return JSON object."""
    r = web.get(url)
    r.raise_for_status()
    return r.json()


def show_results(query, data, url):
    """List results."""
    for result in data['list']:
        word = result['word']
        thumbs_up_cnt = result['thumbs_up']
        thumbs_down_cnt = result['thumbs_down']
        thumbs_up_sign = u'\U0001F44D'
        thumbs_down_sign = u'\U0001F44E'
        title = u"{} • {} {} | {} {}".format(word,
                                             thumbs_up_sign,
                                             thumbs_up_cnt,
                                             thumbs_down_sign,
                                             thumbs_down_cnt)
        wf.add_item(valid=True,
                    title=title,
                    subtitle=result['definition'],
                    arg=result['permalink'])

    return wf.send_feedback()


def main(wf):
    """Run workflow."""
    update_workflow()
    query = wf.args[0]

    url = 'http://api.urbandictionary.com/v0/define?' + \
        urlencode({'term': query.encode('utf-8')})

    data = get_data(query, url)
    show_results(query, data, url)


if __name__ == '__main__':
    wf = Workflow3(update_settings=UPDATE_SETTINGS)
    sys.exit(wf.run(main))
