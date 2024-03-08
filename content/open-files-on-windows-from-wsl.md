+++
title               = "Open Files on Windows from WSL"
description         = "Use the Windows default application to open files from the Windows Subsystem for Windows bash"
date                = 2022-03-19
updated             = 2024-03-08
taxonomies.category = ["Using Windows"]
taxonomies.tags     = ["wsl", "shell"]
+++

# Open Files on Windows from WSL

When you are in a WSL-bash and maybe generated an `svg` file and want to look at it, you can use the following bash function:

```bash
function o() {
    w=$(wslpath -wa "$1" | sed "s/'/''/g")
    /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -Command Start-Process "'${w}'"
}
```

What this does:
*   use `wslpath` to translate the argument into an absolute windows path. This will be something like `\\wsl.localhost\Ubuntu-20.04\home\wonko\tmp\file.svg`
*   Open __Windows Powershell__ (which is not the same as __Powershell__, see below)
*   Tell that to open the file with `Start-Process`.

Another nice tool is to open an explorer window with the file selected:

```bash
function x() {
    w=$(wslpath -wa "$1")
    /mnt/c/Windows/SysWOW64/explorer.exe /select, "$w"
    true # because explorer.exe has the weirdest return codes :/
}
```

## Earlier Attempts

The rest of this post is a deep dive into why `cmd.exe start` and
`explorer.exe` are weird, don't follow the windows best practices, and how
I managed to get it working anyways, until it broke in the spring of 2023.

### Using `cmd.exe start`

In 2022 I had never touched powershell, so I naturally used `cmd.exe` which has been around since I started with computers.
This no longer works, which I will address at the end of this article, but in 2022 it did work.
The function I came up with at the time was this:


```bash
function o() {
    w=$(wslpath -wa "$1")
    (
        builtin cd /mnt/c/Windows/System32
        exec cmd.exe /c start '"Foo"' "$w"
    )
}
```

The Windows command interpreter `cmd.exe` has many quirks. For example, it can not `cd` into `UNC` Paths (e.g. `\\server\path`) so you'd get a weird error message if you execute
`cmd.exe` on a path in the Linux file system.
(If you even have Windows exes in your PATH).
That is why we `cd` first, to the director that contains `cmd.exe`. And that is done in a sub shell, so we do not have to `cd` back.

You have to resolve the path with `wslpath` before `cd` so relative paths resolve correctly.

I use `builtin cd` because `cd` is an alias that records where I'm at so I can quickly jump there later with [bashjump](https://github.com/wonkodv/bashjump).

`start` is a builtin of the `cmd.exe` that does the same as double clicking on a file in the explorer.
If the `'"Foo"'` bothers you, then you are correct. It bothers me too. I'll get to that next.

### Argument Parsing on Windows is Not Like You Expect

Getting the above commands (using `explorer.exe` and `cmd.exe`) to work for files without spaces was trivial.
Maybe 3 minutes.
Getting them to work for files with spaces was hard.
Maybe 4 hours.

Because Windows command line parsing is special and `cmd.exe start` and `explorer.exe` are most very special.

On Unix, a process receives an array of strings as arguments.
It is the job of the calling process to supply that array.
A shell will typically split a string on whitespace unless those whitespace are surrounded by quotes or escaped with backslashes.
Other tools will either supply the array or ask the shell for help with splitting (see pythons `subprocess.Popen`).

