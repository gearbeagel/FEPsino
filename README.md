# FEPsino

The project is fully dockerized and can be built with the following command:
```bash
docker-compose up --build
```

from the project root directory.

To run the project next times use:
```bash
docker-compose up
```

backend works on port 8000 and frontend on port 5173.


## Example of .env file (create in the root of the project):

```bash
SECRET_KEY=your-secret-key

DB_HOST=db
DB_NAME=dbname
DB_USER=username
DB_PASS=userpass
```
