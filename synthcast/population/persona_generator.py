"""
PersonaGenerator: A module for generating diverse synthetic personas based on demographic data
"""

import json
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

@dataclass
class OccupationCategories:
    """Predefined occupation categories for different industries."""
    
    agriculture: List[str] = field(default_factory=list)
    industry: List[str] = field(default_factory=list)
    manufacturing: List[str] = field(default_factory=list)
    services: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.agriculture = [
            "farmer", "agricultural worker", "farm manager", "fishery worker", 
            "forest worker", "agricultural technician"
        ]
        self.industry = [
            "factory worker", "machine operator", "welder", "electrician",
            "construction worker", "mechanical engineer", "chemical engineer",
            "production supervisor", "quality control inspector", "carpenter",
            "plumber", "automotive technician"
        ]
        self.manufacturing = [
            "assembly line worker", "manufacturing technician", "industrial engineer",
            "production manager", "quality assurance specialist", "process engineer",
            "machinist", "equipment operator", "industrial maintenance technician"
        ]
        self.services = [
            "software engineer", "teacher", "nurse", "sales representative",
            "financial analyst", "marketing manager", "accountant", "chef",
            "retail manager", "bank teller", "insurance agent", "real estate agent",
            "healthcare worker", "IT consultant", "lawyer", "doctor",
            "graphic designer", "human resources manager", "customer service representative",
            "hotel manager", "restaurant owner", "small business owner"
        ]

@dataclass
class PersonaTraits:
    """Predefined personality traits and characteristics for persona generation."""
    
    personality: List[str] = field(default_factory=list)
    financial_attitudes: List[str] = field(default_factory=list)
    economic_concerns: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.personality = [
            "conservative", "progressive", "risk-averse", "entrepreneurial",
            "traditional", "innovative", "cautious", "ambitious"
        ]
        self.financial_attitudes = [
            "values financial security", "focuses on long-term savings",
            "prioritizes immediate needs", "balances saving and spending",
            "interested in investment opportunities", "prefers stable income",
            "concerned about retirement planning", "values work-life balance"
        ]
        self.economic_concerns = [
            "worried about inflation", "focused on career growth",
            "concerned about job security", "interested in property ownership",
            "planning for retirement", "managing student loans",
            "supporting family", "growing business opportunities"
        ]

