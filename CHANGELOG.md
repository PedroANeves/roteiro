# Changelog

## unreleased

### added
### changed
### removed

## 0.2.2
2024/01/10

### added
- saving csv using cli interface

### changed
- fixed csv file encoding on windows

### removed

## 0.2.1
2024/01/09

### added
- file picker now only shows .docx files
- develop branch
- typing improvements
- spellchecking

### changed
- changed final file extension to csv, still tab separated
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
