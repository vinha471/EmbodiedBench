import json
import os
import numbers


def _is_numeric(value):
    return isinstance(value, numbers.Real) and not isinstance(value, bool)


def maybe_init_wandb(config, model_name, env_name, eval_set):
    wandb_entity = config.get("wandb_entity")
    if wandb_entity is None or wandb_entity == "":
        return None

    import wandb

    model_short = model_name.split("/")[-1]
    exp_name = config.get("exp_name") or "baseline"
    run_name = config.get("wandb_run_name") or f"{model_short}_{env_name}_{eval_set}_{exp_name}"
    group = config.get("wandb_group") or model_short
    project = config.get("wandb_project") or "embodiedbench-eval"

    wandb.init(
        project=project,
        entity=wandb_entity,
        name=run_name,
        group=group,
    )

    config_payload = {}
    try:
        for key, value in dict(config).items():
            if isinstance(value, (dict, list, str, int, float, bool)) or value is None:
                config_payload[key] = value
            else:
                config_payload[key] = str(value)
    except Exception:
        config_payload = {"config_str": str(config)}

    config_payload["wandb_env"] = env_name
    config_payload["wandb_eval_set"] = eval_set
    wandb.config.update(config_payload, allow_val_change=True)

    return wandb


def log_episode_metrics(wandb, step, episode_info, running_metrics=None):
    if wandb is None:
        return

    payload = {}
    for key, value in episode_info.items():
        if _is_numeric(value):
            payload[f"episode/{key}"] = value

    if running_metrics is not None:
        for key, value in running_metrics.items():
            if _is_numeric(value):
                payload[f"running/{key}"] = value

    if payload:
        wandb.log(payload, step=int(step))


def log_summary_metrics(wandb, results_dir, summary_file_candidates=("summary.json", "summary_all.json")):
    if wandb is None:
        return

    for filename in summary_file_candidates:
        summary_path = os.path.join(results_dir, filename)
        if not os.path.exists(summary_path):
            continue

        try:
            with open(summary_path, "r", encoding="utf-8") as f:
                summary = json.load(f)
        except Exception:
            continue

        payload = {}
        for key, value in summary.items():
            if _is_numeric(value):
                payload[f"summary/{key}"] = value

        if payload:
            wandb.log(payload)
        return


def finish_wandb(wandb):
    if wandb is not None:
        wandb.finish()
