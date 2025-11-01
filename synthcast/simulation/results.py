"""Utilities for saving and loading simulation results"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

def save_simulation_results(
    results: List[Dict],
    question: str,
    country_code: str,
    base_path: Optional[str] = None
) -> str:
    """
    Save simulation results to a JSON file with a unique timestamp.
    
    Args:
        results: List of agent responses
        question: The question that was asked
        country_code: The country code for the responses
        base_path: Optional base path for saving results. Defaults to synthcast/data/responses
        
    Returns:
        str: Path to the saved file
    """
    if base_path is None:
        base_path = str(Path(__file__).parent.parent / 'data' / 'responses')
    
    # Create responses directory if it doesn't exist
    Path(base_path).mkdir(parents=True, exist_ok=True)
    
    # Create unique timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create filename with timestamp and country code
    filename = f"{country_code}_{timestamp}.json"
    filepath = str(Path(base_path) / filename)
    
    # Prepare data structure
    data = {
        "timestamp": timestamp,
        "country_code": country_code,
        "question": question,
        "responses": results,
        "metadata": {
            "total_responses": len(results),
            "response_distribution": {}
        }
    }
    
    # Calculate response distribution
    for result in results:
        response = result["response"].lower().strip()
        data["metadata"]["response_distribution"][response] = \
            data["metadata"]["response_distribution"].get(response, 0) + 1
    
    # Save to file
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

    # Also append an aggregated datapoint for quick analysis across runs
    try:
        append_aggregated_datapoint(
            country_code=country_code,
            num_agents=len(results),
            question=question,
            distribution=data["metadata"]["response_distribution"],
            base_path=base_path,
        )
    except Exception:
        # Don't fail the main save if aggregation fails
        pass

    return filepath

def load_simulation_results(filepath: str) -> Dict:
    """
    Load simulation results from a JSON file.
    
    Args:
        filepath: Path to the results file
        
    Returns:
        Dict: The loaded results data
    """
    with open(filepath, 'r') as f:
        return json.load(f)

def list_country_results(country_code: str, base_path: Optional[str] = None) -> List[str]:
    """
    List all result files for a specific country.
    
    Args:
        country_code: The country code to search for
        base_path: Optional base path for results. Defaults to synthcast/data/responses
        
    Returns:
        List[str]: List of filepaths for the country's results
    """
    if base_path is None:
        base_path = str(Path(__file__).parent.parent / 'data' / 'responses')
    
    pattern = f"{country_code}_*.json"
    return sorted([str(p) for p in Path(base_path).glob(pattern)])


def append_aggregated_datapoint(
    country_code: str,
    num_agents: int,
    question: str,
    distribution: Dict[str, int],
    base_path: Optional[str] = None,
) -> str:
    """
    Append an aggregated datapoint for a run/question to a persistent JSONL file.

    Each line in the file is a JSON object with keys: timestamp, country_code,
    num_agents, question, distribution.

    Returns the filepath written to.
    """
    if base_path is None:
        base_path = str(Path(__file__).parent.parent / 'data' / 'responses')

    Path(base_path).mkdir(parents=True, exist_ok=True)
    # Keep an append-only JSONL for streaming and a cumulative JSON array file
    filepath = str(Path(base_path) / 'aggregated_runs.jsonl')
    cumulative_path = Path(base_path) / 'aggregated_runs.json'

    datapoint = {
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "country_code": country_code,
        "num_agents": num_agents,
        "question": question,
        "distribution": distribution,
    }

    # Append as a single JSON line
    with open(filepath, 'a') as f:
        f.write(json.dumps(datapoint) + "\n")

    # Also maintain a cumulative JSON file with an array of datapoints
    try:
        stats_path = Path(base_path) / 'aggregated_statistics.json'
        if stats_path.exists():
            try:
                with open(stats_path, 'r') as sf:
                    existing = json.load(sf)
                    if not isinstance(existing, list):
                        existing = []
            except Exception:
                existing = []
        else:
            existing = []

        existing.append(datapoint)

        # Write back the cumulative JSON file (pretty printed)
        with open(stats_path, 'w') as sf:
            json.dump(existing, sf, indent=2)
    except Exception:
        # don't fail on statistics write; the JSONL append already persisted
        pass

    # Also maintain a cumulative JSON file with an array of datapoints
    try:
        if cumulative_path.exists():
            try:
                with open(cumulative_path, 'r') as cf:
                    existing_cum = json.load(cf)
                    if not isinstance(existing_cum, list):
                        existing_cum = []
            except Exception:
                existing_cum = []
        else:
            existing_cum = []

        existing_cum.append(datapoint)

        with open(cumulative_path, 'w') as cf:
            json.dump(existing_cum, cf, indent=2)
    except Exception:
        # best-effort; don't interrupt main flow
        pass

    return filepath


def load_aggregated_datapoints(base_path: Optional[str] = None) -> List[Dict]:
    """Load all aggregated datapoints from the cumulative JSON file.

    This reads `aggregated_runs.json` which contains a JSON array of datapoints.
    If the file does not exist or is malformed, an empty list is returned.
    """
    if base_path is None:
        base_path = str(Path(__file__).parent.parent / 'data' / 'responses')
    filepath = Path(base_path) / 'aggregated_runs.json'
    if not filepath.exists():
        return []

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception:
        # fallthrough to return empty on any error
        pass

    return []