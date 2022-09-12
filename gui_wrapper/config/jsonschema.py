SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "robot_name": {"type": "string"},
            "dh": {
                "type": "object",
                "properties": {
                    "d": {"type": "array", "items": {"type": ["string", "number"]}},
                    "theta": {"type": "array", "items": {"type": ["string", "number"]}},
                    "a": {"type": "array", "items": {"type": ["string", "number"]}},
                    "alpha": {"type": "array", "items": {"type": ["string", "number"]}},
                },
                "required": ["d", "theta", "a", "alpha"],
            },
            "is_std": {"type": "boolean"},
            "is_rad": {"type": "boolean"},
            "is_revol": {"type": "array", "items": {"type": "boolean"}},
        },
        "required": ["robot_name", "dh", "is_std", "is_rad", "is_revol"],
    },
}
