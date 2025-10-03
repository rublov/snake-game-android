# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Android APK Build System**: Complete Docker + Buildozer setup for guaranteed APK builds
  - `main_android.py`: Android entry point with platform detection
  - `buildozer_production.spec`: Production-ready buildozer configuration
  - `Dockerfile.production`: Optimized Docker image for APK building
  - `build-apk.ps1`: PowerShell script for Windows APK builds
  - `build-apk.sh`: Bash script for Linux/Mac APK builds
  - `.github/workflows/build-apk-docker.yml`: GitHub Actions for automated APK builds

- **Documentation**: Comprehensive guides for APK building
  - `QUICKSTART.md`: Quick start guide (3 commands to APK)
  - `BUILD_APK_GUIDE.md`: Detailed APK build documentation
  - `APK_BUILD_SUMMARY.md`: Technical summary of build system

- **Kivy Support**: Full Kivy-based UI for Android
  - Touch input support
  - Native Android rendering
  - Optimized for mobile devices

### Changed

- **CI/CD Pipeline**: Added Docker-based APK build to GitHub Actions
- **README.md**: Updated with Android build instructions
- **Project Structure**: Reorganized for multi-platform support

### Fixed

- **All linter errors**: Fixed F821, F823, E501 errors in `snake_game.py`
- **MyPy type errors**: Resolved type checking issues in `create_splash.py`
- **PyGame CI issues**: Fixed initialization errors in headless CI environments
- **Pip installation**: Fixed `--user` flag conflicts in Docker virtualenv

## [1.0.0] - Previous Release

### Added

- Classic Snake gameplay
- Two modes: MAP (premium with obstacles) and MVP (free)
- Themes: Light and Dark
- Sound effects and background music
- Settings persistence
- Promo codes for MAP mode
- Time tracking during gameplay
- Visual mode indicator

### Desktop Features

- PyGame-based desktop version
- Keyboard controls
- Settings UI
- Profile system

---

## Version Numbering

- **Major** (X.0.0): Breaking changes, major new features
- **Minor** (0.X.0): New features, improvements
- **Patch** (0.0.X): Bug fixes, minor changes

---

## Links

- [Repository](https://github.com/rublov/snake-game-android)
- [Issues](https://github.com/rublov/snake-game-android/issues)
- [Releases](https://github.com/rublov/snake-game-android/releases)
