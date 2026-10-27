"""
setup_models.py
---------------
Model management utility for CodeAlpha AI Language Translator.
Downloads and installs Argos Translate neural models locally.
Provides installation progress, verification, and summary reports.
"""

import sys

# Force UTF-8 stdout for Windows command prompts
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from language_routes import REQUESTED_LANGUAGES

# Target bidirectional language pairs focusing on requested languages
PRIORITY_PAIRS = [
    ("en", "hi"), ("hi", "en"),
    ("en", "es"), ("es", "en"),
    ("en", "fr"), ("fr", "en"),
    ("en", "de"), ("de", "en"),
    ("en", "it"), ("it", "en"),
    ("en", "pt"), ("pt", "en"),
    ("en", "ru"), ("ru", "en"),
    ("en", "ar"), ("ar", "en"),
    ("en", "zh"), ("zh", "en"),
    ("en", "ja"), ("ja", "en"),
    ("en", "ko"), ("ko", "en"),
    ("en", "tr"), ("tr", "en"),
]


def check_installed_models():
    """Lists currently installed models."""
    try:
        import argostranslate.translate
        installed = argostranslate.translate.get_installed_languages()
        installed_pairs = []
        for lang in installed:
            for target in lang.translations_from:
                installed_pairs.append((lang.code, target.code))
        return installed_pairs
    except Exception:
        return []


def install_models(target_pairs=None):
    """
    Fetches official Argos package index and installs requested model pairs.
    Skips models that are already installed.
    """
    try:
        import argostranslate.package
        import argostranslate.translate
    except ImportError:
        print("[!] Error: 'argostranslate' is not installed in this environment.")
        print("    Please run: pip install -r requirements.txt")
        sys.exit(1)

    pairs_to_install = target_pairs or PRIORITY_PAIRS
    print("=" * 68)
    print("CodeAlpha AI Language Translator -- Offline Model Setup")
    print("=" * 68)
    print("1. Updating Argos package index (requires internet connection once)...")

    try:
        argostranslate.package.update_package_index()
        print("   [OK] Package index updated successfully.")
    except Exception as e:
        print(f"   [!] Warning: Could not reach package index: {e}")
        print("       If models are already installed locally, offline translation will continue to work.")

    available_packages = argostranslate.package.get_available_packages()
    installed_pairs = check_installed_models()

    print(f"\n2. Currently installed translation routes: {len(installed_pairs)}")
    for src, tgt in installed_pairs:
        print(f"   [+] {src.upper()} -> {tgt.upper()}")

    print(f"\n3. Evaluating {len(pairs_to_install)} target translation routes...")
    installed_count = 0

    for from_code, to_code in pairs_to_install:
        from_label = REQUESTED_LANGUAGES.get(from_code, from_code)
        to_label = REQUESTED_LANGUAGES.get(to_code, to_code)

        if (from_code, to_code) in installed_pairs:
            print(f"   [ALREADY INSTALLED] {from_label} -> {to_label} ({from_code.upper()} -> {to_code.upper()})")
            continue

        # Look for matching package
        matching_pkg = next(
            (pkg for pkg in available_packages if pkg.from_code == from_code and pkg.to_code == to_code),
            None
        )

        if matching_pkg:
            print(f"   -> Downloading & installing {from_label} -> {to_label} ({from_code.upper()} -> {to_code.upper()})...")
            try:
                download_path = matching_pkg.download()
                argostranslate.package.install_from_path(download_path)
                print(f"      [OK] Successfully installed {from_code.upper()} -> {to_code.upper()}")
                installed_count += 1
            except Exception as ex:
                print(f"      [X] Failed to install {from_code.upper()} -> {to_code.upper()}: {ex}")
        else:
            print(f"   [-] Model not found in repository for {from_code.upper()} -> {to_code.upper()}")

    print("\n4. Verifying installed models in memory...")
    refreshed_langs = argostranslate.translate.get_installed_languages()
    print(f"   Total functional language nodes loaded: {len(refreshed_langs)}")
    print("=" * 68)
    print(f"Setup complete! {installed_count} new models installed.")
    print("All translation routes are stored locally in user data directory.")
    print("You can now run 'streamlit run app.py' completely offline.")
    print("=" * 68)


if __name__ == "__main__":
    install_models()
