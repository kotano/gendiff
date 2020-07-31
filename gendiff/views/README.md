# Views

Views folder is made to add new views to Gendiff.

## Adding new view

To add new view you should create new module in views folder.
It's name will be collected by `cli` automatically.

Inside that module you have to add function called 'modulename + _view', i.e. `plain_view` for plain module.

After you finished creating your view, add corresponding code to views.\_\_init__.render function.
