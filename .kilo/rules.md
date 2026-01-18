# KILO PROJECT OVERRIDE: TINY TOOL PROTOCOL

## ARCHITECTURE OVERRIDE
**STATUS**: SINGLE_FILE_MODE
**GLOBAL_RULES_IGNORED**: [Modularization, ConfigSeparation, LoggingUtils]

## CONSTRAINTS
1. **Single File Policy**: All logic MUST be contained within `main.py`. Do not create `config.py`, `utils.py`, or `constants.py`.
2. **Dependency Ban**: Do not import `loggingutils`. Use standard `logging`.
3. **Config Ban**: Hardcode all constants (VERSION, APP_NAME, COSTS) directly into `main.py`.
4. **Type Hinting**: Use standard Python types. Do not over-engineer for Pylance if it complicates the single-file structure.

## REASONING
This project is a "Tiny Tool" meant for public distribution via `curl` or copy-paste. It must have zero external dependencies other than `boto3`.
