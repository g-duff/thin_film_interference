# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

* Documentation for:
	* Fresnel functions.

* Support for both lists and numpy arrays to ellipsometer function.

### Changed

### Removed

### Fixed

## 0.0.1 - 2022-11-11

### Added

* Installation instructions for pip and wheel file.

### Changed

* Directory structure to better conform to the [src-layout](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#src-layout).
* Calculation from using ray angles in each layer to using wavevector components.

### Fixed

* Relative import paths throughout.

## v0.0.0 - 2022-10-23

### Added

* Function to calculate ellipsometry parameters Psi and Delta for arbitrary number of thin films on a semi-infinite substrate.
* Benchmark test against [Regress Pro](https://github.com/franko/regress-pro/tree/master/src).
