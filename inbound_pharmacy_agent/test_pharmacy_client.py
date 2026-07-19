from unittest.mock import patch, Mock
import requests

from pharmacy_client import PharmacyClient

SEED_RECORD = {
    "id": 1,
    "name": "HealthFirst Pharmacy",
    "phone": "+1-555-123-4567",
    "email": "contact@healthfirst.com",
    "city": "New York",
    "state": "NY",
    "prescriptions": [
        {"drug": "Lisinopril", "count": 42},
        {"drug": "Atorvastatin", "count": 38},
        {"drug": "Metformin", "count": 20},
    ],
}

NEW_SHAPE_RECORD = {
    "name": "Test New Pharmacy",
    "phone": "+1-555-NEW-LEAD-TEST",
    "avg_monthly_prescriptions": [],
    "id": "6",
    "address": "123 Test Street",
    "contactPerson": "Sarah Wilson",
    "email": "sarah@testnewpharmacy.com",
    "rxVolume": 4000,
}


def mock_ok_response(records):

    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = records
    return mock_response


@patch("pharmacy_client.requests.get")
def test_finds_pharmacy_with_seed_schema(mock_get):

    mock_get.return_value = mock_ok_response([SEED_RECORD])

    result = PharmacyClient().get_by_phone("+1-555-123-4567")

    assert result.name == "HealthFirst Pharmacy"
    assert result.location == "New York, NY"
    assert result.rx_volume == 100
    assert result.is_known is True


@patch("pharmacy_client.requests.get")
def test_finds_pharmacy_with_new_lead_schema(mock_get):
    mock_get.return_value = mock_ok_response([NEW_SHAPE_RECORD])

    result = PharmacyClient().get_by_phone("+1-555-NEW-LEAD-TEST")

    assert result.name == "Test New Pharmacy"
    assert result.location == "123 Test Street"
    assert result.rx_volume == 4000


@patch("pharmacy_client.requests.get")
def test_formatting_differences_still_match(mock_get):
   
    mock_get.return_value = mock_ok_response([SEED_RECORD])

    result = PharmacyClient().get_by_phone("1 (555) 123-4567")

    assert result is not None
    assert result.name == "HealthFirst Pharmacy"


@patch("pharmacy_client.requests.get")
def test_unrecognized_number_returns_none(mock_get):
    mock_get.return_value = mock_ok_response([SEED_RECORD, NEW_SHAPE_RECORD])

    result = PharmacyClient().get_by_phone("+1-555-000-0000")

    assert result is None


@patch("pharmacy_client.requests.get")
def test_api_failure_returns_none_instead_of_raising(mock_get):
    mock_get.side_effect = requests.RequestException("network down")

    result = PharmacyClient().get_by_phone("+1-555-123-4567")

    assert result is None
