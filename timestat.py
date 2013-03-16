#!/usr/bin/python

# This file is part of Timestat.
#
# Timestat is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Timestat is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Timestat.  If not, see <http://www.gnu.org/licenses/>.

# Copyright (C) 2009 Csaba Hoch

"""Program for creating time statistics about activities one does.

Handy lines in .bashrc:

    function L
    # Adding a new action to the action file.
    {
        echo "[`date '+20%y-%m-%d %H:%M:%S'`]" "$@" >> .../myactionfile
    }

    function LE
    # Editing the action file.
    {
        gvim .../myactionfile
    }

    export ACTIONFILES=.../myactionfile

Example (assuming the previous lines are in bashrc):
    $ L mywork         # starting working on 'mywork'
    $ L stop           # 20 minutes later, stopping working on 'mywork'
    $ L 10 myotherwork # add 10 minutes to 'myotherwork'
    $ cat .../myactionfile
    [2009-07-25 20:33:07] mywork
    [2009-07-25 20:53:11] stop
    [2009-07-25 20:54:11] 10 myotherwork
    $ ./timestat.py
    {'myotherwork': 10, 'mywork': 20}
"""

from __future__ import with_statement
import sys
import re
import datetime
import optparse
import os

def timedelta_to_min(td):
    return int(td.total_seconds() / 60)

class ReMatch():

    def match(self, *args, **kw):
        self.r = re.match(*args, **kw)
        return self.r

    def __getattr__(self, attr):
        return getattr(self.r, attr)


class Action:

    def __str__(self):
        return ('<Action: '
                'datetime="%s" '
                'text=%s>' %
                (self.datetime, repr(self.text)))

    def __lt__(self, other):
        if self.type == 'interval':
            return True # intervals first
        else:
            return self.datetime < other.datetime

    def calc(self):
        r = ReMatch()
        if self.text == '':
            return False
        if self.text == 'stop':
            self.type = 'stop'
        elif r.match('^([^ ]+)$', self.text):
            self.type = 'start'
            self.activity = r.group(1)
        elif r.match('^([^ ]+) ([^ ]+)$', self.text):
            self.type = 'interval'
            self.timelen = int(r.group(1))
            self.activity = r.group(2)
        else:
            print 'WARNING: Incorrect line'
            return False
        return True

    def between(self, since, until):
        return ((since == None or self.datetime.date() >= since) and
                (until == None or self.datetime.date() <= until))


def parse_actionfile(filename):
    actions = []
    with open(filename) as f:
        #for line_number, line in enumerate(f):
        #    line_number += 1
        for line in f:
            line = line.strip()
            if line != '' and line[0] != '#':
                try:
                    r = re.match(
                            r'\[(?P<year>\d\d\d\d)-'
                            r'(?P<month>\d\d)-'
                            r'(?P<day>\d\d) '
                            r'(?P<hour>\d\d):'
                            r'(?P<minute>\d\d):'
                            r'(?P<second>\d\d)\] '
                            r'(?P<text>.*)',
                            line)
                    assert(r != None)
                    action = Action()
                    action.datetime = \
                        datetime.datetime(
                            int(r.group('year')),
                            int(r.group('month')),
                            int(r.group('day')),
                            int(r.group('hour')),
                            int(r.group('minute')),
                            int(r.group('second')))
                    action.text = r.group('text')
                    add = action.calc()
                    if add:
                        actions.append(action)
                except Exception:
                    print 'WARNING: Incorrect line'
    return actions

def collect_activities(actions):

    activities = {}

    def add_activity(activity, timelen):
        """Adds an activity to the dict."""
        activities[activity] = activities.get(activity, 0) + timelen

    current = None
    for index, action in enumerate(actions):
        if action.type == 'interval':
            add_activity(action.activity, action.timelen)
        elif action.type == 'stop':
            pass
        elif action.type == 'start':
            if index+1 < len(actions):
                nextactiontime = actions[index+1].datetime
            else:
                nextactiontime = datetime.datetime.now()
                current = action
            add_activity(
                action.activity,
                timedelta_to_min(nextactiontime - action.datetime))

    return activities, current

