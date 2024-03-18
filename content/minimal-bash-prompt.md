+++
title               = "Minimal Bash Prompt"
description         = "Working with a minimal bash prompt"
date                = 2022-09-24
taxonomies.category = ["Unix"]
taxonomies.tags     = ["bash"]
+++

# Minimal bash prompt

When I got into Unix, I made myself the ultimate bash prompt, with several modules each in its
own file included from `.bashrc`. When all are active (what I usually did)
they show:
*   time
*   user
*   host
*   git/svn status (colors for uncomitted/ unpushed changes, branch)
*   Jobs
*   Return code of previous command
*   In some configurations even SHLVL
*   If I'm in SSH
*   the python virtual env I'm in
*   Current python virtual Environment
*   The Id that the next command will have in `history` in case I want to reuse it with `!42`

{{ image(path="old-bash-prompt.png", alt="Screenshot of old bash prompt", title="Old bash
prompt showed everything and was rather confusing") }}


I've been using this for 10 years and then I stumbled upon someone on twitter who said `; ` is enough.
Thinking about that, I realized that I never really use all the information but it takes some time to generate on EVERY command.  (And on raspberries, the git prompt takes a loong time)

So now my bash prompt looks like this:

{{ image(path="new-bash-prompt.png", alt="Screenshot of new bash prompt", title="New bash prompt shows nothing unless you ask") }}

I previously had an alias `alias ?="git status"` which I used  *all the time*. So now my bash
prompt does nothing and is instantaneous, and my `?` command tells me everything.

```bash
alias ?="_status"
function _status() {
    local bold="\e[1m"
    local red="\e[1;31m"
    local clear="\e[0m"

    if [[ $(jobs |wc -l ) -gt 0 ]]
    then
        echo -e "${bold}Jobs${clear}"
        jobs
    fi

    if [ -n "$VIRTUAL_ENV" ]
    then
        echo -ne"${bold}VENV${clear}    "
        echo "$VIRTUAL_ENV"
    fi

    if [ -n "$SSH_CLIENT" ]
    then
        echo -ne "${bold}SSH${clear}   "
        echo "$SSH_CONNECTION"
    fi

    echo -en "${bold}ID${clear}      "
    [ "$USER" == root ] && echo -ne ${red}
    echo -e $USER${clear}@$HOSTNAME

    if [ -r /sys/class/power_supply/BAT0/ ]
    then
        echo -en "${bold}BATTERY${clear} "
        full=`cat /sys/class/power_supply/BAT0/energy_full`
        now=`cat /sys/class/power_supply/BAT0/energy_now`
        echo -n "$((now*100/full))% "
        cat /sys/class/power_supply/BAT0/status
    fi

    if   git rev-parse &>/dev/null
    then
        echo -e "${bold}GIT${clear}"
        git status -bs --show-stash --ahead-behind -M
        git stash list
    fi

    echo -en "${bold}PWD${clear}     "
    echo  "$PWD"
}
```

I set this up 3 months ago and am quite happy with it.
