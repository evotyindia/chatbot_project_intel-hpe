"""
Pre-Flight Check - Verifies system readiness before installation
No dependencies required for this check
"""

import os
import sys
from pathlib import Path

print("=" * 60)
print("UNIVERSITY ADMISSIONS CHATBOT - PRE-FLIGHT CHECK")
print("=" * 60)
print()

base_dir = Path(__file__).parent
checks_passed = 0
checks_failed = 0
warnings = 0

# Check 1: Python version
print("[1] Python Version Check...")
version = sys.version_info
if version.major >= 3 and version.minor >= 8:
    print(f"    OK - Python {version.major}.{version.minor}.{version.micro}")
    checks_passed += 1
else:
    print(f"    FAIL - Python {version.major}.{version.minor} (need 3.8+)")
    checks_failed += 1

# Check 2: Directory structure
print("\n[2] Directory Structure Check...")
required_dirs = {
    'backend': 'Backend Python files',
    'frontend': 'Frontend HTML/CSS/JS files',
    'college_data': 'University data files',
    'cache': 'Cache directory',
    'logs': 'Log directory'
}

all_dirs_ok = True
for dir_name, description in required_dirs.items():
    dir_path = base_dir / dir_name
    if dir_path.exists():
        print(f"    OK - {dir_name}/ ({description})")
    else:
        print(f"    FAIL - {dir_name}/ missing!")
        all_dirs_ok = False

if all_dirs_ok:
    checks_passed += 1
else:
    checks_failed += 1

# Check 3: Backend files
print("\n[3] Backend Files Check...")
backend_files = [
    'app.py', 'config.py', 'utils.py', 'ingest.py',
    'scaledown.py', 'gemini_client.py', 'requirements.txt'
]

all_backend_ok = True
for file in backend_files:
    file_path = base_dir / 'backend' / file
    if file_path.exists():
        size = file_path.stat().st_size
        print(f"    OK - {file} ({size:,} bytes)")
    else:
        print(f"    FAIL - {file} missing!")
        all_backend_ok = False

if all_backend_ok:
    checks_passed += 1
else:
    checks_failed += 1

# Check 4: Frontend files
print("\n[4] Frontend Files Check...")
frontend_files = ['index.html', 'style.css', 'script.js']

all_frontend_ok = True
for file in frontend_files:
    file_path = base_dir / 'frontend' / file
    if file_path.exists():
        size = file_path.stat().st_size
        print(f"    OK - {file} ({size:,} bytes)")
    else:
        print(f"    FAIL - {file} missing!")
        all_frontend_ok = False

if all_frontend_ok:
    checks_passed += 1
else:
    checks_failed += 1

# Check 5: Data files
print("\n[5] Data Files Check...")
data_files = list((base_dir / 'college_data').glob('*.txt')) + \
             list((base_dir / 'college_data').glob('*.pdf'))

if data_files:
    print(f"    OK - Found {len(data_files)} data files:")
    for file in data_files:
        size = file.stat().st_size
        print(f"         - {file.name} ({size:,} bytes)")
    checks_passed += 1
else:
    print("    WARNING - No data files found!")
    warnings += 1

# Check 6: Configuration files
print("\n[6] Configuration Files Check...")
if (base_dir / '.env.example').exists():
    print("    OK - .env.example exists")
else:
    print("    FAIL - .env.example missing!")
    checks_failed += 1

if (base_dir / '.env').exists():
    print("    OK - .env exists (configured)")
    checks_passed += 1
else:
    print("    WARNING - .env not found (needs setup)")
    print("         Create from .env.example and add API keys")
    warnings += 1

if (base_dir / '.gitignore').exists():
    print("    OK - .gitignore exists")
else:
    print("    WARNING - .gitignore missing")
    warnings += 1

# Check 7: README
print("\n[7] Documentation Check...")
if (base_dir / 'README.md').exists():
    print("    OK - README.md exists")
    checks_passed += 1
else:
    print("    WARNING - README.md missing")
    warnings += 1

# Check 8: Startup scripts
print("\n[8] Startup Scripts Check...")
if (base_dir / 'start.bat').exists():
    print("    OK - start.bat exists (Windows)")
else:
    print("    WARNING - start.bat missing")
    warnings += 1

if (base_dir / 'start.sh').exists():
    print("    OK - start.sh exists (Linux/Mac)")
else:
    print("    WARNING - start.sh missing")
    warnings += 1

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Checks Passed: {checks_passed}")
print(f"Checks Failed: {checks_failed}")
print(f"Warnings: {warnings}")
print()

if checks_failed > 0:
    print("STATUS: FAILED - Please fix the issues above")
    sys.exit(1)
elif warnings > 0:
    print("STATUS: READY WITH WARNINGS")
    print()
    print("NEXT STEPS:")
    print("1. Install dependencies:")
    print("   cd backend")
    print("   pip install -r requirements.txt")
    print()
    print("2. Create .env file:")
    print("   copy .env.example .env       (Windows)")
    print("   cp .env.example .env         (Linux/Mac)")
    print()
    print("3. Edit .env and add your API keys:")
    print("   - GEMINI_API_KEY")
    print("   - SCALEDOWN_API_KEY")
    print()
    print("4. Start the application:")
    print("   start.bat                    (Windows)")
    print("   ./start.sh                   (Linux/Mac)")
else:
    print("STATUS: ALL CHECKS PASSED!")
    print()
    print("The system appears to be ready.")
    print("Make sure you have:")
    print("1. Installed dependencies (pip install -r backend/requirements.txt)")
    print("2. Configured .env with your API keys")
    print("3. Run start.bat or start.sh to launch")

print()
print("=" * 60)
