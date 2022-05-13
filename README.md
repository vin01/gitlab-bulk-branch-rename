# gitlab-bulk-branch-rename

Use Gitlab API to rename branches and help with bulk operations (eg. `master` -> `main` migration)

# usage

```
NAME
    gitlab-bulk-branch-rename.py - Migrate project branch to new remote branch using the Gitlab API. By default, marks new branch as pro
tected and deletes old branch.

SYNOPSIS
    gitlab-bulk-branch-rename.py URL TOKEN <flags>

DESCRIPTION
    url : str
        URL to the gitlab instance
    token: str
        access token for authentication
    group: int
        Group id for which projects need to be migrated to new branch
    protect_new: bool
        Protect the new/target branch
    unprotect_old: bool
        Unprotect old/source branch
    delete_old bool
        Delete old/source branch
    source: str
        Source branch from which new branch should be created
    target; str
        Target branch

POSITIONAL ARGUMENTS
    URL
    TOKEN

FLAGS
    --group=GROUP
        Type: Optional[]
        Default: None
    --protect_new=PROTECT_NEW
        Default: True
    --unprotect_old=UNPROTECT_OLD
        Default: True
    --delete_old=DELETE_OLD
        Default: True
    --source=SOURCE
        Default: 'master'
    --target=TARGET
        Default: 'main'
```
