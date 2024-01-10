# Changelog

## unreleased

### added
### changed
### removed

### added
- file picker now only shows .docx files
- typing improvements
- spellchecking

### changed
- code refactor

### removed
- setup to allow changing separator for final file

## 0.2.0
2024/01/06

### added
- save as .tsv button
- separate lint yml(flake8 black mypy) from test yml(pytest)
- cicd linux build artifact
- xml code coverage
- lint and build badges
- windows version

### changed
- fix make run executable path
- make run does not rebuild
- reenable cli interface by booting with '--cli' flag
- code refactor
- updated cicd steps versions to stable
- fix cicd depreciated option
- optimized linux build

### removed

## 0.1.0
2024/01/01

### added
- changelog
- versioning
- tk gui
- flake8 linting gh actions
- black formatting gh actions
- test badge on readme

### changed
- defaults to gui tk interface instead of cli
- build result packed into single file

### removed
- failing gh actions builds
- cli interface
