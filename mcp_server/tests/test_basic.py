import pytest
from mcp_server_neo4j_gds import server

def test_import_server():
    """Test that we can import the server module."""
    assert server is not None

def test_serialize_result_string():
    """Test the serialize_result function with string input."""
    result = "test string"
    serialized = server.serialize_result(result)
    assert serialized == "test string"

def test_serialize_result_list():
    """Test the serialize_result function with list input."""
    result = [1, 2, 3]
    serialized = server.serialize_result(result)
    assert "1" in serialized
    assert "2" in serialized
    assert "3" in serialized

def test_sample_data_fixture(sample_data):
    """Test that the sample_data fixture works."""
    assert len(sample_data["nodes"]) == 3
    assert len(sample_data["values"]) == 3
    assert sample_data["nodes"][0] == "A"
    assert sample_data["values"][0] == 1

def test_mock_gds_fixture(mock_gds):
    """Test that the mock_gds fixture works."""
    assert mock_gds.connected is True
    mock_gds.close()
    assert mock_gds.connected is False 