class PersonaGenerator:
    """
    Generate synthetic personas based on demographic data.
    
    This class creates realistic persona descriptions using demographic, economic,
    and social data from different countries. It ensures the generated personas
    reflect the actual distribution of population characteristics.
    """

    def __init__(self, population_data_path: Optional[str] = None):
        """
        Initialize the PersonaGenerator with population data.
        
        Args:
            population_data_path: Path to the JSON file containing population data.
                                If None, uses the default data file.
        """
        if population_data_path is None:
            population_data_path = str(Path(__file__).parent.parent / 'data'/"reference"/ 'population.json')
        
        self.population_data = self._load_population_data(population_data_path)
        self.occupations = OccupationCategories()
        self.traits = PersonaTraits()

    def _load_population_data(self, file_path: str) -> Dict:
        """Load and parse the population data JSON file."""
        with open(file_path, 'r') as f:
            return json.load(f)

    def _get_random_age(self, age_distribution: Dict) -> int:
        """Generate a random age based on the country's age distribution."""
        ranges = []
        weights = []
        
        # Convert age ranges to actual age ranges
        for key, value in age_distribution.items():
            if '0-14' in key or '0-17' in key:
                ranges.append((0, 17))
                weights.append(float(value))
            elif '15-64' in key or '18-64' in key:
                ranges.append((18, 64))
                weights.append(float(value))
            elif '65_plus' in key:
                ranges.append((65, 90))
                weights.append(float(value))
        
        # Normalize weights
        total = sum(weights)
        weights = [w/total for w in weights]
        
        # Select age range and generate specific age
        selected_range = random.choices(ranges, weights=weights)[0]
        return random.randint(selected_range[0], selected_range[1])

    def _get_random_occupation(self, industry_distribution: Dict) -> str:
        """Generate random occupation based on industry distribution."""
        industries = list(industry_distribution.keys())
        weights = [float(industry_distribution[industry]) for industry in industries]
        
        # Normalize weights
        total = sum(weights)
        weights = [w/total for w in weights]
        
        # Select industry
        industry = random.choices(industries, weights=weights)[0]
        
        # Map industry to occupation list
        if industry == "industry":
            occupation_list = self.occupations.industry
        elif industry == "agriculture":
            occupation_list = self.occupations.agriculture
        elif industry == "manufacturing":
            occupation_list = self.occupations.manufacturing
        else:  # services
            occupation_list = self.occupations.services
        
        return random.choice(occupation_list)

    def _get_random_income_level(self, income_distribution: Dict) -> str:
        """Generate random income level based on country distribution."""
        levels = list(income_distribution.keys())
        weights = [float(income_distribution[level]) for level in levels]
        
        total = sum(weights)
        weights = [w/total for w in weights]
        
        return random.choices(levels, weights=weights)[0]

    def _get_random_city(self, top_cities: List[Dict]) -> str:
        """Generate random city, including 'other' for non-major cities."""
        total_major_city_percent = sum(city["percent_of_country"] for city in top_cities)
        cities = top_cities + [{"city": "other", "percent_of_country": 100 - total_major_city_percent}]
        
        weights = [float(city["percent_of_country"]) for city in cities]
        return random.choices([city["city"] for city in cities], weights=weights)[0]

    def generate_persona(self, country_data: Dict) -> str:
        """Generate a single persona description based on country data."""
        # Get random demographic information
        gender = random.choices(
            ["male", "female"],
            weights=[
                float(country_data["gender_distribution"]["male"]),
                float(country_data["gender_distribution"]["female"])
            ]
        )[0]
        
        age = self._get_random_age(country_data["age_distribution"])
        occupation = self._get_random_occupation(country_data["industry_of_work"])
        income_level = self._get_random_income_level(country_data["income_distribution"])
        city = self._get_random_city(country_data["top_cities"])
        
        # Get random personality traits
        personality = random.choice(self.traits.personality)
        financial_attitude = random.choice(self.traits.financial_attitudes)
        economic_concern = random.choice(self.traits.economic_concerns)
        
        # Pronouns
        pronoun = "he" if gender == "male" else "she"
        possessive = "his" if gender == "male" else "her"
        
        # Build the prompt
        prompt = (
            f"You are a {age}-year-old {gender} working as a {occupation} in {city}, {country_data['iso_code']}. "
            f"Living in a {country_data['political_regime']}, with a {income_level} economic background, "
            f"{pronoun} has a {personality} outlook on economic policies. {financial_attitude}, and {economic_concern}. "
            f"Working in the {occupation} field shapes {possessive} perspective on labor markets and tax policies. "
            f"The local currency ({country_data['currency']}) has a strength of {country_data['currency_strength_vs_usd']:.2f} vs USD, "
            f"and you face a top income tax rate of {country_data['tax_levels']['personal_income_tax_top_rate']}%. "
            f"Make decisions considering your economic circumstances, personal background, and the broader economic environment."
        )
        
        return prompt

    def generate_country_personas(self, country_code: str, num_personas: int = 100) -> List[str]:
        """Generate multiple personas for a specific country identified by its ISO code."""
        # Flexible lookup: allow direct key (if data is keyed by ISO), or match iso_code field
        # Normalize code for comparison
        if country_code in self.population_data:
            country_data = self.population_data[country_code]
        else:
            # try to find by matching the iso_code field inside the values
            matched = None
            for name, data in self.population_data.items():
                iso = data.get('iso_code') if isinstance(data, dict) else None
                if iso and str(iso).upper() == str(country_code).upper():
                    matched = data
                    break
            if matched is None:
                raise KeyError(f"Country with ISO code '{country_code}' not found in population data")
            country_data = matched

        return [self.generate_persona(country_data) for _ in range(num_personas)]