+++
title = "Writing good shell scripts"
description = "How to write less ugly shell scripts"
date  = "2021-01-19"
updated = "2024-03-14"
taxonomies.category=["Programming"]
taxonomies.tags=["shell"]
+++

# How to write good shell scripts

I encounter (and have written) a lot of shell scripts which are horrible, so
here I want to present some ideas that would make me like your script more:

## Don't

__Don't write shell scrips!__ The language a shell implements is optimized to be as powerful as possible
in 1 line, while staying backwards compatible to the Bourne Shell (`sh`) release in 1978.
This goal is completely contrary to being readable.

Writing a shell script, because you find yourself executing the same line again and again,
comes naturally (not to everyone I guess) and makes sense.
But soon you add arguments.
Then argument verification.
Then Error messages.
Then you have 50 lines of spaghetti code with that one overly complicated one-liner at its center.
3 months later you have no clue how anything works and you rewrite the script.

Before you start on this path, stop.
Think about the tool you want to have and then write it in 150 lines of beautiful readable rust.
You will need more or less the same time, but now, maintenance of the tool is possible (easy).
You have probably already written 1 or 2 unit tests
for the complicated parts and `clap` gives you `--help` for free.

## But I have to

If you have to use shell or batch (e.g. no python, no binaries allowed, obscure security measures),
then you should still stop,
think about the tool you need and then write it in a proper fashion.
Every shell script should include:

-   Feedback on errors.
-   In bash, put `set -e` at the top so that the script aborts on failed
    commands.
-   Usage instructions, at least a good comment at the top, better yet that
    comment being printed when you call the script with `-h`.
-   If your script uses relative paths internally and does not take arguments,
    write `cd "$(dirname "$0")"` for unix shells or `cd /D %~dp0` in windows batch files.
    This makes the shell `cd` into the directory that the script lives in.
    Now relative paths work, even when the script is invoked from somewhere unexpected.
-   Comments for the more obscure features and syntax (do you know what `${s%%*/}` is? Are you aware that the
    value of `${SECONDS}` changes every second?)
