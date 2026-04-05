The environment of this project is managed by uv which prefers keeping environments local to the project folder.  
Unlike Conda, uv does not maintain a global registry of environments. It follows the "project-local" philosophy.

Try not to use `pip` to install dependencies, use `uv add` instead.