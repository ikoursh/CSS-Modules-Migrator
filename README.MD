CSS to CSS Modules Migrator
=====
A quick and dirty script to assist with migrating css to css modules.

**Note: This is a badly written poorly made script to help with the migration. It will not replace manual work, only minimise it.**

IMPORTANT
====
This script accepts html and does not support react files out of the box. If you want to input a react js or ts file please copy paste the jsx inside the return statement to a new file and pass that as an argument.

Help
----
```
usage: main.py [-h] [-js JS] [-css CSS] [-sufix SUFIX]

Migrate CSS to CSS Modals

optional arguments:
  -h, --help    show this help message and exit
  -js JS        js or ts react file (default: None)
  -css CSS      Css file (default: None)
  -sufix SUFIX  What to append to converted styles (default: )
```
Known Bugs
-----
1. Sometimes misidentifies class names to convert
2. Cannot properly handle special characters like > when used in tag declaration
