"""
Example usage of the PersonaGenerator class.
"""

from pathlib import Path
from synthcast.spawner import PersonaGenerator

def main():
    # Initialize the persona generator
    generator = PersonaGenerator()
    
    # Create output directory
    output_dir = Path(__file__).parent.parent / 'data' / 'generated_personas'
    
    # Generate personas for all countries
    generator.save_personas(str(output_dir))
    
    # Generate personas for a specific country
    usa_personas = generator.generate_country_personas("United States", num_personas=100)
    print("\nExample persona for United States:")
    print(usa_personas[0])
    
    # Generate personas for multiple specific countries
    for country in ["Germany", "Japan", "China"]:
        personas = generator.generate_country_personas(country, num_personas=100)
        print(f"\nExample persona for {country}:")
        print(personas[0])

if __name__ == "__main__":
    main()