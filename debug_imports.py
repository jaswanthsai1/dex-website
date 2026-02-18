
import sys
import os

print("Debugging imports...")

try:
    import api
    print("✅ api imported successfully")
except Exception as e:
    print(f"❌ api import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    import token_manager
    print("✅ token_manager imported successfully")
except Exception as e:
    print(f"❌ token_manager import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    import byte
    print("✅ byte imported successfully")
except Exception as e:
    print(f"❌ byte import failed: {e}")
    import traceback
    traceback.print_exc()

try:
    import guest_generator
    print("✅ guest_generator imported successfully")
except Exception as e:
    print(f"❌ guest_generator import failed: {e}")
    import traceback
    traceback.print_exc()
