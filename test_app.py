import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from app import app


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def dash_app(dash_duo):
    """Start the Dash app and navigate to it before each test."""
    dash_duo.start_server(app)
    return dash_duo


@pytest.fixture(scope="session")
def driver():
    """Auto-download and configure ChromeDriver via webdriver-manager."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    d = webdriver.Chrome(service=service, options=options)
    yield d
    d.quit()


# ── Tests ─────────────────────────────────────────────────────────────────────

def test_header_is_present(dash_app):
    """The page title 'Pink Morsel Sales' should be visible in the header."""
    dash_app.wait_for_text_to_equal("h1", "Pink Morsel Sales", timeout=10)
    header = dash_app.find_element("h1")
    assert header is not None, "Header <h1> element was not found on the page."
    assert "Pink Morsel Sales" in header.text


def test_chart_is_present(dash_app):
    """The sales line chart (id='sales-chart') should be rendered on the page."""
    dash_app.wait_for_element("#sales-chart", timeout=10)
    chart = dash_app.find_element("#sales-chart")
    assert chart is not None, "Sales chart element (#sales-chart) was not found on the page."


def test_region_picker_is_present(dash_app):
    """The region radio button group (id='region-selector') should be present
    and contain all five expected options: all, north, south, east, west."""
    dash_app.wait_for_element("#region-selector", timeout=10)
    region_picker = dash_app.find_element("#region-selector")
    assert region_picker is not None, "Region selector (#region-selector) was not found on the page."

    # Verify all five radio options are rendered
    labels = dash_app.find_elements("#region-selector label")
    label_texts = [label.text.lower() for label in labels]

    for expected in ["all regions", "north", "south", "east", "west"]:
        assert any(expected in text for text in label_texts), (
            f"Expected region option '{expected}' not found in radio buttons. "
            f"Found: {label_texts}"
     )