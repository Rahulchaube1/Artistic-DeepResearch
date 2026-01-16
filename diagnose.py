import sys
import traceback
print(f"Python executable: {sys.executable}")
print(f"Python path: {sys.path}")

print("-" * 20)
print("Attempting to import Artistic_DeepResearch.configuration...")
try:
    import Artistic_DeepResearch.configuration
    print("SUCCESS: Artistic_DeepResearch.configuration imported")
except ImportError:
    traceback.print_exc()
except Exception:
    traceback.print_exc()

print("-" * 20)
print("Attempting to import Artistic_DeepResearch.utils...")
try:
    import Artistic_DeepResearch.utils
    print("SUCCESS: Artistic_DeepResearch.utils imported")
except ImportError:
    traceback.print_exc()
except Exception:
    traceback.print_exc()

print("-" * 20)
print("Attempting to import Artistic_DeepResearch.deep_researcher...")
try:
    import Artistic_DeepResearch.deep_researcher
    print("SUCCESS: Artistic_DeepResearch.deep_researcher imported")
except ImportError:
    traceback.print_exc()
except Exception:
    traceback.print_exc()
