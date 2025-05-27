#Docker

### Activate virtual environment

Caveats:

- Ensure your in the directory containing the venv folder
- Ensure you have created the virtual environment to begin with using `python -m venv venv`

Then run the following:

```
source <venv folder>/bin/activate
```

or

```
source venv/bin/activate
```

document.querySelector to get element of specific class very str8 forward

vector operations and tradional data queries, one database

fast api for two way communciations AND real time database update

The main differences between @router and @app decorators in FastAPI are:

@app decorators
Direct binding: Routes are directly attached to the main FastAPI application instance
Global scope: All routes defined with @app are immediately available at the application level
Simple structure: Good for small applications with few routes

@router decorators
Modular organization: Routes are defined on APIRouter instances for better code organization
Prefix support: Can add URL prefixes when including the router in the app
Separation of concerns: Allows grouping related endpoints in separate files
Reusability: Routers can be included in multiple apps or with different prefixes

In your current setup:
SQL routes use @router.get() and are included with prefix /api/sql
Vector routes use @router.get() and are included with prefix /api/vector
This means your endpoints will be:
/api/sql/companies
/api/vector/search
etc.
