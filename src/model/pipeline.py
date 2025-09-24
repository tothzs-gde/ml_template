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
        if key in ["transformers", "steps"]:
            params[key] = [(
                (item.get("name"), _instantiate_component(item), item.get("columns"))
                if item.get("columns")
                else (item.get("name"), _instantiate_component(item))
            ) for item in val]
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