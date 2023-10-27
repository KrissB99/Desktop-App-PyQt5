# System Integrations - desktop application

**Excercise 2**

The task is to extend the program implemented in Excercise 1. in such a way that it includes:

- database support using a JDBC connection,
- a button for importing data from the database,
- a button to export data to the database,
- displaying additional text information inside the application about the number of new records found and the number of duplicates found, based on what the user currently sees

after reading data from a TXT/XML file or database, color it: 

- in red those records that are duplicates compared to what the user sees,
- in gray the others,
- in white those records that the user will modify inside the application (after changing any cell).


## File structure

Files folder contains sample files to use in the application.
Output files folder contains files generated in the application.

## Development

Install Python on your computer if you don't have it.

Create and activate virtual environment.

```shell
$ python -m venv .venv
$ source .venv/bin/activate
```

Install runtime and development dependencies.

```shell
$ pip install -r requirements.txt
```

Run 'main.py' to start application.

## Appearance of the application window

