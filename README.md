
## Graph app - create and visualization graphs.

## Installing

### Local

Firstly you must be sure that you have python3.5.

1.  Download project from gitlab to your local machine:

```sh
git clone https://github.com/barbarossa92/graph_app.git
```

2. Install all dependencies to your virtual enviroment:

```sh
pip install -r requirements.txt
```
3. Run migration command (this command will create graph_db.sqlite3 database in project root folder):

```sh
./manage.py migrate
```

## Test

For test import graph xml file (create) you can use xml files from 'test_cases' folder.