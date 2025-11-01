from synthcast.simulation.simulation import Simulation
from synthcast.spawner.persona_generator import PersonaGenerator

if __name__ == "__main__":
    # List all country codes from PersonaGenerator's population data
    pg = PersonaGenerator()
    country_codes = [data["iso_code"] for data in pg.population_data.values()]
    print("Available country codes:")
    print(", ".join(country_codes))

    # Get user input for number of agents per country
    try:
        num_agents = int(input("Enter the number of agents per country: "))
    except Exception:
        print("Invalid input. Using 1 agent per country.")
        num_agents = 1

    # Prepare simulation
    country_agent_counts = {code: num_agents for code in country_codes}
    sim = Simulation(country_agent_counts, temperature=0.7)

    # The question to ask
    question = "Will your country face significant domestic protests against globalization by 2030?"
    results = sim.ask_question(question)

    # Print results
    for result in results:
        print("---")
        print(f"Persona: {result['persona']}")
        print(f"Response: {result['response']}")
