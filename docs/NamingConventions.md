# Fast API Naming Conventions

## Pythong Naming Convention

Sure, here's a table showing the standard naming conventions for Python code, based on `PEP 8``, the official style guide for Python:

| Type | Naming Convention | Example |
|---|---|---|
| Variable | Snake case | `my_variable` |
| Function | Snake case | `my_function()` |
| Class | Pascal case | `MyClass` |
| Constant | All uppercase with underscores | `MY_CONSTANT` |
| Module | Short, lowercase names. Can have underscores | `my_module.py` |
| Package | Short, lowercase names. Should not have underscores | `mypackage` |
| Method | Snake case | `my_method()` |
| Instance variable | Snake case (beginning with underscore if private) | `_my_instance_var` or `my_instance_var` |
| Global variable | Snake case | `my_global_var` |
| Factory function | (returns instance of a class) should be named like classes | `FactoryFunction()` |

## FastAPI Naming Convention

- FastAPI is a Python-based framework, so most of the general Python naming conventions apply

- However, FastAPI also uses `Pydantic` for data validation which pushes it's own conventions over Python convention

- So, following table shows `Python vs FastAPI Conventions`, highlighting the similarity & difference among the 2:

| Type | Python Naming Convention | Example | FastAPI Naming Convention | Example | Similar/Different |
|---|---|---|---|---|---|
| Variable | Snake case | `user_name` | Snake case | `user_name` | Similar |
| Function | Snake case | `def get_user():` | Snake case | `def get_user():` | Similar |
| Class | PascalCase | `class User:` | Snake case for Pydantic models, PascalCase otherwise | Pydantic model - `class user:`, Others - `class User:` | Different |
| Constant | All uppercase with underscores | `MAX_LIMIT` | All uppercase with underscores | `MAX_LIMIT` | Similar |
| Module | Short, lowercase names. Can have underscores | `user_model.py` | Short, lowercase names. Can have underscores | `user_model.py` | Similar |
| Package | Short, lowercase names. Should not have underscores | `mypackage` | Short, lowercase names. Should not have underscores | `mypackage` | Similar |
| Method | Snake case | `def get_user():` | Snake case | `def get_user():` | Similar |
| Instance Variable | Snake case (beginning with underscore if private) | `_user_name` | Snake case (beginning with underscore if private) | `_user_name` | Similar |
| Global Variable | Snake case | `total_users` | Snake case | `total_users` | Similar |
| Endpoint Parameters | N/A | N/A | Snake case | `@app.get("/users/{user_id}")` | N/A |
| Path Operations | N/A | N/A | Snake case | `@app.get("/get_users")` | N/A |
| Pydantic Model | N/A | N/A | PascalCase | `class UserModel:` | N/A |
| Pydantic Field | N/A | N/A | Snake case | `user_name: str` in a Pydantic model | N/A |

**Note** that endpoint parameters, path operations, Pydantic models and Pydantic fields are specific to FastAPI and don't have a corresponding Python convention.

## JSON Conventions for RestAPI

Sure, here's the updated table:

| Component | Convention | Example |
|:---------:|:----------:|:-------:|
| Resource Name | Plural form, lowercase | `/creditCards` |
| Path Parameters | Lowercase, represents resource identifier | `/creditCards/123` |
| Query Parameters | camelCase, used for filtering/sorting/field selection | `/creditCards?sortBy=cardType&order=desc` |
| Body Parameters | camelCase | `{ "cardHolderName": "John Doe", "cardNumber": "1234567812345678", "expiryDate": "12/24" }` |
| Headers | PascalCase (camelCase with first letter capitalized) | `{ "Content-Type": "application/json", "Authorization": "Bearer abc123" }` |

## Covenstion Issues

Let's summarize the naming convention for Application vs API:

- `RestAPI` - Primarily **camelCase**
- `FastAPI` - Primarily **snake_case**

By default, FastAPI api parameters are defined in snakecase & thus, reflected as is in API's breaking RestAPI naming convention

[Post for Better Explanation of the issue](https://medium.com/analytics-vidhya/camel-case-models-with-fast-api-and-pydantic-5a8acb6c0eee)

## Resolution
