+++
title               = "Submodules in Git"
description         = "When to use submodules in git"
date                = "2021-01-05"
taxonomies.category = ["Programming"]
taxonomies.tags     = ["git"]
+++

# Should you use submodules in Git?

When starting a larger project, there is the question of how to partition code and if submodules could help.
With git, you can either put all your code in one repository or use submodules.

## Benefits of a single repository

- Simple
- Basic git knowledge suffices for the developers
- related commits to different components can be tracked under 1 feature branch and pull request
- Tools work faster if they do not have to recourse through submodules

## Benefits of Submodules

- Keep unrelated commits out of a component's repository.
    Git resolves conflicts very well, but a merge without conflicts can still break the repository. That is why `git merge` prepares a commit for you whenever the merge is not linear (fast forwardable). For example
  - A removes an "unused" function from `util`
  - B starts to use that function in `app`
- Reusing a component is as simple as including the components repository as submodule in another project. The entire history will be there, bugs fixed in that new project will be fixed for all uses of that component.
- Each repository is very small, which makes working with the repository faster. (But work on the entire project of multiple submodules becomes slower)
- Enforces good architecture

## Requirements to use submodules

Using submodules will work well for:

- Third Party code

- Non Code (Requirements documentation, test logs, build tools, ...)

- well encapsulated components which:

  - deal with 1 well defined responsibility
  - contain documentation: a README.md file which tells what this submodule represents,
    how the file tree is structured, __How to build it__, external dependencies,  ...
  - contain tests: The tests serve both as verification to create trust in the component as well as the most precise documentation by giving functional examples which are never out of date / unmaintained.
  - have a clear interface towards:
    - Software: A set of well documented functions that are usable by dependant code.
    - Tooling: A configuration for the build/bundle tool (`Makefile`, `CMakeLists.txt`, `setup.py`, ...)

  All of these can be expected of a well designed software component anyway.

- Changes to multiple submodules must be rare.

  - Touching 2 submodules will happen, when new functionality is added to a library L and later used by a dependant library or application D. When functionality is added, new L is a drop in replacement for old L.
- Is released in versions. When the submodule changes, the commit message should
  be `Bump BSP to v2.3.9` instead of `use newest BSP`.

## Indicators when not to use submodules

- your architecture will likely change
- your project is not that large
- The components are not that useful outside of that project.
- The code of the submodule can not be compiled into a library easily.

## So . . .

It must be mentioned, that the Linux kernel developers created `git` based on
their experience creating the kernel and they do not use submodules. They manage
twenty different architectures and hundreds of drivers and modules in one
single repository. But then,
the kernel is a very different kind of project, compared with whatever you are
planning.

If the use of submodules seems to create extra work this can be viewed to some
extend as effort that would be needed later, when untangling a component for
reuse in a different project.
If your pull requests in one repository stall because of other pull requests in
other repositories, those two components should probably be developed in the
same repository (for a while?).

My recommendation is to start with 1 repository and whenever a component appears
as a good submodule candidate, [extract it into one](@/git-extract-submodule.md).
