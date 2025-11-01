"""
Simulation module for running multi-agent experiments
"""

from typing import Dict, List, Optional
import asyncio
import functools
import logging
from pathlib import Path
from synthcast.simulation.nebius import NebiusAgent
from synthcast.population.persona_generator import PersonaGenerator
from synthcast.simulation.logger import setup_logging
from synthcast.simulation.results import save_simulation_results

class Simulation:
    def __init__(self, country_agent_counts: Dict[str, int], temperature: float = 0.7, model_name: str = "Qwen/Qwen2.5-Coder-7B-fast"):
        self.logger = setup_logging()
        self.logger.info(f"Initializing simulation with {sum(country_agent_counts.values())} total agents across {len(country_agent_counts)} countries")
        self.country_agent_counts = country_agent_counts
        self.temperature = temperature
        self.model_name = model_name
        self.agents = self._create_agents()

    def _create_agents(self):
        """Create agents for each country with their personas."""
        agents = []
        pg = PersonaGenerator()
        
        for country_code, count in self.country_agent_counts.items():
            self.logger.info(f"Creating {count} agents for country {country_code}")
            personas = pg.generate_country_personas(country_code, count)
            
            for persona_prompt in personas:
                agent = NebiusAgent(model_name=self.model_name)
                agents.append({
                    "persona": persona_prompt,
                    "agent": agent,
                    "temperature": self.temperature,
                    "country_code": country_code  # Add country code to track responses
                })
        
        return agents

    def ask_question(self, question: str, save_results: bool = True, base_path: Optional[str] = None) -> Dict[str, List[Dict]]:
        """
        Ask a question to all agents and collect their responses.
        
        Args:
            question: The question to ask
            save_results: Whether to save results to files by country
            
        Returns:
            Dict[str, List[Dict]]: Dictionary of responses by country code
        """
        results_by_country = {}
        self.logger.info(f"Asking question to {len(self.agents)} agents: {question}")
        instruction = (
            "You MUST answer with exactly one of the following (case-insensitive):\\n"
            "very likely\\n"
            "likely\\n"
            "unlikely\\n"
            "highly unlikely\\n\\n"
            "Return ONLY that phrase — no quotes, punctuation, explanation, or additional text. "
            "Base your answer only on your persona and the information provided."
        )

        def _normalize_internal(resp: str) -> str:
            if not resp:
                return "invalid_response"
            s = resp.lower().strip()
            options = ["very likely", "likely", "unlikely", "highly unlikely"]
            if s in options:
                return s
            if "very unlikely" in s:
                return "highly unlikely"
            for opt in options:
                if opt in s:
                    return opt
            if "likely" in s and "unlikely" not in s:
                return "likely"
            if "unlikely" in s:
                return "unlikely"
            if any(k in s for k in ("cannot", "unable", "do not know", "not able", "no information")):
                return "unlikely"
            return "invalid_response"

        async def _handle_agent(agent):
            persona_prompt = agent["persona"]
            llm_agent = agent["agent"]
            country_code = agent["country_code"]
            self.logger.debug(f"Getting response from agent with persona: {persona_prompt[:100]}...")

            async def _get_response(prompt_text):
                try:
                    return await llm_agent.generate_response_async(persona_prompt, prompt_text, temperature=agent["temperature"])
                except Exception as e:
                    return f"__NEBIUS_ERROR__: {e}"

            response = await _get_response(f"{question}\n{instruction}")
            normalized = _normalize_internal(response)
            attempts = 3
            attempt = 1
            while attempt <= attempts and normalized == "invalid_response":
                followup = (
                    f"Your previous answer was: \"{response}\"\n"
                    "That answer is not acceptable.\n"
                    "You MUST now reply with exactly one of (lowercase):\\n"
                    "very likely\\n"
                    "likely\\n"
                    "unlikely\\n"
                    "highly unlikely\\n\\n"
                    "Return ONLY that phrase and nothing else.\n"
                    "If you cannot decide, choose 'unlikely'."
                )
                response = await _get_response(f"{question}\n{instruction}\nFOLLOW-UP: {followup}")
                normalized = _normalize_internal(response)
                attempt += 1

            if normalized == "invalid_response":
                s = (response or "").lower()
                if any(k in s for k in ("cannot", "unable", "do not know", "no information", "not able")):
                    normalized = "unlikely"
                elif "very" in s and "likely" in s:
                    normalized = "very likely"
                elif "likely" in s:
                    normalized = "likely"
                elif "unlikely" in s:
                    normalized = "unlikely"
                else:
                    normalized = "unlikely"

            if country_code not in results_by_country:
                results_by_country[country_code] = []
            results_by_country[country_code].append({"persona": persona_prompt, "response": normalized})

        async def _gather():
            tasks = [asyncio.create_task(_handle_agent(a)) for a in self.agents]
            await asyncio.gather(*tasks)

        try:
            asyncio.run(_gather())
        except Exception:
            for agent in self.agents:
                persona_prompt = agent["persona"]
                llm_agent = agent["agent"]
                country_code = agent["country_code"]
                response = llm_agent.generate_response(persona_prompt, f"{question}\n{instruction}", temperature=agent["temperature"])
                normalized = _normalize_internal(response)
                if normalized == "invalid_response":
                    normalized = "unlikely"
                if country_code not in results_by_country:
                    results_by_country[country_code] = []
                results_by_country[country_code].append({"persona": persona_prompt, "response": normalized})
        
        # Save results by country if requested
        if save_results:
            for country_code, country_results in results_by_country.items():
                filepath = save_simulation_results(
                    results=country_results,
                    question=question,
                    country_code=country_code,
                    base_path=base_path
                )
                self.logger.info(f"Saved {len(country_results)} responses for {country_code} to {filepath}")
                # Also append an aggregated datapoint for this run
                # Build distribution counts
                distribution = {}
                for r in country_results:
                    key = r.get('response')
                    distribution[key] = distribution.get(key, 0) + 1
                try:
                    from synthcast.simulation.results import append_aggregated_datapoint
                    agg_path = append_aggregated_datapoint(
                        country_code=country_code,
                        num_agents=len(country_results),
                        question=question,
                        distribution=distribution,
                        base_path=base_path
                    )
                    self.logger.info(f"Appended aggregated datapoint for {country_code} to {agg_path}")
                except Exception as e:
                    self.logger.warning(f"Failed to append aggregated datapoint for {country_code}: {e}")
        
        self.logger.info(f"Collected responses for {len(results_by_country)} countries")
        return results_by_country