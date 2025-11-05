import argparse
import logging
import sys
from pathlib import Path 
import pandas as pd

def setup_log():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )