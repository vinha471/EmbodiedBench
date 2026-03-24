from embodiedbench.planner.planner_config.modular_generation_guide import build_generation_schema

VLM_ENABLED_MASK = [True, True, True, True]
LLM_ENABLED_MASK = [False, True, True, True]

vlm_generation_guide = build_generation_schema(
    enabled_mask=VLM_ENABLED_MASK,
    is_manipulation=False,
)

llm_generation_guide = build_generation_schema(
    enabled_mask=LLM_ENABLED_MASK,
    is_manipulation=False,
)
