+++
title = "Extract a Submodule from a Git Repository"
description = "Extract a directory and its history into a new git repository"
date  = "2020-12-15"
taxonomies.category=["Programming"]
taxonomies.tags=["Git"]
+++

# Extract a Submodule from a Git Repository

Using several git commands, you can extract a directory and all of its commit
history into a new git repository and include that as a submodule.

`git subtree split` filters the entire commit history, collecting those that touched a directory, and produces a new commit chain from it.

## Prepare the server

A repository with submodules specifies the URL where to clone the sub repositories from. You must create a new repository on that server and fix access rights and stuff. It should be the same where everyone gets your project from.

## Extract the history

Extract the history of `component` and label it as the branch `split`. Prefix every commit message with `S!` to indicate that this commit happend before the split.

Go to your repository and execute the following command. Then grab a coffee because git now checks every commit in your projects history and this can takes 0.1 to 1 second per commit.

```
project$ git subtree split --prefix=component --branch split --annotate "S! " master
```

Once this is done, you can inspect the new history with `git log --stat split`.

## Create the sub repository

Delete the component from the project repository

```
project$ git rm -rf component
```

Create a dedicated repository

```
project$ mkdir component
project$ cd component
component$ git init
component$ cd ..
project$ 
```

Copy (push) the created history into the dedicated repo

```
project$ git push ./component split
```

There are no files in `component` yet, because `master` is the initial empty state and the branch`split` you just pushed is not checked out.

Got to the component repository and switch to `master` and, also do some cleanup:

- remove the `split` branch
- create a `.gitignore`
- create a commit that explains the extraction (use `--allow-empty` if you have no changed files to commit to add a note to the history)
- configure the `remote` and push

```
project$ cd component
component$ git -C master
component$ git branch -d split
component$ echo "stuff to ignore" >> .gitignore
component$ git add .gitignore
component$ git commit -m "extract component from project"
component$ git remote add server https://server/component
component$ git push server -u master master
component$ cd ..
project$ 
```

You now have a git repository for the component inside the project repository, but it is not a submodule yet. If you accidentally `git add` the component, there is a special warning message for you.

## Add the sub repository as submodule

```
project$ git submodule add https://server/component component
```

Note that `git submodule add` will not inspect or test the url when adding existing subrepositories. It will only write it into the `.gitmodules` file. Users who try to pull/clone your repository will notice any errors you make here before you do.

In the project repository, add the `.gitmodules` file and the submodule

```
project$ git add .gitmodules
project$ git add component
project$ git commit -m 'component: extract into submodule'
```

The last thing to do is to delete the `split` branch used to hold the artificial history in the project repository.

```
project$ git branch -D split
```

Test the entire project. If the component was successfully pushed to the server, you can now push the project.

```
project$ git push
```

Done. 5 Minutes + 1 coffee break.
