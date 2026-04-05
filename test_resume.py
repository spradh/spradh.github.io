"""
Tests that index.html accurately represents key facts from the source resume (Profile (3).pdf).

Each test class covers one role. Tests check for:
  - The role title and company appearing in the HTML
  - Key quantitative facts (numbers, percentages, timeframes)
  - Key proper nouns (tools, products, initiatives)
  - Bold category titles present on each bullet

Run with: python test_resume.py
"""

import unittest
from html.parser import HTMLParser


class TextExtractor(HTMLParser):
    """Extracts all visible text from an HTML file."""

    def __init__(self):
        super().__init__()
        self.text = []
        self._skip_tags = {"script", "style"}
        self._current_skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in self._skip_tags:
            self._current_skip += 1

    def handle_endtag(self, tag):
        if tag in self._skip_tags:
            self._current_skip -= 1

    def handle_data(self, data):
        if self._current_skip == 0:
            self.text.append(data)

    def get_text(self):
        return " ".join(self.text).lower()


def load_page_text():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    parser = TextExtractor()
    parser.feed(html)
    return parser.get_text()


PAGE = load_page_text()


def contains(phrase):
    return phrase.lower() in PAGE


class TestStructure(unittest.TestCase):
    """Top-level structural checks."""

    def test_all_companies_present(self):
        for company in ["Meta", "General Mills", "UnitedHealth Group"]:
            self.assertTrue(contains(company), f"Missing company: {company}")

    def test_all_role_titles_present(self):
        roles = [
            "Data Scientist — Ranking",
            "Data Scientist — Reality Labs",
            "Lead Data Scientist",
            "Data Science Manager",
            "Senior Data Scientist",
            "Data Scientist — Venture Capital",
        ]
        for role in roles:
            self.assertTrue(contains(role), f"Missing role title: {role}")

    def test_bullet_titles_present(self):
        """Every bullet should have a bold category title (colon after the label)."""
        titles = [
            "Developer Experience:",
            "AI Impact Measurement:",
            "Platform Value",
            "Ecosystem Strategy:",
            "Developer Empowerment:",
            "Product Quality",
            "Enterprise AI Strategy:",
            "Impactful Pilots:",
            "Thought Leadership:",
            "Cloud Migration:",
            "Team Leadership:",
            "Data Pipeline Governance:",
            "AI-Driven Forecasting:",
            "ML System Migration:",
            "Seasonal Forecasting:",
            "Anomaly Detection:",
            "AI-Powered Crisis Response:",
            "Start-Up",
            "Deep Learning",
        ]
        for title in titles:
            self.assertTrue(contains(title), f"Missing bullet title: {title}")


class TestMetaRanking(unittest.TestCase):
    """DS — Ranking (Feb 2026–Present)"""

    def test_feature_store(self):
        self.assertTrue(contains("feature store"), "Missing: feature store")

    def test_ads_ranking(self):
        self.assertTrue(contains("ranking"), "Missing: ads ranking context")

    def test_north_star_metrics(self):
        self.assertTrue(contains("north star"), "Missing: North Star metrics")

    def test_revenue_impact(self):
        self.assertTrue(contains("revenue"), "Missing: revenue impact")

    def test_ml_engineer_developer_experience(self):
        self.assertTrue(contains("ML engineers"), "Missing: ML engineers developer experience")


class TestMetaRealityLabs(unittest.TestCase):
    """DS — Reality Labs (Sep 2025–Jan 2026)"""

    def test_dau_engagement(self):
        self.assertTrue(contains("DAU"), "Missing: DAU metric from resume")

    def test_immersive_web_sdk(self):
        self.assertTrue(contains("Immersive Web SDK"), "Missing: Immersive Web SDK")

    def test_bug_retention_framework(self):
        self.assertTrue(contains("retention"), "Missing: bug retention framework")

    def test_browser_app(self):
        self.assertTrue(contains("Browser app"), "Missing: Browser app context")


class TestGeneralMillsLead(unittest.TestCase):
    """Lead Data Scientist (Jan 2024–Aug 2025)"""

    def test_200mm_opportunity(self):
        self.assertTrue(contains("$200MM"), "Missing: $200MM+ opportunity figure")

    def test_80_percent_reduction(self):
        self.assertTrue(contains("80%"), "Missing: 80% reduction in operational overhead")

    def test_european_australian_markets(self):
        self.assertTrue(contains("European"), "Missing: European market deployment")
        self.assertTrue(contains("Australian"), "Missing: Australian market deployment")

    def test_ai_summit_attendees(self):
        self.assertTrue(contains("600"), "Missing: 600+ AI Summit attendees")

    def test_ai_hackathon(self):
        self.assertTrue(contains("Hackathon"), "Missing: 2024 GM AI Hackathon win")

    def test_ai_momentum_award(self):
        self.assertTrue(contains("Momentum Maker"), "Missing: AI Momentum Maker Award")


class TestGeneralMillsManager(unittest.TestCase):
    """Data Science Manager (Dec 2021–Dec 2023)"""

    def test_google_cloud_migration(self):
        self.assertTrue(contains("Google Cloud"), "Missing: Google Cloud migration")

    def test_five_products_migrated(self):
        self.assertTrue(contains("five"), "Missing: five products migrated to cloud")

    def test_team_size(self):
        self.assertTrue(contains("10-member"), "Missing: 10-member team size")

    def test_dbt_adoption(self):
        self.assertTrue(contains("dbt"), "Missing: dbt pipeline adoption")


class TestGeneralMillsSenior(unittest.TestCase):
    """Senior Data Scientist (Jul 2020–Nov 2021)"""

    def test_four_regions(self):
        self.assertTrue(contains("four"), "Missing: four U.S. regions for forecasting pilot")

    def test_nielsen_migration(self):
        self.assertTrue(contains("Nielsen"), "Missing: Nielsen system migration")

    def test_seasonal_forecasting(self):
        self.assertTrue(contains("seasonal"), "Missing: seasonal category forecasting models")

    def test_anomaly_detection(self):
        self.assertTrue(contains("anomaly detection"), "Missing: anomaly detection framework")

    def test_covid_context(self):
        self.assertTrue(contains("COVID-19"), "Missing: COVID-19 market disruption context")


class TestUnitedHealthGroup(unittest.TestCase):
    """Data Scientist — Venture Capital (May 2018–Jul 2020)"""

    def test_covid_dashboard_speed(self):
        self.assertTrue(contains("48 hours"), "Missing: 48-hour COVID dashboard deployment")

    def test_r_shiny(self):
        self.assertTrue(contains("R Shiny"), "Missing: R Shiny tool")

    def test_chief_science_officer(self):
        self.assertTrue(contains("Chief Science Officer"), "Missing: CSO audience detail")

    def test_level2_startup(self):
        self.assertTrue(contains("Level2"), "Missing: Level2 healthcare startup")

    def test_type2_diabetes(self):
        self.assertTrue(contains("Type 2 Diabetes"), "Missing: Type 2 Diabetes initiative")

    def test_keras(self):
        self.assertTrue(contains("Keras"), "Missing: Keras deep learning package")


if __name__ == "__main__":
    unittest.main(verbosity=2)
