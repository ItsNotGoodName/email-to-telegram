import os
import pytest
from pytest_lazyfixture import lazy_fixture

from email_to_telegram.utils import (
    get_emails,
    get_attachments_paths,
    clear_attachments,
)
from .fixture import *


@pytest.mark.parametrize(
    "fixture",
    [
        lazy_fixture("email_picture_fixture"),
        lazy_fixture("email_test_fixture"),
        lazy_fixture("email_multiple_fixture"),
    ],
)
def test_get_emails(fixture):
    # Email file is not empty
    assert os.stat(fixture["path"]).st_size != 0

    emails, action_count = get_emails(fixture["path"])

    # Email file is now empty
    assert os.stat(fixture["path"]).st_size == 0
    # Check number of emails
    assert len(emails) == fixture["num_of_emails"]
    if fixture["num_of_emails"] > 0:
        email = emails[fixture["email_index"]]
        # Check email subject
        assert email.mail["subject"] == fixture["subject"]
    # Check how many times mail file was accessed
    assert action_count == 1


@pytest.mark.parametrize(
    "fixture",
    [
        lazy_fixture("email_picture_fixture"),
        lazy_fixture("email_invalid_picture_fixture"),
        lazy_fixture("email_test_fixture"),
    ],
)
def test_get_attachments_path(tmpdir, fixture):
    emails, action_count = get_emails(fixture["path"])
    email = emails[fixture["email_index"]]
    attachemnts = get_attachments_paths(email, tmpdir)
    # Check number of attachments
    assert len(attachemnts) == fixture["num_of_attachments"]
    if fixture["num_of_attachments"] != 0:
        # Attachment was created
        assert (
            attachemnts[fixture["attachment_index"]].basename
            == fixture["attachment_name"]
        )
        # Attachment file is not empty
        assert os.stat(attachemnts[fixture["attachment_index"]]).st_size != 0


def test_clear_attachments(tmpdir, file_names_fixture):
    for f in file_names_fixture:
        open(tmpdir / f, "a").close()

    assert len(os.listdir(tmpdir)) == len(file_names_fixture)
    clear_attachments(tmpdir)
    assert len(os.listdir(tmpdir)) == 0
