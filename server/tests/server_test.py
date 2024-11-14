import pytest
from server import app
from modules.data_types import ModelAlias


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_prompt_haiku(client):
    response = client.post(
        "/prompt", json={"prompt": "ping", "model": ModelAlias.haiku}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data["response"], str)
    assert isinstance(data["runTimeMs"], int)
    assert isinstance(data["inputAndOutputCost"], (int, float))
    assert data["runTimeMs"] > 0
    assert data["inputAndOutputCost"] >= 0


def test_prompt_sonnet(client):
    response = client.post(
        "/prompt", json={"prompt": "ping", "model": ModelAlias.sonnet}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data["response"], str)
    assert isinstance(data["runTimeMs"], int)
    assert isinstance(data["inputAndOutputCost"], (int, float))
    assert data["runTimeMs"] > 0
    assert data["inputAndOutputCost"] >= 0


def test_prompt_gemini_pro_2(client):
    response = client.post(
        "/prompt", json={"prompt": "ping", "model": ModelAlias.gemini_pro_2}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data["response"], str)
    assert isinstance(data["runTimeMs"], int)
    assert isinstance(data["inputAndOutputCost"], (int, float))
    assert data["runTimeMs"] > 0
    assert data["inputAndOutputCost"] >= 0


def test_prompt_gemini_flash_2(client):
    response = client.post(
        "/prompt", json={"prompt": "ping", "model": ModelAlias.gemini_flash_2}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data["response"], str)
    assert isinstance(data["runTimeMs"], int)
    assert isinstance(data["inputAndOutputCost"], (int, float))
    assert data["runTimeMs"] > 0
    assert data["inputAndOutputCost"] >= 0


def test_prompt_gemini_flash_8b(client):
    response = client.post(
        "/prompt", json={"prompt": "ping", "model": ModelAlias.gemini_flash_8b}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data["response"], str)
    assert isinstance(data["runTimeMs"], int)
    assert isinstance(data["inputAndOutputCost"], (int, float))
    assert data["runTimeMs"] > 0
    assert data["inputAndOutputCost"] >= 0


def test_prompt_gpt_4o_mini(client):
    response = client.post(
        "/prompt", json={"prompt": "ping", "model": ModelAlias.gpt_4o_mini}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data["response"], str)
    assert isinstance(data["runTimeMs"], int)
    assert isinstance(data["inputAndOutputCost"], (int, float))
    assert data["runTimeMs"] > 0
    assert data["inputAndOutputCost"] >= 0


def test_prompt_gpt_4o(client):
    response = client.post(
        "/prompt", json={"prompt": "ping", "model": ModelAlias.gpt_4o}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data["response"], str)
    assert isinstance(data["runTimeMs"], int)
    assert isinstance(data["inputAndOutputCost"], (int, float))
    assert data["runTimeMs"] > 0
    assert data["inputAndOutputCost"] >= 0


def test_prompt_gpt_4o_predictive(client):
    response = client.post(
        "/prompt", json={"prompt": "ping", "model": ModelAlias.gpt_4o_predictive}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data["response"], str)
    assert isinstance(data["runTimeMs"], int)
    assert isinstance(data["inputAndOutputCost"], (int, float))
    assert data["runTimeMs"] > 0
    assert data["inputAndOutputCost"] >= 0
