"""
Additional runtime hook specifically for pandas warnings
Place this file as: hooks/rthook_pandas_warnings.py
"""
import warnings
import os
import sys


# Suppress pandas-specific warnings
def suppress_pandas_warnings():
    """Suppress pandas and related library warnings."""

    # Environment variables to suppress warnings
    os.environ['PYTHONWARNINGS'] = 'ignore'
    os.environ['PANDAS_PLOTTING_BACKEND'] = 'matplotlib'

    # Pandas-specific suppressions
    warnings.filterwarnings("ignore", message=".*pandas.*")
    warnings.filterwarnings("ignore", module="pandas")
    warnings.filterwarnings("ignore", category=FutureWarning, module="pandas")
    warnings.filterwarnings("ignore", category=DeprecationWarning, module="pandas")

    # NumPy warnings (pandas dependency)
    warnings.filterwarnings("ignore", module="numpy")
    warnings.filterwarnings("ignore", category=FutureWarning, module="numpy")

    # Suppress specific pandas warnings that commonly appear
    warnings.filterwarnings("ignore", message=".*DataFrame.applymap.*")
    warnings.filterwarnings("ignore", message=".*is_categorical_dtype.*")
    warnings.filterwarnings("ignore", message=".*is_datetime64tz_dtype.*")
    warnings.filterwarnings("ignore", message=".*downcasting.*")

    # SQLAlchemy warnings related to pandas
    warnings.filterwarnings("ignore", message=".*pandas.io.sql.*")
    warnings.filterwarnings("ignore", message=".*to_sql.*")

    # Suppress openpyxl warnings if present
    warnings.filterwarnings("ignore", module="openpyxl")

    # Suppress xlrd warnings
    warnings.filterwarnings("ignore", module="xlrd")


# Apply suppressions
suppress_pandas_warnings()

# Additional: Monkey patch pandas to prevent warnings
try:
    import pandas as pd

    # Disable specific pandas warnings
    pd.options.mode.chained_assignment = None
    pd.set_option('mode.chained_assignment', None)
except ImportError:
    pass