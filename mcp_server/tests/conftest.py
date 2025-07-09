import pytest
import sys
import os
from pathlib import Path

# Add the src directory to the Python path so we can import our modules
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

@pytest.fixture
def sample_data():
    """Sample data for testing."""
    return {
        "nodes": ["A", "B", "C"],
        "values": [1, 2, 3]
    }

@pytest.fixture
def mock_gds():
    """Mock GraphDataScience object for testing."""
    class MockGDS:
        def __init__(self):
            self.connected = True
        
        def close(self):
            self.connected = False
    
    return MockGDS() 