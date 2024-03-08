+++
title               = "Zola pre-push hook"
description         = "A pre-push hook to build zola"
date                = 2022-11-21
taxonomies.category = ["Using Unix"]
taxonomies.tags     = ["git", "zola"]
+++

# Zola pre-push hook

I commit the generated site files into my blog's repo because that is the easiest way to get github to host it for me.
In order to not forget to build, I wanted a hook that reminds me before I push.

Running `zola build` alone isn't enough, as it doesn't give an error return code or modify one of the files to be pushed.
`git diff` doesn't normally have a return code to indicate if there are diffs, but `git diff --quiet` does.
Combining both will build and then fail, if anything in `docs/` isn't added or committed.

```bash
zola build && git diff --quiet docs/
```

To include this in a [pre-commit](https://pre-commit.com) config, wrap it in `bash -c` and use as a system hook.
Check out me [.pre-commit-config.yaml](https://github.com/wonkodv/wonkodv.github.io/blob/main/.pre-commit-config.yaml).
