+++
title               = "NeoVim Remote as git diff tool"
description         = "use `neovim-remote` as git diff tool, for using git in nvim's `:terminal`"
date                = 2022-11-21
taxonomies.category = ["Unix"]
taxonomies.tags     = ["git", "vim"]
+++

# NeoVim Remote as git diff tool

In Neovim you can open a terminal and use git.
This git should not open another neovim when editing commit messages or rebase commands.
Instead, you want those files to open in a new tab. This can be accomplished with
[neovim-remote](https://pypi.org/project/neovim-remote/) and the following line in your vimrc:

```vim
let $EDITOR="nvr --remote-tab-wait"
```

For diff and merge, you can configure git to call `nvr`, in `git config --global --edit`:

```ini
[diff]
	tool = nvimdiff
[merge]
	tool = nvimmerge
[difftool "nvimdiff"]
	cmd = nvr -s -d \"$LOCAL\" \"$REMOTE\"
[mergetool "nvimmerge"]
	cmd = nvr -s -d \"$LOCAL\" \"$BASE\" \"$REMOTE\" \"$MERGED\" -c 'wincmd J | wincmd ='
```
