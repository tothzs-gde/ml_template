import yaml
import importlib
from typing import Any
from typing import Type


def _import_class(class_path: str) -> Type:
    module_name, class_name = class_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


def _instantiate_component(component_config: dict[str, Any]) -> Any:
    cls = _import_class(component_config["class"])
    params = component_config.get("params", {})

    for key, val in params.items():
        if isinstance(val, list) and key == "steps":
            new_steps = []
            for step_cfg in val:
                step_name = step_cfg["name"]
                step_obj = _instantiate_component(step_cfg)
                new_steps.append((step_name, step_obj))
            params[key] = new_steps

        elif isinstance(val, list) and key == "transformers":
            new_transformers = []
            for transformer_cfg in val:
                transformer_name = transformer_cfg["name"]
                transformer_obj = _instantiate_component(transformer_cfg)
                transformer_columns = transformer_cfg["columns"]
                new_transformers.append(
                    (transformer_name, transformer_obj, transformer_columns)
                )
            params[key] = new_transformers

        elif isinstance(val, dict) and "class" in val:
            params[key] = _instantiate_component(val)

    return cls(**params)


def load_config(path: str) -> dict[str, Any]:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_pipeline(pipeline_config: dict[str, Any]):
    return _instantiate_component(pipeline_config)


def load_search_params(search_params_config: dict[str, Any]):
    search_params = []
    for param_dict in search_params_config:
        new_param_dict = {}
        for key, val in param_dict.items():
            if isinstance(val, list):
                new_list = []
                for item in val:
                    if isinstance(item, dict) and "class" in item:
                        new_list.append(_instantiate_component(item))
                    else:
                        new_list.append(item)
                new_param_dict[key] = new_list
            else:
                new_param_dict[key] = val
        search_params.append(new_param_dict)
    return search_params