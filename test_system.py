"""
System Test Script for University Admissions Chatbot
Tests all components without requiring API keys
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

print("=" * 60)
print("UNIVERSITY ADMISSIONS CHATBOT - SYSTEM TEST")
print("=" * 60)
print()

# Test 1: Import all modules
print("[TEST 1] Importing modules...")
try:
    import config
    import utils
    import ingest
    import scaledown
    import gemini_client
    import app
    print("✅ All modules imported successfully")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

print()

# Test 2: Check configuration
print("[TEST 2] Checking configuration...")
try:
    errors = config.validate_config()
    if errors:
        print("⚠️  Configuration issues found:")
        for error in errors:
            print(f"   - {error}")
        print()
        print("Note: API key errors are expected if .env is not configured yet")
    else:
        print("✅ Configuration valid")
except Exception as e:
    print(f"❌ Configuration check failed: {e}")

print()

# Test 3: Check data files
print("[TEST 3] Checking data files...")
try:
    data_dir = config.COLLEGE_DATA_DIR
    if not data_dir.exists():
        print(f"❌ Data directory not found: {data_dir}")
    else:
        files = list(data_dir.glob('*.txt')) + list(data_dir.glob('*.pdf'))
        if files:
            print(f"✅ Found {len(files)} data files:")
            for f in files:
                print(f"   - {f.name}")
        else:
            print("⚠️  No data files found in college_data/")
except Exception as e:
    print(f"❌ Data file check failed: {e}")

print()

# Test 4: Test data ingestion (local files only)
print("[TEST 4] Testing data ingestion...")
try:
    result = ingest.load_local_data()
    if result['summary']['successful'] > 0:
        print(f"✅ Successfully loaded {result['summary']['successful']} files")
        total_chars = sum(len(f['content']) for f in result['files_data'].values())
        print(f"   Total content: {total_chars:,} characters")
    else:
        print("⚠️  No files loaded successfully")

    if result['errors']:
        print(f"⚠️  {len(result['errors'])} errors occurred:")
        for error in result['errors'][:3]:  # Show first 3 errors
            print(f"   - {error}")
except Exception as e:
    print(f"❌ Data ingestion test failed: {e}")

print()

# Test 5: Test Scaledown module (without API call)
print("[TEST 5] Testing Scaledown module...")
try:
    compressor = scaledown.ScaledownCompressor()
    is_configured = compressor.is_configured()

    if is_configured:
        print("✅ Scaledown API key configured")
    else:
        print("⚠️  Scaledown API key not configured")
        print("   Compression will fall back to uncompressed mode")
except Exception as e:
    print(f"❌ Scaledown test failed: {e}")

print()

# Test 6: Test Gemini module (without API call)
print("[TEST 6] Testing Gemini module...")
try:
    import os
    if os.getenv('GEMINI_API_KEY'):
        print("✅ Gemini API key configured")
    else:
        print("⚠️  Gemini API key not configured")
        print("   Set GEMINI_API_KEY in .env file")
except Exception as e:
    print(f"❌ Gemini test failed: {e}")

print()

# Test 7: Check frontend files
print("[TEST 7] Checking frontend files...")
try:
    frontend_dir = Path(__file__).parent / 'frontend'
    required_files = ['index.html', 'style.css', 'script.js']
    missing = []

    for file in required_files:
        if not (frontend_dir / file).exists():
            missing.append(file)

    if missing:
        print(f"❌ Missing frontend files: {', '.join(missing)}")
    else:
        print("✅ All frontend files present")
except Exception as e:
    print(f"❌ Frontend check failed: {e}")

print()

# Test 8: Check directory structure
print("[TEST 8] Checking directory structure...")
try:
    base_dir = Path(__file__).parent
    required_dirs = ['backend', 'frontend', 'college_data', 'cache', 'logs']
    missing_dirs = []

    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        if not dir_path.exists():
            missing_dirs.append(dir_name)
        else:
            # Try to create a test file to verify write permissions
            test_file = dir_path / '.test'
            try:
                test_file.touch()
                test_file.unlink()
            except:
                print(f"⚠️  Directory {dir_name} is not writable")

    if missing_dirs:
        print(f"❌ Missing directories: {', '.join(missing_dirs)}")
    else:
        print("✅ All directories present and writable")
except Exception as e:
    print(f"❌ Directory structure check failed: {e}")

print()

# Final Summary
print("=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print()
print("✅ = Passed")
print("⚠️  = Warning (not critical)")
print("❌ = Failed (requires attention)")
print()
print("Next Steps:")
print("1. If API keys show warnings, create .env from .env.example")
print("2. Add your GEMINI_API_KEY and SCALEDOWN_API_KEY")
print("3. Run: python backend/app.py (or use start.bat/start.sh)")
print("4. Open frontend/index.html in a web browser")
print()
print("=" * 60)
