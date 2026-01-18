import sys
from pathlib import Path
import config

# Setup loggingutils path
# loggingutils is at D:\Documents\PYTHON\loggingutils
# Project is at D:\Documents\PYTHON\AWS_Waste_Killer
# We add parent directory to sys.path to access it
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from loggingutils import logger
except ImportError:
    # Fallback if loggingutils is not found during initial setup
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

def main():
    logger.info(f"Starting {config.APP_NAME} v{config.VERSION}")
    
    # Logic will go here
    
    logger.info("Task completed.")

if __name__ == "__main__":
    main()
