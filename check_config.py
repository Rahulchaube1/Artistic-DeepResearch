try:
    print("Attempting to import Configuration...")
    from Artistic_DeepResearch.configuration import Configuration
    print("Success!")
except ImportError as e:
    print(f"Failed: {e}")
except Exception as e:
    print(f"Other Error: {e}")
