#!/usr/bin/env python3
#
# Copyright © 2018 Arthur Pinheiro
#
# MIT Licence. See http://opensource.org/licenses/MIT

""""Alfred workflow aimed to search Urban Dictionary."""

import re
import sys

from workflow import Workflow, web

HELP_URL = "https://github.com/xilopaint/alfred-urban-dictionary"


def main(wf):  # pylint: disable=redefined-outer-name
    """Run workflow."""
    query = wf.args[0]

    param = {"term": query}
    url = "http://api.urbandictionary.com/v0/define"
    r = web.get(url, params=param)
    r.raise_for_status()
    data = r.json()

    results = data["list"]

    for result in results:
        definition = re.sub(r'\[|\]', '', result["definition"])
        permalink = result["permalink"]
        thumbs_up = result["thumbs_up"]
        thumbs_down = result["thumbs_down"]
        word = result["word"]

        title = f'{word} (▲ {thumbs_up} / ▼ {thumbs_down})'
        subtitle = definition

        item = wf.add_item(
            title=title,
            subtitle=subtitle,
            arg=permalink,
            valid=True,
        )

        item.add_modifier(
            key="cmd",
            subtitle="Show Definition in Large Type",
            arg=definition,
        )

    return wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow(help_url=HELP_URL)
    sys.exit(wf.run(main))
