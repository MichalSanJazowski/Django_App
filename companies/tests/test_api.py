from unittest import TestCase
import json
import pytest
from django.test import Client
from django.urls import reverse
import logging

from companies.models import Company

@pytest.mark.django_db
class BasicCompanyAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.companies_url = reverse("companies-list")

    def tearDown(self):
        pass

class TestGetCompanies(BasicCompanyAPITestCase):
    def test_zero_companies_should_return_empty_list(self):
        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code,200)
        self.assertEqual(json.loads(response.content),[])

    def test_one_company_exist_should_succeed(self):
        test_company = Company.objects.create(name="New_one")
        response = self.client.get(self.companies_url)
        response_content = json.loads(response.content)[0]
        print(response_content)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response_content.get("name"),test_company.name)
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")
        test_company.delete()


class TestPostCompanies(BasicCompanyAPITestCase):
    def test_create_company_without_arguments_should_fail(self):
        response = self.client.post(path=self.companies_url)
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_content.get("name"), [
        "This field is required."
    ])
    def test_create_existing_company_should_fail(self):
        test_company = Company.objects.create(name="New_one")
        response = self.client.post(path=self.companies_url, data={"name":test_company.name})
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_content.get("name"), [
            "company with this name already exists."])
    def test_create_company_with_only_name_all_fields_should_be_default(self):
        response = self.client.post(path=self.companies_url, data={"name":"test company name"})
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_content.get("name"), "test company name")
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")
    def test_create_company_with_layoff_status(self):
        response = self.client.post(path=self.companies_url, data={"name":"another test company name","status": "Layoffs"})
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_content.get("status"), "Layoffs")

    def test_wrong_status_should_fail(self):
        response = self.client.post(path=self.companies_url,
                                    data={"name": "another new test company name", "status": "Layoffsen"})
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertIn( "is not a valid choice",str(response_content))

    @pytest.mark.xfail
    def test_should_be_ok_if_fails(self):
        self.assertEqual(1,2)

    @pytest.mark.skip
    def test_should_be_skipped(self):
        self.assertEqual(1, 2)

def test_raise_sample_exception():
    raise ValueError("Sample Exception")

def test_raise_sample_exception_should_pass():
    with pytest.raises(ValueError) as e:
        test_raise_sample_exception()
    assert "Sample Exception" == str(e.value)

logger = logging.getLogger("SAMPLE_LOGS")

def function_that_logs_something():
    try:
        raise ValueError("Sample Exception")
    except ValueError as e:
        logger.warning(f"I am logging {str(e)}")

def test_logged_warning_level(caplog):
    function_that_logs_something()
    assert "I am logging Sample Exception" in caplog.text

def test_logged_info_level(caplog):
    with caplog.at_level(logging.INFO):
        logger.info("I am logging info level")
        assert "I am logging info level" in caplog.text
