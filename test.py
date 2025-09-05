import yaml
import importlib


def import_class(class_path):
    module_name, class_name = class_path.rsplit('.', 1)
    return getattr(importlib.import_module(module_name), class_name)


def flatten_params(config, prefix=""):
    param_list = []

    for key, value in config.items():
        print(f"Working on {key=} with {value=}")
        full_key = f"{prefix}__{key}" if prefix else key

        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and "class" in item:
                    cls = import_class(item["class"])
                    instance = cls()
                    param_dict = {full_key: [instance]}

                    # Handle optional params
                    params = item.get("params", {})
                    for param_key, param_val in params.items():
                        param_dict[f"{full_key}__{param_key}"] = param_val if isinstance(param_val, list) else [param_val]

                    param_list.append(param_dict)

                else:
                    param_list.append({full_key: [item]})


        elif isinstance(value, dict) and "class" in value:
            cls = import_class(value["class"])
            base = {f"{prefix}__classifier": [cls()]}

            params = value.get("params", {})
            for param_key, param_val in params.items():
                base[f"{prefix}__classifier__{param_key}"] = param_val if isinstance(param_val, list) else [param_val]

            param_list.append(base)

        elif isinstance(value, dict):
            nested = flatten_params(value, prefix=full_key)
            param_list.extend(nested)

    return param_list


def load_search_parameters(config_path="search_config.yaml"):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    pipeline_config = config.get("pipeline", {})
    return flatten_params(pipeline_config)


def build_component(cfg):
    cls = import_class(cfg["class"])
    params = cfg.get("params", {}).copy()

    # Check for nested lists of components in any param (like 'steps' or 'transformers')
    for key, val in params.items():
        if isinstance(val, list) and all(isinstance(i, list) for i in val):
            # This looks like a list of tuples/lists like [(name, component_cfg), ...]
            built = []
            for item in val:
                # item: could be (name, component_cfg) or (name, component_cfg, extra)
                name = item[0]
                component_cfg = item[1]
                component = build_component(component_cfg)

                # If tuple has 3 elements, treat third as extra param (e.g., columns)
                if len(item) == 3:
                    built.append((name, component, item[2]))
                else:
                    built.append((name, component))
            params[key] = built

    return cls(**params)

def build_pipeline_from_yaml(path):
    import yaml
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    return build_component(config["pipeline"])



if __name__ == "__main__":
    pipeline = build_pipeline_from_yaml("hyper_tuning_config.yaml")
    print(pipeline)