from django.test import Client


# REVIEW: this test fails, dependency versions are wrong
def test_get_package():
    client = Client()
    response = client.get("/package/minimatch/3.1.2")
    assert response.status_code == 200
    assert response.json() == {
        "dependencies": [
            {
                "dependencies": [
                    {"dependencies": [], "name": "balanced-match", "version": "1.0.2"},
                    {"dependencies": [], "name": "concat-map", "version": "0.0.1"},
                ],
                "name": "brace-expansion",
                "version": "1.1.11",
            }
        ],
        "name": "minimatch",
        "version": "3.1.2",
    }


# REVIEW: add more tests for the API edge cases. Could also make the API client a pytest fixture
