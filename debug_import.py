import traceback
import sys
import os

sys.path.append(os.path.join(os.getcwd(), "src"))

try:
    print("Importing Artistic_DeepResearch.deep_researcher...")
    import Artistic_DeepResearch.deep_researcher
    print("Import successful!")
except Exception:
    print("Caught Exception!")
    traceback.print_exc()
except SystemExit:
    print("Caught SystemExit!")
except:
    print("Caught Unknown Error!")
    traceback.print_exc()
