"""
Run simulation and collect responses
"""

from synthcast.population.persona_generator import PersonaGenerator
from synthcast.simulation.simulation import Simulation
import logging
from synthcast.simulation.logger import setup_logging

if __name__ == "__main__":
    logger = setup_logging()
    
    # List all country codes from PersonaGenerator's population data
    logger.info("Loading population data and getting country codes")
    pg = PersonaGenerator()
    country_codes = [data["iso_code"] for data in pg.population_data.values()]
    print("Available country codes:")
    print(", ".join(country_codes))

    # Get user input for number of agents per country
    try:
        num_agents = int(input("Enter the number of agents per country: "))
        logger.info(f"User requested {num_agents} agents per country")
    except Exception as e:
        logger.warning(f"Invalid input received: {e}. Using 1 agent per country.")
        print("Invalid input. Using 1 agent per country.")
        num_agents = 1

    # Prepare simulation
    country_agent_counts = {code: num_agents for code in country_codes}
    logger.info("Creating simulation instance")
    sim = Simulation(country_agent_counts, temperature=0.7)

    # The question to ask
    question = "Will your country face significant domestic protests against globalization by 2030?"
    logger.info(f"Running simulation with question: {question}")
    results = sim.ask_question(question)

    # Print and log results
    logger.info("Simulation complete. Printing results.")
    for result in results:
        print("---")
        print(f"Persona: {result['persona']}")
        print(f"Response: {result['response']}")

    # Summary statistics
    response_counts = {}
    for result in results:
        response = result['response'].lower().strip()
        response_counts[response] = response_counts.get(response, 0) + 1
    
    logger.info("Response distribution:")
    for response, count in response_counts.items():
        percentage = (count / len(results)) * 100
        logger.info(f"{response}: {count} ({percentage:.1f}%)")