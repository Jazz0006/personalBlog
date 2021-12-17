# T3A3: A Personal Blog Web APP

This web app provides 2 major functions:

- Write bolgs and view blogs of other users
- Record the products a user has bought, log the price and the warrenty expire date.

This web app includes below pages:

| Page | Function |
|------|----------|
| user sign up | For a new user to register its account |
| user login   | Existing user to login |
| user detail | Display detailed information of a single user |
| blog index   | List of blogs that visible to the current user |
|single blog page | Display the full content of a blog |
|write a blog | For the current user to write a new blog or edit an old blog |
| list of items | Show all the items belongs to the current user |
| item detail | Show the detailed information of a single item |
| item input | Record a new item |

### The entity relationship diagram:

![ERD](.\docs\personalBlog_ERD.png)

### Validations:

| Table | Field | validation |
|-------|------------|-------|
| Users |password | Length > 6 |
|       |email | format of an email address |