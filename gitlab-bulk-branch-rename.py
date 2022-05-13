#!/usr/bin/env python3

from urllib.parse import urlparse
import requests
import fire

SESSION = requests.session()


def rename_branch(url, token, group=None, protect_new=True, unprotect_old=True, delete_old=True, source="master", target="main"):
    """Migrate project branch to new remote branch using the Gitlab API.
    By default, marks new branch as protected and deletes old branch.

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
    """

    if not "&page=" in url:
        SESSION.headers.update({"Authorization": "Bearer %s" % (token)})
        if group:
            resp = SESSION.get(
                "%s/api/v4/groups/%d/projects?per_page=40&page=1" % (url, group))
        else:
            resp = SESSION.get("%s/api/v4/projects?per_page=40&page=1" % (url))
    else:
        resp = SESSION.get(url)
    root_url = "%s://%s" % (urlparse(url).scheme, urlparse(url).netloc)
    if resp.ok:
        for project in resp.json():
            proj_resp = SESSION.get(
                "%s/api/v4/projects/%s/repository/branches" % (root_url, project["id"]))
            if proj_resp.ok:
                branches = [branch["name"] for branch in proj_resp.json()]
                if target in branches:
                    print("Skipping project `%s`, it already has branch `%s`." %
                          (project["name"], target))
                else:
                    if source in branches:
                        br_resp = SESSION.post(
                            "%s/api/v4/projects/%s/repository/branches?branch=%s&ref=%s" % (root_url, project["id"], target, source))
                        if not br_resp.ok:
                            print("project %s: failed to create branch, response code %s" % (
                                project["name"], br_resp.status_code))
                            continue
                        default_br_resp = SESSION.put(
                            "%s/api/v4/projects/%s" % (root_url, project["id"]), data={"default_branch": target})
                        if not default_br_resp.ok:
                            print("project %s: failed to set default branch, response code %s" % (
                                project["name"], default_br_resp.status_code))
                            continue
                        if br_resp.ok and default_br_resp.ok:
                            print("project %s: `%s` created and set as default branch." % (
                                project["name"], target))
                            if protect_new:
                                r = SESSION.post(
                                    "%s/api/v4/projects/%s/protected_branches?name=%s" % (root_url, project["id"], target))
                                if not r.ok:
                                    print("failed to protect branch `%s`, API response code: %s" % (
                                        target, r.status_code))
                                else:
                                    print("protected branch `%s`." % (target))
                            if unprotect_old:
                                r = SESSION.delete(
                                    "%s/api/v4/projects/%s/protected_branches/%s" % (root_url, project["id"], source))
                                if not r.ok:
                                    print("failed to unprotect branch `%s`, API response code: %s" % (
                                        source, r.status_code))
                                else:
                                    print("unprotected branch `%s`." %
                                          (source))
                            if delete_old:
                                r = SESSION.delete(
                                    "%s/api/v4/projects/%s/repository/branches/%s" % (root_url, project["id"], source))
                                if not r.ok:
                                    print("failed to delete branch `%s`, API response code: %s" % (
                                        target, r.status_code))
                                else:
                                    print("deleted branch `%s`." % (source))
                    else:
                        print("Skipping project `%s`, it does not have a protected branch named `%s`." % (
                            project["name"], source))
            print()
        if resp.links.get("next"):
            rename_branch(resp.links["next"]["url"], token, group,
                          protect_new, unprotect_old, delete_old, source, target)
    else:
        print(resp.status_code)


if __name__ == "__main__":
    fire.Fire(rename_branch)