def collect_actions_2(actions):

    actions_res = []

    def add_action(activity, startime, timelen):
        """Adds an activity to the dict."""
        action = Action()
        action.text = activity
        action.datetime = startime
        action.timelen = timelen
        actions_res.append(action)

    for index, action in enumerate(actions):
        if action.type == 'interval':
            add_action(action.activity, action.datetime, action.timelen)
        elif action.type == 'stop':
            pass
        elif action.type == 'start':
            if index+1 < len(actions):
                nextactiontime = actions[index+1].datetime
            else:
                nextactiontime = datetime.datetime.now()
            add_action(
                action.activity,
                action.datetime,
                timedelta_to_min(nextactiontime - action.datetime))

    return actions_res

def date_str_to_date(s):
    r = re.match('(\d\d\d\d)-(\d\d)-(\d\d)', s)
    return \
        datetime.date(
            int(r.group(1)),
            int(r.group(2)),
            int(r.group(3)))

def parse_args():

    parser = optparse.OptionParser()

    parser.add_option('--since', dest='since',
                      help='Work with actions since this date. (yyyy-mm-dd)')
    parser.add_option('--until', dest='until',
                      help='Work with actions until this date. (yyyy-mm-dd)')
    parser.add_option('-f', '--actionfiles', dest='actionfiles',
                      help='Action files, separated with colon')
    parser.add_option('-w', dest='weekly_sum',
                      action='store_true', default=False,
                      help='Print a weekly summary.')
    parser.add_option('-s', '--sum', dest='sum',
                      action='store_true', default=False,
                      help='Print only the sum of the activity time.')
    parser.add_option('-i', '--ignore-activities', dest='ignore_activities',
                      default='',
                      help='Ignores the given activities. The activities are '
                      'separated by colons.')
    parser.add_option('-H', '--hour', dest='hour',
                      action='store_true', default=False,
                      help='Print in HH:MM format.')
    parser.add_option('-c', '--current', dest='current',
                      action='store_true', default=False,
                      help='Display the name of ongoing task, if any.')

    options, args = parser.parse_args()

    if options.since is not None:
        options.since = date_str_to_date(options.since)
    if options.until is not None:
        options.until = date_str_to_date(options.until)

    if options.actionfiles is not None:
        options.actionfiles = options.actionfiles.split(':')
    elif os.getenv('ACTIONFILES') is not None:
        options.actionfiles = os.getenv('ACTIONFILES').split(':')
    else:
        print 'You should set either the ACTIONFILES environment variable or '
        print 'give --actionfiles argument!'
        sys.exit(0)

    return options, args

def to_hour(i):
    return '%02d:%02d' % (i / 60, i % 60)

def main():
    options, args = parse_args()
    actions = []
    for actionfile in options.actionfiles:
        actions += parse_actionfile(actionfile)
    actions.sort()
    actions = [ action for action in actions
                if action.between(options.since, options.until) ]

    ignored_activities = \
        set(options.ignore_activities.split(':')) - set([''])

    if options.weekly_sum:
        actions = collect_actions_2(actions)
        d = {}
        for action in actions:
            if action.text not in ignored_activities:
                year, week_number, week_day = action.datetime.isocalendar()
                x = '%s-%02d' % (year, week_number)
                d.setdefault(x, 0)
                d[x] += action.timelen
        for k in sorted(d.keys()):
            print k,
            print 'x' * (d[k] / 60)

    else:
        d, c = collect_activities(actions)

        # Removing ignored activities
        keys = d.keys()
        for activity in keys:
            if activity in ignored_activities:
                del d[activity]

        if options.current:
            if c is not None:
                time = timedelta_to_min(datetime.datetime.now() - c.datetime)
                print '%s:%d' % (c.text, time)
        elif options.sum:
            time_sum = sum(d.values())
            if options.hour:
                time_sum = to_hour(time_sum)
            print time_sum
        else:
            if options.hour:
                d2 = {}
                for key, value in d.items():
                    d2[key] = to_hour(value)
            else:
                d2 = d
            for key, value in sorted(d2.items()):
                print '%s: %s' % (key, value)

main()
