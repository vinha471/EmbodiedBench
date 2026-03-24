MANIPULATION_MODULE_ORDER = [
    "visual_state_description",
    "reasoning_and_reflection",
    "language_plan",
    "executable_plan",
]

MANIPULATION_MODULE_DEFS = {
    "visual_state_description": {
        "type": "string",
        "description": "Describe the color and shape of each object in the detection box in the numerical order in the image. Then provide the 3D coordinates of the objects chosen from input.",
    },
    "reasoning_and_reflection": {
        "type": "string",
        "description": "Reason about the overall plan that needs to be taken on the target objects, and reflect on the previous actions taken if available.",
    },
    "language_plan": {
        "type": "string",
        "description": "A list of natural language actions to achieve the user instruction. Each language action is started by the step number and the language action name.",
    },
    "executable_plan": {
        "type": "array",
        "description": "A list of discrete actions needed to achieve the user instruction, with each discrete action being a 7-dimensional discrete action.",
        "items": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "The 7-dimensional discrete action in the format of a list given by the prompt",
                }
            },
            "required": ["action"],
        },
    },
}

NAV_MODULE_ORDER = [
    "visual_state_description",
    "reasoning_and_reflection",
    "language_plan",
    "executable_plan",
]

NAV_MODULE_DEFS = {
    "visual_state_description": {
        "type": "string",
        "description": "Description of current state from the visual image",
    },
    "reasoning_and_reflection": {
        "type": "string",
        "description": "summarize the history of interactions and any available environmental feedback. Additionally, provide reasoning as to why the last action or plan failed and did not finish the task",
    },
    "language_plan": {
        "type": "string",
        "description": "The list of actions to achieve the user instruction. Each action is started by the step number and the action name",
    },
    "executable_plan": {
        "type": "array",
        "description": "A list of actions needed to achieve the user instruction, with each action having an action ID and a name. Do not output empty list.",
        "items": {
            "type": "object",
            "properties": {
                "action_id": {
                    "type": "integer",
                    "description": "The action ID to select from the available actions given by the prompt",
                },
                "action_name": {
                    "type": "string",
                    "description": "The name of the action",
                },
            },
            "required": ["action_id", "action_name"],
        },
    },
}


def _module_config(is_manipulation: bool):
    if is_manipulation:
        return MANIPULATION_MODULE_ORDER, MANIPULATION_MODULE_DEFS
    return NAV_MODULE_ORDER, NAV_MODULE_DEFS


def build_generation_schema(
    enabled_mask: list[bool],
    is_manipulation: bool = False,
):
    module_order, module_defs = _module_config(is_manipulation)

    if enabled_mask is None:
        raise ValueError("enabled_mask must be provided")
    if len(enabled_mask) != len(module_order):
        raise ValueError("enabled_mask length mismatch")
    if not all(isinstance(x, bool) for x in enabled_mask):
        raise TypeError("enabled_mask must contain bool values only")

    enabled_keys = [k for k, on in zip(module_order, enabled_mask) if on]
    if "executable_plan" not in enabled_keys:
        raise ValueError("executable_plan must stay enabled")

    return {
        "type": "object",
        "properties": {k: module_defs[k] for k in enabled_keys},
        "required": enabled_keys,
        "additionalProperties": False,
    }
