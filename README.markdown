**Timestat** is a command-line program for creating and displaying time
statistics about activities.

Timestat's features include:

- Record actions like starting/stopping doing a task.
- Print different statistics and summaries.
- Set targets and print statistics about them.
- Select an activity with a pattern and/or interactively.
- All information is kept in plain-text files that are easy to edit manually
  too.

Quick demo
==========

<a id="quick-demo"></a>

Let's have a look at a quick demo of Timestat:

    $ export ACTIONFILES=$HOME/myactionfile

    $ timestat add mywork          # Started to work on 'mywork'

    $ timestat add myotherwork     # 20 minutes later, started to work on
                                   # 'myotherwork'

    $ timestat add mywork          # Another 20 minutes later, back to 'mywork'

    $ timestat add stop            # 5 minutes later, stopped working

    $ timestat add mywork          # Some mywork again

    $ timestat add stop            # 10 minutes later, mywork stopped again

    $ timestat add 10 myotherwork  # Adding 10 minutes to 'myotherwork'
                                   # that we did while not at the computer

    $ cat $HOME/myactionfile
    [2009-07-25 20:00:00] mywork
    [2009-07-25 20:20:00] myotherwork
    [2009-07-25 20:40:00] mywork
    [2009-07-25 20:45:00] stop
    [2009-07-25 20:55:00] mywork
    [2009-07-25 21:05:00] stop
    [2009-07-25 22:05:00] 10 myotherwork

    $ ./timestat show
    myotherwork: 00:30
    mywork: 00:35

