[# gitlab-bulk-branch-rename

Use Gitlab API to rename branches and help with bulk operations (eg. `master` -> `main` migration)

*Note*: Unless a group id is passed using `--group`, it will rename branches for all projects which the auth token owner has access to.

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
    update_mrs
        Update open merge requests
    update_schedules
        Update pipeline schedules
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
    --update_mrs=UPDATE_MRS
        Default: True
    --update_schedules=UPDATE_SCHEDULES
        Default: True
    --source=SOURCE
        Default: 'master'
    --target=TARGET
        Default: 'main'
```
](https://github.com/vin01/gitlab-bulk-branch-rename/pulse)
