**Timestat** is a program for creating and displaying time statistics about
activities.

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

    $ timestat add myotherwork     # Some myotherwork again

    $ timestat add stop            # 10 minutes later, myotherwork stopped again

    $ timestat add 10 myotherwork  # Adding 10 minutes to 'myotherwork'
                                   # that we did while not at the computer

    $ cat $HOME/myactionfile
    [2009-07-25 20:00:00] mywork
    [2009-07-25 20:20:00] myotherwork
    [2009-07-25 20:40:00] mywork
    [2009-07-25 20:45:00] stop
    [2009-07-25 20:55:00] myotherwork
    [2009-07-25 21:05:00] stop
    [2009-07-25 22:05:00] 10 myotherwork

    $ ./timestat show
    mywork: 25
    myotherwork: 40

The same steps, assuming you have the [bashrc configuration](#bashrc)
described below (the `tq` alias switches to the previous state):

    $ tq mywork             # Started to work on 'mywork'

    $ tq myotherwork        # 20 minutes later, started to work on
                            # 'myotherwork'

    $ tq                    # Another 20 minutes later, back to 'mywork'
    "myotherwork" activity resumed

    $ tq stop               # 5 minutes later, stopped working

    $ tq                    # Some myotherwork again
    "myotherwork" activity resumed

    $ tq                    # 10 minutes later, myotherwork stopped again
    "myotherwork" activity stopped

    $ ts add 10 myotherwork  # Adding 10 minutes to 'myotherwork'
                            # that we did while not at the computer

    $ cat $HOME/myactionfile
    [2009-07-25 20:00:00] mywork
    [2009-07-25 20:20:00] myotherwork
    [2009-07-25 20:40:00] mywork
    [2009-07-25 20:45:00] stop
    [2009-07-25 20:55:00] myotherwork
    [2009-07-25 21:05:00] stop
    [2009-07-25 22:05:00] 10 myotherwork

    $ ./timestat show
    mywork: 25
    myotherwork: 40

Command-line commands and options
=================================

Timestat is a command line tool, and its general syntax is the following:

    timestat [options] [COMMAND [PARAMETERS]]

### Common options

- `-v, --verbose`: Display verbose printouts.

### add: add an action to the action file

Usage:

    timestat [options] a ACTION
    timestat [options] add ACTION

If more than one parameter is given, they will be joined and handled as one
action.

Options:

- `-f ACTIONFILES, --actionfiles ACTIONFILES`: Action files to be used,
  separated with a colon. If not specified, the `ACTIONFILES` environmental
  variable is used.
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

Switch to the previous state. The step is calculated in the following
way:

- If `ACTION` is specified, start work on that action. Otherwise:
- If an activity is ongoing (according to the action file), stop that activity.
- If there is no ongoing activity, find out the previous state (either
  'stopped' or a previous activity), and go into that state (i.e.
  either stop, or start the previous activity).

Options:

- `-f ACTIONFILES, --actionfiles ACTIONFILES`: Action files to be used,
  separated with a colon. If not specified, the `ACTIONFILES` environmental
  variable is used.
- `-a ACTIONFILE_SUBSTR, --actionfile ACTIONFILE_SUBSTR`: If
  `--actionfile` is specified, then `ACTION` will be added to the
  action file whose name contains `ACTIONFILE_SUBSTR`. If
  `--actionfile` is not specified, the first action file will be used.

Notes:

- If more than one parameter is given, they will be joined and handled
  as one action.
- Although the previous state is found out based on all action files,
  the new line will be added to the one specified by `--actionfile`
  (or the default one).

Examples: see the [Quick demo](#quick-demo) above.

### edit: open the action file in a text editor

Usage:

    timestat [options] e
    timestat [options] edit

The EDITOR environment variable is used to open the files.

Options:

- `-f ACTIONFILES, --actionfiles ACTIONFILES`: Action files to be used,
  separated with a colon. If not specified, the `ACTIONFILES` environmental
  variable is used.
- `-a ACTIONFILE_SUBSTR, --actionfile ACTIONFILE`: Specify which
  action file to open in the editor. If not specified, the first
  action file will be opened. If `--actionfile` is `"ALL"`, then all
  files will be opened.

### list: list all action files

Usage:

    timestat [options] list

Option:

- `-f ACTIONFILES, --actionfiles ACTIONFILES`: Action files to be used,
  separated with a colon. If not specified, the `ACTIONFILES` environmental
  variable is used.

### show-weekly-sum

TODO

### show-targets

TODO

### show-status

TODO

### show: show statistics about the activities

Usage (the two lines are equivalent):

    timestat [options]
    timestat [options] show

Different statistics are available with different options. The default
format is to print all activities with the minutes that have been
spent on them.

Options:

- `-f ACTIONFILES, --actionfiles ACTIONFILES`: Action files to be used,
  separated with a colon. If not specified, the `ACTIONFILES` environmental
  variable is used.
- `--since DATE`: Work with actions since this date. (Format: see
  below.)
- `--until DATE`: Work with actions until this date. (Format: see
  below.) The default value is `today`, which has the advantage that
  future targets are not yet taken into account.
- `--day DATE`: Work with actions on this date. (Format: see below.)
  `--day DATE` is equivalent to `--since DATE --until DATE`.
- `-w, --weekly-sum`: Print a weekly summary.
- `-s, --sum`: Print only the sum of the activity time.
- `-i, --ignore-activities`: Ignore the given activities. The activities should
  be separated with a colon.
- `-c, --current`: Display the name of ongoing task, if any, and the
  time since the last action.
- `--seconds`: Display the seconds in the printed intervals.

Date formats:

- `today`
- `yesterday`
- `yyyy-mm-dd`
- `mm-dd`: Given day in the current year. (Be careful with it in
  January, since `12-xx` means the end of the current year, not last
  year.)

Examples:

    $ timestat show
    mywork: 20
    myotherwork: 65

    $ timestat -H show
    mywork: 00:20
    myotherwork: 01:05

    $ timestat -c
    myotherwork:20

### test: run unit tests

Usage:

    timestat test

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
  `MM` or `HH:MM` format), and `ACTIVITY` may not contain whitespace.
  For example:

        10 myotherwork
        1:30 myotherwork

- **Increase target action**, which means that the target time of an
  activity is increased:

        increase-target ACTIVITY TIME_LENGTH

  where `ACTIVITY` may not contain whitespace. Examples:

        increase-target mywork 8:00
        increase-target work/task1 90

Action files do not have to be sorted.

### Comments 

Beside the descriptions of actions, an action file may contain empty
lines and comment. Comment are marked with a hash mark. A comment is
either a whole line, or it is after the description of an action. (In
the latter case, only hash marks preceeded by a space character are
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
