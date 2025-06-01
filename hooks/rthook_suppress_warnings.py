"""
Runtime hook to suppress warnings in PyInstaller executable
"""
import warnings
import os

# Set environment variable
os.environ['PYTHONWARNINGS'] = 'ignore'

# Suppress all warning categories
warnings.filterwarnings("ignore")
warnings.simplefilter("ignore")

# Specific suppressions
for category in [UserWarning, DeprecationWarning, FutureWarning, 
                PendingDeprecationWarning, ImportWarning, ResourceWarning]:
    warnings.filterwarnings("ignore", category=category)

# Module-specific suppressions
for module in ['pkg_resources', 'setuptools', 'distutils', 'pandas', 'numpy', 'sqlalchemy']:
    warnings.filterwarnings("ignore", module=module)
