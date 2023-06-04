import pytest
import yaml
from app.utils import load_config, hash, verify

@pytest.fixture
def mock_config_file(tmp_path):
    config = {"key": "value"}
    config_file = tmp_path / "config.yaml"
    with open(config_file, "w") as f:
        yaml.dump(config, f)
    return config_file

def test_load_config(mock_config_file):
    config = load_config(mock_config_file)

    expected_config = {"key": "value"}
    assert config == expected_config

def test_hash_password():
    password = "my_password"
    hashed_password = hash(password)

    assert password != hashed_password

    assert verify(password, hashed_password)

def test_verify_password():
    password = "my_password"
    hashed_password = hash(password)

    assert verify(password, hashed_password)

    assert not verify("wrong_password", hashed_password)
