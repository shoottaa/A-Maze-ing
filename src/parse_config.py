import sys
from typing import Any, Dict, Tuple


REQUIRED_KEYS = {
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
}


def parse_coords(raw: str, key: str) -> Tuple[int, int]:
    try:
        parts = raw.split(",")
        if len(parts) != 2:
            print(f"Error: bad format for {key}: '{raw}'")
            sys.exit(1)
        x = int(parts[0].strip())
        y = int(parts[1].strip())
    except ValueError:
        print(f"Error: {key} coords must be ints: '{raw}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error: failed to parse {key}: {e}")
        sys.exit(1)
    return (x, y)


def parse_bool(raw: str, key: str) -> bool:
    lowered = raw.strip().lower()
    if lowered in ("true", "1", "yes"):
        return True
    if lowered in ("false", "0", "no"):
        return False
    print(f"Error: bad bool for {key}: '{raw}'")
    sys.exit(1)
    return False


def parse_int(raw: str, key: str) -> int:
    try:
        val = int(raw.strip())
    except (ValueError, OverflowError):
        print(f"Error: {key} must be an int: '{raw}'")
        sys.exit(1)
    if val <= 0:
        print(f"Error: {key} must be > 0: {val}")
        sys.exit(1)
    return val


def validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    validated: Dict[str, Any] = {}

    validated["WIDTH"] = parse_int(config["WIDTH"], "WIDTH")
    validated["HEIGHT"] = parse_int(config["HEIGHT"], "HEIGHT")
    validated["ENTRY"] = parse_coords(config["ENTRY"], "ENTRY")
    validated["EXIT"] = parse_coords(config["EXIT"], "EXIT")
    out = config["OUTPUT_FILE"].strip()
    if not out:
        print("Error: OUTPUT_FILE is empty")
        sys.exit(1)
    validated["OUTPUT_FILE"] = out
    validated["PERFECT"] = parse_bool(config["PERFECT"], "PERFECT")

    w = validated["WIDTH"]
    h = validated["HEIGHT"]
    entry_x, entry_y = validated["ENTRY"]
    exit_x, exit_y = validated["EXIT"]

    if entry_x < 0 or entry_x >= w or entry_y < 0 or entry_y >= h:
        print(f"OOB! Entry: {entry_x},{entry_y} / Size: {w}x{h}")
        sys.exit(1)

    if exit_x < 0 or exit_x >= w or exit_y < 0 or exit_y >= h:
        print(f"OOB! Exit: {exit_x},{exit_y} / Size: {w}x{h}")
        sys.exit(1)

    if (entry_x, entry_y) == (exit_x, exit_y):
        print("Error: entry and exit are the same")
        sys.exit(1)

    for key, value in config.items():
        if key not in REQUIRED_KEYS:
            validated[key] = value

    return validated


def parse_config(file_path: str) -> Dict[str, Any]:
    config: Dict[str, str] = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith("#") or not line:
                    continue
                if "=" not in line:
                    print(f"Error: bad line: '{line}'")
                    sys.exit(1)
                key, _, value = line.partition("=")
                config[key.strip()] = value.strip()
    except Exception as e:
        print(f"Error: could not read '{file_path}': {e}")
        sys.exit(1)

    missing = REQUIRED_KEYS - config.keys()
    if missing:
        print(f"Error : missing keys : {', '.join(missing)}")
        sys.exit(1)

    return validate_config(config)
