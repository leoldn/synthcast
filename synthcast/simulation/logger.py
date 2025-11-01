"""
Logging configuration for the simulation module
"""

import logging
from pathlib import Path
import datetime

def setup_logging(log_dir: str = None) -> logging.Logger:
    """
    Set up logging configuration for the simulation
    
    Args:
        log_dir: Directory to store log files. If None, uses 'logs' in current directory.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    if log_dir is None:
        log_dir = "logs"
    
    # Create logs directory if it doesn't exist
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    # Create timestamped log file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = Path(log_dir) / f"simulation_{timestamp}.log"
    
    # Configure logging
    logger = logging.getLogger("simulation")
    logger.setLevel(logging.INFO)
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger