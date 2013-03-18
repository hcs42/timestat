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

    $ timestat add stop            # Another 20 minutes later, stopped working

    $ timestat add myotherwork     # Some myotherwork again

    $ timestat add stop            # 10 minutes later, myotherwork stopped again

    $ timestat add 10 myotherwork  # Adding 10 minutes to 'myotherwork'
                                   # that we did while not at the computer

    $ cat $HOME/myactionfile
    [2009-07-25 20:00:00] mywork
    [2009-07-25 20:20:00] myotherwork
    [2009-07-25 20:40:00] stop
    [2009-07-25 20:50:00] myotherwork
    [2009-07-25 21:00:00] stop
    [2009-07-25 22:00:00] 10 myotherwork

    $ ./timestat show
    mywork: 20
    myotherwork: 40

The same steps, assuming you have the [bashrc configuration](#bashrc)
described below:

    $ TQ mywork             # Started to work on 'mywork'

    $ TQ myotherwork        # 20 minutes later, started to work on
                            # 'myotherwork'

    $ TQ                    # Another 20 minutes later, stopped working
    "myotherwork" activity stopped

    $ TQ                    # Some myotherwork again
    "myotherwork" activity resumed

    $ TQ                    # 10 minutes later, myotherwork stopped again
    "myotherwork" activity stopped

    $ T add 10 myotherwork  # Adding 10 minutes to 'myotherwork'
                            # that we did while not at the computer

    $ cat $HOME/myactionfile
    [2009-07-25 20:00:00] mywork
    [2009-07-25 20:20:00] myotherwork
    [2009-07-25 20:40:00] stop
    [2009-07-25 20:50:00] myotherwork
    [2009-07-25 21:00:00] stop
    [2009-07-25 22:00:00] 10 myotherwork

    $ T
    mywork: 20
    myotherwork: 40

Command-line commands and options
=================================

Timestat is a command line tool, and its general syntax is the following:

    timestat [options] [COMMAND [PARAMETERS]]

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
- `--actionfile ACTIONFILE_SUBSTR`: If `--actionfile` is specified, then
  `ACTION` will be added to the action file whose name contains
  `ACTIONFILE_SUBSTR`. If `--actionfile` is not specified, the first action
  file will be used.

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

Perform the "next logical step", according to the according file. The
step is calculated in the following way:

- If `ACTION` is specified, start work on that action. Otherwise:
- If an activity is ongoing (according to the action file), stop that activity.
- If there is no ongoing activity, resume the latest one.

If more than one parameter is given, they will be joined and handled as one
action.

Options:

- `-f ACTIONFILES, --actionfiles ACTIONFILES`: Action files to be used,
  separated with a colon. If not specified, the `ACTIONFILES` environmental
  variable is used.
- `--actionfile ACTIONFILE_SUBSTR`: If `--actionfile` is specified, then
  `ACTION` will be added to the action file whose name contains
  `ACTIONFILE_SUBSTR`. If `--actionfile` is not specified, the first action
  file will be used.

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
- `--actionfile ACTIONFILE`: Specify which action file to open in the editor.
  If not specified, the first action file will be opened. If `--actionfile` is
  `"ALL"`, then all files will be opened.

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
- `--since DATE`: Work with actions since this date. (Format: yyyy-mm-dd)
- `--until DATE`: Work with actions until this date. (Format: yyyy-mm-dd)
- `-w, --weekly-sum`: Print a weekly summary.
- `-s, --sum`: Print only the sum of the activity time.
- `-i, --ignore-activities`: Ignore the given activities. The activities should
  be separated with a colon.
- `-c, --current`: Display the name of ongoing task, if any, and the
  time since the last action.

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

The only exceptions to this rule are that an action files may contain
empty lines and comment lines (which start with hash mark), but these
are ignored by Timestat.

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

Bashrc
------

<a id="bashrc"></a>

The following lines are handy in `.bashrc` or `.bash_profile`:

    export ACTIONFILES=.../myactionfile # List of action files
    alias T=.../timestat                # timestat alias
    alias TQ=".../timestat quickadd"    # timestat alias

If you use multiple machines, it is convenient to use a separate
action file for each one, since this way you will have have merge
problems with synchronizing them.

Since the modifier commands (add, quickadd, edit) will use the first
action file by default, the most convenient setup is on each machine
to have the action file corresponding to that machine as the first
action file:

    # Bashrc of machine 1:
    export ACTIONFILES=.../machine_1.txt:.../machine_2.txt

    # Bashrc of machine 2:
    export ACTIONFILES=.../machine_2.txt:.../machine_1.txt