A Windows process only gets 1 String.
The OS sometimes does some rather cursed[^1] interpretation
of double quotes and whitespace in order to get the right executable,
but the executable will always get the unmodified string, just as the caller supplied it.
Then all applications call [CommandLineToArgvW()](https://docs.microsoft.com/en-us/windows/win32/api/shellapi/nf-shellapi-commandlinetoargvw)
which splits like a Unix shell (but cursed[^2]).
All Applications? No. One small group of tools knows better, and of course `start` and `explorer` are among the rebellious.

The initial versions of the commands above had the following relevant lines:
*   `cmd.exe /c start "$w"`
*   `explorer.exe /select,"$w"`

With proper filenames that don't contain spaces, everything worked. With spaces, it didn't. I therefor tried to escape the spaces in bash so the exes would like
them better: among the this I tried were: `"$w"`, `'"'$w'"'`, `'"'"$w"'"'` and finally something like "${w// /\^ }" because
someone suggested you can escape space with carets.

I finally did the sensible thing and tried to get it working from cmd.exe, circumventing bash and the WSL-Windows bridge[^3].
Here are some samples of `cmd.exe start` executed from another `cmd.exe`
*   `cmd.exe /c start \\wsl$\Ubuntu-20.04\home\wonko\tmp\file.svg` works
*   `cmd.exe /c start \\wsl$\Ubuntu-20.04\home\wonko\tmp\file with space.svg` works
*   `cmd.exe /c start "\\wsl$\Ubuntu-20.04\home\wonko\tmp\file with space.svg"` opens a new terminal window,
    waiting on your input.
    If you look real close,
    you will notice this window has the title
    `\\wsl$\Ubuntu-20.04\home\wonko\tmp\file with space.svg` 🤔
*   `cmd.exe /c start "Foo" "\\wsl$\Ubuntu-20.04\home\wonko\tmp\file with space.svg"` works.

Getting information about `start` is simple,
you open `cmd.exe` and type `help start` and then very carefully note,
that the synopsis begins with `START ["Title"] ... [PROGRAMM|FILE] [ARGUMENTS...]`.
After you already know whats going on, the following questions become obvious:
*   how can the first positional argument be optional?
*   No single argument has quotes, why does title?
Yes. They really did. If the first argument is surrounded by quotes, it is Title, otherwise it is File.
Passing in a `"Title"` with quotes means even more quotes in bash `'"Foo"'` and things worked (Until an update in 2023, see below).

Getting information about what arguments you can pass to `explorer.exe` is surprisingly difficult.
Typing `help explorer` into `cmd.exe` can not help you but suggests you try `explorer /?` which only opens "My Documents".
Searching the web gives you FAQs, 3rd party sites which don't mention whitespace at all,
and one poor soul on stackexchange who, in their quest for answers, looked at explorer.exe in a hex editor.
I even tried with bing, hoping that they would know the way around msdn, but I did not find any vaguely official looking source of information.

Consensus is, that you call `explorer.exe /select,OBJECT` or `explorer.exe /select, OBJECT` to open `OBJECT`.
The comma is important, the whitespace after it isn't.

Here are some samples for `explorer.exe` again from a windows `cmd.exe`:
*   `explorer.exe /select,\\wsl$\Ubuntu-20.04\home\wonko\tmp\file.svg` works
*   `explorer.exe /select,\\wsl$\Ubuntu-20.04\home\wonko\tmp\file with space.svg` works
*   `explorer.exe /select,"\\wsl$\Ubuntu-20.04\home\wonko\tmp\file with space.svg"` works
*   `explorer.exe "/select,\\wsl$\Ubuntu-20.04\home\wonko\tmp\file with space.svg"` opens "My Documents", thank you very much
*   `explorer.exe /select, "\\wsl$\Ubuntu-20.04\home\wonko\tmp\file with space.svg"` works

The culprit is again, special treatment of quotes in the arguments.
Here, it is important that `/select` is not inside quotes.
The synopsis in a man page would be something like `explorer.exe /select,"PATH"`
The way to achieve this, when the WSL-Windows bridge adds double quotes,
is to use the `/select, PATH` syntax that includes a space not because `explorer.exe` needs
this space, but to put `/select` into a different slot in the argument array than the path,
preventing double quotes around the `/select`.

Conclusion: Don't try to deal with windows argument parsing and whitespace in paths at the same time.
And if you do, don't add WSL and bash to the mix.

### Windows is Constantly Improving

After a very optimistic, later regretted `wsl --update` in the spring of 2023,
the `cmd.exe start` no longer worked.
All I got when using `o FILE` was "Syntaxerror" on the terminal, nothing more.
After procrastinating for 3 Months and not having a working `o` function, I finally investigated.

Executing in a WSL Bash `cmd.exe /c start '"Foo"' "File"` now leads to a process on windows,
which has the command line `cmd.exe /c start "\"Foo\"" "File"`.
That is not something hat `cmd.exe` can deal with.
The folks at Microsoft did something to the "WSL-Windows Bridge"[^3], probably in an effort to
make anything better, and now quotes are escaped. For processes that use `CommandLineToArgvW()`,
this is  probably an improvement, since they now get the amount of quotes, that the caller intended.
The new behavior is probably better, but this makes it impossible to call `cmd.exe start` correctly.

I finally acknowledged, that `cmd.exe` is old and crappy, and informed myself about Powershell.

### Powershell


The first thing I learned about Powershell is, that Powershell is not Windows Powershell.
The first is new, cross platform, and typically installed in `C:\Program Files\Powershell\7\pwsh.exe`
while the second is old, Windows only, more powerful,
and installed in `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`.
The second option seemed a more stable Path that might be the same everywhere, so I'm using that.
Getting the windows powershell based version of `o` to work took 5 or 10 Minutes.
Information about `-Command` and `Start-Process` is easy to get, although they do try to confuse you,
by also providing `Invoke-Item` which has the same effect in my case.


### Improving the Powershell version

In the first pwsh version, I forgot to test with multiple whitespaces. This was pointed out to me on the discussions page on github, so I added
the `sed` part. I can now successfully `o "foo'bar    ba\z.txt"`. Windows translates the backslash to something weird, but it can be opened.

-------------------------------------

[^1]: Excerpt from [CreateProcessW](https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw) ig you pass `lpCommandLine` but not `lpApplicationName`:
> ... consider the string "c:\program files\sub dir\program name". This string can be interpreted in a number of ways. The system tries to interpret the possibilities in the following order:
>
> 1. c:\program.exe
> 2. c:\program files\sub.exe
> 3. c:\program files\sub dir\program.exe
> 4. c:\program files\sub dir\program name.exe

[^2]: Excerpt from  [CommandLineToArgvW()](https://docs.microsoft.com/en-us/windows/win32/api/shellapi/nf-shellapi-commandlinetoargvw)
> ... has a special interpretation of backslash characters when they are followed by a quotation mark character ("). This interpretation assumes that any preceding argument is a valid file system path, __or else it may behave unpredictably__.


[^3]: WSL-Windows Bridge is my placeholder name for whatever happens between the syscall into the linux kernel that bash does with its array of arguments and the
  process creation by the windows kernel with its single string.
