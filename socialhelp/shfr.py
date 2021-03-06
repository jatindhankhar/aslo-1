# Copyright (C) Sam Parkinson 2014
#
# This file is part of ASLO.
#
# ASLO is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ASLO is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with ASLO.  If not, see <http://www.gnu.org/licenses/>.

import os
import os.path
import json
import requests
from subprocess import call
from flask import Flask, redirect, jsonify

from helpers import crossdomain
import fc

DATA_DIR = os.environ['DATA_DIR']
SOCIALHELP = 'https://socialhelp.sugarlabs.org'
mappings = {}

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(SOCIALHELP)

@app.route('/goto/<id>')
def goto(id):
    if id == 'None':
        return redirect('{}/c/{}'.format(SOCIALHELP, 'sugar-shell'))
    if id in mappings:
        return redirect('{}/c/{}'.format(SOCIALHELP, mappings[id]))
    else:
        return redirect('{}/t/category-not-found/'.format(SOCIALHELP))

# Max amount of topics to show for comments
MAX_TOPICS = 50

def compress_forum_json(big_data):
    big_topics = big_data['topic_list']['topics']
    if len(big_topics) > MAX_TOPICS:
        big_topics = big_topics[:MAX_TOPICS]

    topics = []
    for t in big_topics:
        print t
        if t['pinned'] or not t['visible']:
            continue

        topics.append({
            't': t['title'],
            's': t['slug'],
            'p': t['posts_count'],
            'l': t['like_count']})
    return topics, \
           len(big_data['topic_list']['topics'])-1

@app.route('/goto/<id>.json')
@crossdomain('*')
def goto_json(id):
    if id in mappings:
        url = '{}/c/{}.json'.format(SOCIALHELP, mappings[id])
        r = requests.get(url, verify=False)
        if r.ok:
            data, count = compress_forum_json(r.json())
            return jsonify(success=True, data=data, count=count)
    return jsonify(success=False)

@app.route('/pull', methods=['POST'])
def pull():
    oldwd = os.getcwd()
    os.chdir(DATA_DIR)
    call(['git', 'pull', 'origin', 'master'])
    os.chdir(oldwd)

    fc.main()
    make_cache()
    return 'Cool Potatoes'

@app.route('/mappings')
def mappings_view():
    return json.dumps(mappings)

def make_cache():
    global mappings
    for p, id in ((os.path.join(DATA_DIR, f), f.rstrip('.json')) 
                   for f in os.listdir(DATA_DIR)
                   if os.path.isfile(os.path.join(DATA_DIR, f))):
        if p.endswith('.json') and 'featured.json' not in p:
            activity = json.load(open(p))
            mappings[id] = activity.get('socialhelp_category')

make_cache()
app.run(port=8000, debug=False, host='0.0.0.0')
