# Templates and Examples

This folder contains **templates/boilerplate** notebooks and codes for this project and **examples** of tool usage.

Tool example files are self-contained examples with specific cases. These files shall be able to run on their own. Official example files usually confirm to this rule, but custom example files should also contain dummy data, db connection etc. if needed.

Template files contain generic, boilerplate codes which could be copied when writing a new function, module, or creating a new notebook experiment. These shall contain no specific functionality.

Meta templates are templates for the templates.

## Naming convention

### Folders

Folder names shall start with either "project", "meta" or with the name of the tool it relates to. All lower case letters and underscore (_) used instead of any whitespace. All folder names shall be suffixed with either "_examples" or "_templates".

### File names

Official tool example files shall have their original name. Source shall be noted in a their respective source.md file. Custom scripts/files shall have a descriptive name and also noted in the source.md file as custom/in-house.

## Folders

- **project_templates**: This folder contains the template notebooks and codes. For example a database connection, data cleaning, mlflow tracking server connection etc.

- **[tool]_examples**: These folders contain example codes either officially provided, or created by us. Each of these folders shall have a source.md file containing links to the original source of the example files online.

- **meta_templates**: This folder contains templates for the tepmplate folder.