# Views

Views folder is made to add new views to Gendiff.

## Adding new view

To add new view you should create new module in views folder.
It's name will be collected by `cli` automatically.

Inside that module you have to add function called 'render', which will be used by renderer.

After you finished creating your view, add new view to VIEWS dictionary inside `views.__init__`.