The same steps, assuming you have the [bashrc configuration](#bashrc)
described below (the `tq` alias switches to the previous state):

    $ tq mywork             # Started to work on 'mywork'
    "mywork" activity started

    $ tq myotherwork        # 20 minutes later, started to work on
                            # 'myotherwork'
    "myotherwork" activity started, "mywork" activity stopped

    $ tq                    # Another 20 minutes later, back to 'mywork'
    "mywork" activity resumed, "myotherwork" activity stopped

    $ tq stop               # 5 minutes later, stopped working
    "mywork" activity stopped

    $ tq                    # Some mywork again
    "mywork" activity resumed

    $ tq                    # 10 minutes later, mywork stopped again
    "mywork" activity stopped

    $ ts add 10 myotherwork # Adding 10 minutes to 'myotherwork'
                            # that we did while not at the computer

    $ cat $HOME/myactionfile
    [2009-07-25 20:00:00] mywork
    [2009-07-25 20:20:00] myotherwork
    [2009-07-25 20:40:00] mywork
    [2009-07-25 20:45:00] stop
    [2009-07-25 20:55:00] mywork
    [2009-07-25 21:05:00] stop
    [2009-07-25 22:05:00] 10 myotherwork

    $ ./timestat show
    myotherwork: 00:30
    mywork: 00:35

Command-line commands and options
=================================

Timestat is a command line tool, and its general syntax is the following:

    timestat [options] [COMMAND [PARAMETERS]]

### Common options

- `-v, --verbose`: Display verbose printouts.
- `-f ACTIONFILES, --actionfiles ACTIONFILES`: Action files to be used,
  separated with a colon. If not specified, the `ACTIONFILES` environmental
  variable is used.
- `-i, --ignore-activities`: Ignore the given activities. The activities should
  be separated with a colon.
- `-o, --only-activities`: Consider only the given activities. The activities
  should be separated with a colon.
- `-I, --ignore-pattern`: Ignore the activities that match the pattern.
- `-O, --only-pattern`: Consider only the activities that match the pattern.
  `-i` and `-I` are stronger than `-o` and `-O`, i.e. if something is both
  ignored and included, it will be ignore. This way one can write queries like
  "all work activity except for programming". The following command prints all
  activities that start with "work" except for "work/meeting" (e.g.
  "work/programming" is included but "work/meeting" and "mywork" are not):

      timestat show -O "^work" -i work/meeting

- `--ignore-case`: Be case insensitive when evaluating whether an activity
  matches a regular expression pattern. Note that the action file is always
  considered to be case sensitive, so if it contains a "Work" and a "work"
  entry, those will be different activities even if `--ignore-case` is used.
- `--only-expr ONLY_EXPR`: `ONLY_EXPR` should be a Python 3 expression where the
  `h` variable contains the `Happening` object. The expression should return a
  boolean value. The effect of this option is those happenings will be ignored
  for which the expression's value is `False`. For example the following command
  considers only activities that started between 8am and 4pm:

      timestat show --only-expr \
        'h.is_event() and 8 <= int(h.starttime.strftime("%H")) <= 16'

  The `is_event` check is needed because targets are also filtered, but they are
  not events and hence they don't have a `starttime` data member.

  As another example, let's list all occasions when I worked on the weekend:

      timestat print events  -O work --only-expr \
        'h.is_event() and int(h.starttime.strftime("%w")) in (6, 7)'

- `--multiply-timelen NUMBER`: Multiple the "time length" values with this
  number.

### Options for specifying dates

- `--from DATE`: Ignore happenings before this date. (Format: see
  below.)
- `--to DATE`: Ignore happenings after this date. (Format: see below.) The
  default value is `today`, which has the advantage that future targets are not
  yet taken into account.
- `-d DATE, --day DATE`: Work with actions that happened/started during this
  day. (Format: see below.) `--day DATE` is equivalent to `--from DATE --to
  DATE`.
- `--week ISO_WEEK_NUMBER`: Work with actions that happened/started during this
  week. `--week ISO_WEEK_NUMBER` is equivalent to `--from wISO_WEEK_NUMBER-1
  --to wISO_WEEK_NUMBER-7`.
- `-t, --today` is equivalent to `--day today`.
- `-y, --yesterday` is equivalent to `--day yesterday`.
- `--this-week`: Work with days in this week.

Date formats:

- `t`, `today`
- `y`, `yesterday`
- `yy`: the day before yesterday.
- n times `y`: n days before yesterday.
- `YYYY-MM-DD`
- `MM-DD`: Given day in the current year. (Be careful with it in
  January, since `12-xx` means the end of the current year, which is 12 months
  in the future).
- `YYYY-wWW-D`: ISO week day (e.g. `2000-w02-3` is the Wednesday of week 2 in
  2000).
- `wWW-D`: ISO week day in the current year.

### full-help: print this README

Usage:

    timestat full-help

### add: add an action to the action file

Usage:

    timestat [options] a ACTION
    timestat [options] add ACTION

If more than one parameter is given, they will be joined and handled as one
action.

Options:

- `-f ACTIONFILES, --actionfiles ACTIONFILES`: see "Common Options".
- `-a ACTIONFILE_SUBSTR, --actionfile ACTIONFILE_SUBSTR`: If
  `--actionfile` is specified, then `ACTION` will be added to the
  action file whose name contains `ACTIONFILE_SUBSTR`. If
  `--actionfile` is not specified, the first action file will be used.

Examples:

    $ timestat add programming         # Started programming now
    $ timestat add stop                # Stopped programming
    $ timestat add 20 programming      # Add 20 minutes of programming

    # The "second" action file is modified:
    $ timestat \
          --actionfiles=firstfile.txt:secondfile.txt \
          --actionfile=second \
          add 20 programming

### quickadd: perform the "next logical step"

Usage:

    timestat [options] quickadd
    timestat [options] quickadd ACTION
    timestat [options] quickadd %ACTICITY_PATTERN

Switch to the previous state. The step is calculated in the following
way:

- If `ACTION` is specified, start work on that action.
- If an `ACTICITY_PATTERN` is specified after a percentage sign, find the
  activities with that pattern. If there is only one, start working on it; if
  there is more, ask the user which one they meant.

Otherwise (i.e. if no action or activity pattern is specified):

- If an activity is ongoing (according to the action file), stop that activity.
- If there is no ongoing activity, find out the previous state (either
  'stopped' or a previous activity), and go into that state (i.e.
  either stop, or start the previous activity).

Options described in "Common options":

- `-f ACTIONFILES, --actionfiles ACTIONFILES`
- `-i, --ignore-activities`
- `-o, --only-activities`
- `-I, --ignore-pattern`
- `-O, --only-pattern`
- `--ignore-case`: applies to ignore pattern, only pattern and activity pattern.
- `--only-expr ONLY_EXPR`

Other options:

- `-a ACTIONFILE_SUBSTR, --actionfile ACTIONFILE_SUBSTR`: See the `add` command.

Notes:

- If more than one parameter is given, they will be joined and handled
  as one action.
- Although the previous state is found out based on all action files,
  the new line will be added to the one specified by `--actionfile`
  (or the default one).

Examples: see the [Quick demo](#quick-demo) above.

Example about the activity pattern:

    $ tq %hobby/cp   # I want to start work on a task that matches the
                     # "hobby/cp" regular expression
    Select the desired match (empty line = cancel):
    1: hobby/cp/erl-utils
    2: hobby/cp/ew
    3: hobby/cp/exponwords
    4: hobby/cp/offline-issues
    5: hobby/cp/permet
    6: hobby/cp/vim-erlang-tags
    7: hobby/cp/vim-erlang-tags/python-rewrite
    > 2              # The number "2" is typed by the user
    "hobby/cp/ew" activity started
    $

### edit: open the action file in a text editor

Usage:

    timestat [options] e
    timestat [options] edit

The EDITOR environment variable is used to open the files.

Options:

- `-f ACTIONFILES, --actionfiles ACTIONFILES`: see "Common Options".
- `-a ACTIONFILE_SUBSTR, --actionfile ACTIONFILE`: Specify which
  action file to open in the editor. If not specified, the first
  action file will be opened. If `--actionfile` is `"ALL"`, then all
  files will be opened.

### list: list all action files

Usage:

    timestat [options] list

Option:

- `-f ACTIONFILES, --actionfiles ACTIONFILES`: see "Common Options".

### show: show statistics about the activities

Usage (the two lines are equivalent):

    timestat [options]
    timestat [options] show

Different statistics are available with different options. The default
format is to print all activities with the minutes that have been
spent on them.

Options described in "Common options":

- `-f ACTIONFILES, --actionfiles ACTIONFILES`
- `-i, --ignore-activities`
- `-o, --only-activities`
- `-I, --ignore-pattern`
- `-O, --only-pattern`
- `--ignore-case`
- `--only-expr ONLY_EXPR`
- `--multiply-timelen NUMBER`

Options described in "Options for specifying dates":

- `--from DATE`
- `--to DATE`
- `-d DATE, --day DATE`
- `-t, --today`
- `-y, --yesterday`

Other options:

- `-w, --weekly-sum`: Print a weekly summary (same as the `show-sum weekly`
  command).
- `-s, --sum`: Print only the sum of the activity time.
- `--nosum`: Don't print the sum of the activity time.
- `--sort-time`: Sort the result by activity time.
- `-c, --current`: Display the name of ongoing task, if any, and the
  time since the last action.
- `--seconds`: Display the seconds in the printed intervals.

Examples:

    $ timestat show
    mywork: 20
    myotherwork: 65

    $ timestat -H show
    mywork: 00:20
    myotherwork: 01:05

    $ timestat -c
    myotherwork:20

### show-sum: show a daily/weekly/monthly summary

Usage:

    timestat [options] show-sum daily
    timestat [options] show-sum weekly
    timestat [options] show-sum monthly

Show a summary about how much time was spent on activities per day/per week/per
month.

Options described in "Common options":

- `-f ACTIONFILES, --actionfiles ACTIONFILES`
- `-i, --ignore-activities`
- `-o, --only-activities`
- `-I, --ignore-pattern`
- `-O, --only-pattern`
- `--ignore-case`
- `--only-expr ONLY_EXPR`
- `--multiply-timelen NUMBER`

Options described in "Options for specifying dates":

- `--from DATE`
- `--to DATE`
- `-d DATE, --day DATE`
- `-t, --today`
- `-y, --yesterday`

Other options:

- `--fill`: Print all dates (not only those with time spent).
- `--show-time`: Print time too.
- `--avg`: Print the average time spent.
- `--block-size SECONDS`: Defines how many seconds should one "x" represent.

Example (one `x` means one hour spent):

    $ timestat show-sum daily -O ^work
    2014-01-20 (06:20) xxxxxx
    2014-01-21 (08:20) xxxxxxxx
    2014-01-22 (09:34) xxxxxxxxx
    2014-01-23 (07:19) xxxxxxx
    2014-01-24 (08:34) xxxxxxxx

    $ timestat show-sum weekly --show-time -O ^hobby
    2014-w01 (21:20) xxxxxxxxxxxxxxxxxxxxx
    2014-w02 (07:15) xxxxxxx
    2014-w03 (13:06) xxxxxxxxxxxxx
    2014-w04 (16:52) xxxxxxxxxxxxxxxx
    2014-w05 (09:24) xxxxxxxxx
    2014-w06 (18:04) xxxxxxxxxxxxxxxxxx

### show-targets

Usage:

    timestat [options] st
    timestat [options] show-targets

Show a summary about the targets. See the "Targets" section for more information
about targets.

Options described in "Common options":

- `-f ACTIONFILES, --actionfiles ACTIONFILES`
- `-i, --ignore-activities`
- `-o, --only-activities`
- `-I, --ignore-pattern`
- `-O, --only-pattern`
- `--ignore-case`
- `--only-expr ONLY_EXPR`
- `--multiply-timelen NUMBER`

Options described in "Options for specifying dates":

- `--from DATE`
- `--to DATE`
- `-d DATE, --day DATE`
- `-t, --today`
- `-y, --yesterday`

Example: see the "Targets" section.

### show-status

Usage:

    timestat [options] ss
    timestat [options] show-status

Show the current or last activity.

Options described in "Common options":

- `-f ACTIONFILES, --actionfiles ACTIONFILES`

Example:

    $ timestat show-status
    State: on
    Current activity: hobby/timestat
    Start time: 15:37
    Current time: 15:44
    Time since started: 00:06

### print: print objects

Usage:

    timestat [options] print actions
    timestat [options] print events
    timestat [options] print happenings
    timestat [options] print activities

Print all objects of the given type.

Options described in "Common options":

- `-f ACTIONFILES, --actionfiles ACTIONFILES`
- `-i, --ignore-activities`
- `-o, --only-activities`
- `-I, --ignore-pattern`
- `-O, --only-pattern`
- `--ignore-case`
- `--only-expr ONLY_EXPR`
- `--multiply-timelen NUMBER`

Options described in "Options for specifying dates":

- `--from DATE`
- `--to DATE`
- `-d DATE, --day DATE`
- `-t, --today`
- `-y, --yesterday`

### test: run unit tests

Usage:

    timestat test

### test-coverage: run unit tests

Usage:

    timestat tc
    timestat test-coverage

Action files
------------

An example action file looks like this:

    [2009-07-25 20:33:07] mywork
    [2009-07-25 20:53:11] stop
    [2009-07-25 20:54:11] 10 myotherwork

First let's get some terminology out of the way:

- An **activity** is something you can do for periods of time. In the
  example above, `mywork` and `myotherwork` are activities.
- An **action** is something that happens at a certain moment. The
  example above describes three actions:

  1. Starting to work on `mywork`;
  2. Stopping to work on `mywork`;
  3. Working 10 minutes on `myotherwork`.

  Not all actions relate to concrete time logged: for example if
  the target time for an activity is increased, that is also an
  action.

- An **event** is something that is happening during a period of time.
  It has a beginning and an end. The example above describes two
  events:

  1. Working 30:04 minutes on `mywork`.
  2. Working 10 minutes on `myotherwork`.

- A **happening** is either an event or an action that cannot be converted into
  an event. Currently this means that a happening is either an event or a
  target.

As you see, all **lines** in the action file describe an action, and
they must follow the same format: a date (in the format above) and an
action text:

    [YYYY-mm-dd HH:MM:SS] ACTION_TEXT

The only exceptions to this rule are empty lines and comments, see later.

The **action text** may have the following formats:

- **Start action**, which means that an activity is started (and if
  there is any other ongoing activity, that is finished):

        ACTIVITY

  where `ACTIVITY` may not contain whitespace. Examples:

        mywork
        work/task1
        hobby/english/Catch22

- **Stop action**, which means that the ongoing activity is stopped:

        stop

- **Interval action**, which means that some additional time should be
  logged on an activity (without interfering with an ongoing activity):

        TIME_LENGTH ACTIVITY

  where `TIME_LENGTH` specifies the length of the activity (either in
  `MM`, `HH:MM` or `HH:MM:SS` format), and `ACTIVITY` may not contain
  whitespace. For example:

        10 myotherwork
        1:30 myotherwork
        1:30:12 myotherwork

- **Increase target action**, which means that the target time of an
  activity is increased:

        increase-target ACTIVITY TIME_LENGTH

  where `ACTIVITY` may not contain whitespace. Examples:

        increase-target mywork 8:00
        increase-target work/task1 90

Action files do not have to be sorted.

Currently if an activity is started in an action file, it has to be finished in
that file. This is planned to be changed in the future.

### Comments

Beside the descriptions of actions, an action file may contain empty
lines and comment. Comment are marked with a hash mark. A comment is
either a whole line, or it is after the description of an action. (In
the latter case, only hash marks preceded by a space character are
considered comments.)

So for example the following is a valid action file:

    # My work
    [2009-07-25 20:33:07] mywork # wow, this was hard
    [2009-07-25 20:53:11] stop

    # My jobs
    [2009-07-25 20:54:11] job#01 # this was hard too
    [2009-07-25 21:23:11] job#02 # this was easy
    [2009-07-25 21:30:11] stop

In this example, the activities are called "mywork", "job#01" and
"job#02".

### Targets

You can define targets about how much you want to spend with a certain task
group.

For example your action file might contain the following:

    [2013-02-01 00:00:00] increase-target work 8:00
    [2013-02-02 00:00:00] increase-target work 8:00
    [2013-02-03 00:00:00] increase-target work 8:00
    [2013-02-04 00:00:00] increase-target work 8:00
    [2013-02-01 09:00:00] work
    [2013-02-01 17:00:00] stop # 8 hours of work
    [2013-02-02 09:00:00] work
    [2013-02-02 17:00:00] stop # 8 hours of work
    [2013-02-03 09:00:00] work
    [2013-02-03 18:00:00] stop # 9 hours of work
    [2013-02-04 09:00:00] work
    [2013-02-04 15:00:00] stop # 6 ours of work

Timestat can produce the following reports:

    $ timestat
    work: 31:00
    Sum: 31:00

    $ timestat show-targets
    Target name: work
    Target time: 32:00
    Actual time: 31:00
    Difference: -01:00

Only targets between `from` and `to` are considered:

    $ timestat show-targets --day 2013-02-03
    Target name: work
    Target time: 08:00
    Actual time: 09:00
    Difference: 01:00

Since `to` is "today" by default, the future targets are ignored by default, so
you can add all workdays in the month is advance, you can still track your
balance every day.

Bashrc
------

<a id="bashrc"></a>

The following lines are handy in `.bashrc` or `.bash_profile`:

    export ACTIONFILES=.../myactionfile # List of action files
    alias ts=.../timestat                # timestat alias
    alias tq=".../timestat quickadd"    # timestat alias

If you use multiple machines, it is convenient to use a separate
action file for each one, since this way you will not have merge
problems with synchronizing them.

Since the modifier commands (add, quickadd, edit) will use the first
action file by default, the most convenient setup is on each machine
to have the action file corresponding to that machine as the first
action file:

    # Bashrc of machine 1:
    export ACTIONFILES=.../machine_1.txt:.../machine_2.txt

    # Bashrc of machine 2:
    export ACTIONFILES=.../machine_2.txt:.../machine_1.txt

How to contribute
-----------------

Timestat's unit tests provide 100% code coverage and I want to keep it that way.
I also want to keep everything documented.

So I will accept pull requests only if:

- The new code has proper unit tests and keeps this rule. This is fortunately
  easy because Timestat has built-in commands for executing all unit tests
  measuring their coverage (`test` and `test-coverage`).
- The new features are documented in the README.
- The new code does not contain training white space or lines longer than 80
  characters.

It is recommended to put the following code into `'.git/hooks/pre-commit'`
(`chmod +x` is also necessary) before creating commits:

    #!/bin/bash

    if ./timestat test; then
        true # skip
    else
        echo "pre-commit hook: error: unit test failed, no commit."
        exit 1
    fi

    if grep ' \+$' timestat README.markdown -q; then
        echo "pre-commit hook: error: trailing white space"
        exit 1
    fi

    if grep '.\{81,\}' timestat README.markdown -q; then
        echo "pre-commit hook: error: line longer than 80 character"
        exit 1
    fi
