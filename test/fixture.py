import pytest


@pytest.fixture
def email_picture_fixture(shared_datadir):
    return {
        "path": shared_datadir / "ip_camera_picture.email",
        "num_of_emails": 1,
        "email_index": 0,
        "subject": "IPC Message",
        "num_of_attachments": 1,
        "attachment_index": 0,
        "attachment_name": "20210525151358560ch01.jpg",
    }


@pytest.fixture
def email_invalid_picture_fixture(shared_datadir):
    return {
        "path": shared_datadir / "ip_camera_invalid_picture.email",
        "email_index": 0,
        "num_of_attachments": 0,
    }


@pytest.fixture
def email_test_fixture(shared_datadir):
    return {
        "path": shared_datadir / "ip_camera_test.email",
        "num_of_emails": 1,
        "email_index": 0,
        "subject": "Mail_Test",
        "num_of_attachments": 0,
    }


@pytest.fixture
def email_multiple_fixture(shared_datadir):
    return {
        "path": shared_datadir / "ip_camera_multiple.email",
        "num_of_emails": 2,
        "email_index": 1,
        "subject": "IPC Message",
    }


@pytest.fixture
def file_names_fixture():
    return ["ch1.jpg", "icon.ico", "picture.png"]
