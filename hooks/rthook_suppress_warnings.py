import warnings
import os
import sys

# Suppress all warnings
os.environ['PYTHONWARNINGS'] = 'ignore'
warnings.filterwarnings("ignore")
warnings.simplefilter("ignore")

# Suppress specific warning categories
for category in [UserWarning, DeprecationWarning, FutureWarning, 
                PendingDeprecationWarning, ImportWarning, ResourceWarning]:
    warnings.filterwarnings("ignore", category=category)

# Redirect stderr to suppress remaining warnings
import io
sys.stderr = io.StringIO()
