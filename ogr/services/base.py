# MIT License
#
# Copyright (c) 2018-2019 Red Hat, Inc.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List, Optional, Match, Any

from ogr.abstract import (
    GitService,
    GitProject,
    GitUser,
    PRComment,
    IssueComment,
    Issue,
    PullRequest,
)
from ogr.exceptions import OgrException
from ogr.parsing import parse_git_repo
from ogr.read_only import if_readonly, GitProjectReadOnly
from ogr.utils import search_in_comments, filter_comments, deprecate_and_set_removal


class BaseGitService(GitService):
    def get_project_from_url(self, url: str) -> "GitProject":
        repo_url = parse_git_repo(potential_url=url)
        if not repo_url:
            raise OgrException(f"Cannot parse project url: '{url}'")
        project = self.get_project(repo=repo_url.repo, namespace=repo_url.namespace)
        return project


class BaseGitProject(GitProject):
    @property
    def full_repo_name(self) -> str:
        """
        Get repo name with namespace
        e.g. 'rpms/python-docker-py'

        :return: str
        """
        return f"{self.namespace}/{self.repo}"

    @deprecate_and_set_removal(
        since="0.9.0",
        remove_in="0.14.0 (or 1.0.0 if it comes sooner)",
        message="Use methods on PullRequest objects",
    )
    def get_pr_comments(
        self, pr_id, filter_regex: str = None, reverse: bool = False, author: str = None
    ) -> List[PRComment]:
        """
        Get list of pull-request comments.

        :param pr_id: int
        :param filter_regex: filter the comments' content with re.search
        :param reverse: reverse order of comments
        :param author: filter comments by author
        :return: [PRComment]
        """
        return self.get_pr(pr_id).get_comments(filter_regex, reverse, author)

    @deprecate_and_set_removal(
        since="0.9.0",
        remove_in="0.14.0 (or 1.0.0 if it comes sooner)",
        message="Use methods on PullRequest objects",
    )
    def search_in_pr(
        self,
        pr_id: int,
        filter_regex: str,
        reverse: bool = False,
        description: bool = True,
    ) -> Optional[Match[str]]:
        """
        Find match in pull-request description or comments.

        :param description: bool (search in description?)
        :param pr_id: int
        :param filter_regex: filter the comments' content with re.search
        :param reverse: reverse order of comments
        :return: re.Match or None
        """
        return self.get_pr(pr_id).search(filter_regex, reverse, description)

    @if_readonly(return_function=GitProjectReadOnly.pr_close)
    @deprecate_and_set_removal(
        since="0.9.0",
        remove_in="0.14.0 (or 1.0.0 if it comes sooner)",
        message="Use methods on PullRequest objects",
    )
    def pr_close(self, pr_id: int) -> "PullRequest":
        return self.get_pr(pr_id).close()

    @if_readonly(return_function=GitProjectReadOnly.pr_merge)
    @deprecate_and_set_removal(
        since="0.9.0",
        remove_in="0.14.0 (or 1.0.0 if it comes sooner)",
        message="Use methods on PullRequest objects",
    )
    def pr_merge(self, pr_id: int) -> "PullRequest":
        return self.get_pr(pr_id).merge()

    @deprecate_and_set_removal(
        since="0.9.0",
        remove_in="0.14.0 (or 1.0.0 if it comes sooner)",
        message="Use methods on PullRequest objects",
    )
    def get_pr_labels(self, pr_id: int) -> List[Any]:
        return self.get_pr(pr_id).labels

    @deprecate_and_set_removal(
        since="0.9.0",
        remove_in="0.14.0 (or 1.0.0 if it comes sooner)",
        message="Use methods on PullRequest objects",
    )
    def add_pr_labels(self, pr_id: int, labels: List[str]) -> None:
        return self.get_pr(pr_id).add_label(*labels)

    @deprecate_and_set_removal(
        since="0.9.0",
        remove_in="0.14.0 (or 1.0.0 if it comes sooner)",
        message="Use methods on PullRequest objects",
    )
    def get_pr_info(self, pr_id: int) -> "PullRequest":
        return self.get_pr(pr_id)

    @deprecate_and_set_removal(
        since="0.9.0",
        remove_in="0.14.0 (or 1.0.0 if it comes sooner)",
        message="Use methods on PullRequest objects",
    )
    def update_pr_info(
        self, pr_id: int, title: Optional[str] = None, description: Optional[str] = None
    ) -> "PullRequest":
        return self.get_pr(pr_id).update_info(title, description)

    @deprecate_and_set_removal(
        since="0.9.0",
        remove_in="0.14.0 (or 1.0.0 if it comes sooner)",
        message="Use methods on PullRequest objects",
    )
    def get_all_pr_commits(self, pr_id: int) -> List[str]:
        return self.get_pr(pr_id).get_all_commits()

    @deprecate_and_set_removal(
        since="0.9.0",
        remove_in="0.14.0 (or 1.0.0 if it comes sooner)",
        message="Use methods on PullRequest objects",
    )
    def _get_all_pr_comments(self, pr_id: int) -> List[PRComment]:
        return self.get_pr(pr_id)._get_all_comments()

    @if_readonly(
        return_function=GitProjectReadOnly.pr_comment,
        log_message="Create Comment to PR",
    )
    @deprecate_and_set_removal(
        since="0.9.0",
        remove_in="0.14.0 (or 1.0.0 if it comes sooner)",
        message="Use methods on PullRequest objects",
    )
    def pr_comment(
        self,
        pr_id: int,
        body: str,
        commit: str = None,
        filename: str = None,
        row: int = None,
    ) -> PRComment:
        return self.get_pr(pr_id).comment(body, commit, filename, row)

    @deprecate_and_set_removal(
        since="0.9.0",
        remove_in="0.14.0 (or 1.0.0 if it comes sooner)",
        message="Use methods on Issue objects",
    )
    def get_issue_comments(
        self,
        issue_id,
        filter_regex: str = None,
        reverse: bool = False,
        author: str = None,
    ) -> List[IssueComment]:
        return self.get_issue(issue_id).get_comments(filter_regex, reverse, author)

    @deprecate_and_set_removal(
        since="0.9.0",
        remove_in="0.14.0 (or 1.0.0 if it comes sooner)",
        message="Use methods on Issue objects",
    )
    def can_close_issue(self, username: str, issue: Issue) -> bool:
        return issue.can_close(username)

    @deprecate_and_set_removal(
        since="0.9.0",
        remove_in="0.14.0 (or 1.0.0 if it comes sooner)",
        message="Use methods on Issue objects",
    )
    def get_issue_info(self, issue_id: int) -> Issue:
        return self.get_issue(issue_id)

    @deprecate_and_set_removal(
        since="0.9.0",
        remove_in="0.14.0 (or 1.0.0 if it comes sooner)",
        message="Use methods on Issue objects",
    )
    def _get_all_issue_comments(self, issue_id: int) -> List["IssueComment"]:
        return self.get_issue(issue_id)._get_all_comments()

    @deprecate_and_set_removal(
        since="0.9.0",
        remove_in="0.14.0 (or 1.0.0 if it comes sooner)",
        message="Use methods on Issue objects",
    )
    def issue_comment(self, issue_id: int, body: str) -> "IssueComment":
        return self.get_issue(issue_id).comment(body)

    @deprecate_and_set_removal(
        since="0.9.0",
        remove_in="0.14.0 (or 1.0.0 if it comes sooner)",
        message="Use methods on Issue objects",
    )
    def issue_close(self, issue_id: int) -> Issue:
        return self.get_issue(issue_id).close()

    @deprecate_and_set_removal(
        since="0.9.0",
        remove_in="0.14.0 (or 1.0.0 if it comes sooner)",
        message="Use methods on Issue objects",
    )
    def get_issue_labels(self, issue_id: int) -> List[Any]:
        return self.get_issue(issue_id).labels

    @deprecate_and_set_removal(
        since="0.9.0",
        remove_in="0.14.0 (or 1.0.0 if it comes sooner)",
        message="Use methods on Issue objects",
    )
    def add_issue_labels(self, issue_id: int, labels: List[str]) -> None:
        self.get_issue(issue_id).add_label(*labels)


class BasePullRequest(PullRequest):
    def get_comments(
        self, filter_regex: str = None, reverse: bool = False, author: str = None
    ):
        all_comments = self._get_all_comments()
        return filter_comments(all_comments, filter_regex, reverse, author)

    def search(
        self, filter_regex: str, reverse: bool = False, description: bool = True
    ):
        all_comments: List[Any] = self.get_comments(reverse=reverse)
        if description:
            description_content = self.description
            if reverse:
                all_comments.append(description_content)
            else:
                all_comments.insert(0, description_content)

        return search_in_comments(comments=all_comments, filter_regex=filter_regex)


class BaseGitUser(GitUser):
    pass


class BaseIssue(Issue):
    def get_comments(
        self, filter_regex: str = None, reverse: bool = False, author: str = None
    ) -> List[IssueComment]:
        all_comments: List[IssueComment] = self._get_all_comments()
        return filter_comments(all_comments, filter_regex, reverse, author)

    def can_close(self, username: str) -> bool:
        return username == self.author or username in self.project.who_can_close_issue()
