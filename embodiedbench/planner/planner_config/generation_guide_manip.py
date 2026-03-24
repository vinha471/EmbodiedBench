from embodiedbench.planner.planner_config.modular_generation_guide import build_generation_schema

VLM_ENABLED_MASK_MANIP = [True, True, True, True]
LLM_ENABLED_MASK_MANIP = [False, True, True, True]

vlm_generation_guide_manip = build_generation_schema(
    enabled_mask=VLM_ENABLED_MASK_MANIP,
    is_manipulation=True,
)

llm_generation_guide_manip = build_generation_schema(
    enabled_mask=LLM_ENABLED_MASK_MANIP,
    is_manipulation=True,
)
