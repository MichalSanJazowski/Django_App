from django.core.mail import send_mail
from django.core import mail
from django.test import TestCase, Client
import json
from unittest.mock import patch
import pytest


def test_send_email_should_succeed(mailoutbox, settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    assert len(mailoutbox) == 0
    send_mail(
        "Test Subject here",
        "Test Here is the message.",
        "testfrom@gmail.com",
        ["to@gmail.com"],
        fail_silently=False,
    )
    # Test that one message has been sent.
    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == "Test Subject here"


def test_send_email_without_arguments_should_send_empty_email(client):

    with patch("companies.views.send_mail") as mocked_send_mail_function:
        response = client.post(path="/send-email")
        response_content = json.loads(response.content)
        assert response.status_code == 200
        assert response_content["status"] == "success"
        assert response_content["info"] == "email sent successfully"
        mocked_send_mail_function.assert_called_with(
            subject=None,
            message=None,
            from_email="michaljazowski1995@gmail.com",
            recipient_list=["michaljazowski1995@gmail.com"],
        )


def test_send_email_with_get_verb_should_fail(client):
    response = client.get(path="/send-email")
    assert response.status_code == 405
    assert json.loads(response.content) == {"detail": 'Method "GET" not allowed.'}
