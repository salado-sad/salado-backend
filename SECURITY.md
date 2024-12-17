## Password Storage Security

We prioritize the security of user data, especially passwords. To ensure this:

- **Password Hashing**: All passwords are hashed before being stored in our database. We **do not store plain-text passwords** under any circumstances.
- **Hashing Algorithm**: We use a robust cryptographic hashing algorithm (e.g., `bcrypt` or `Argon2`) that includes salting to protect against brute-force and dictionary attacks.
- **Best Practices**: Hashes are uniquely salted, and computationally expensive functions ensure password security even in the event of database compromise.

This approach helps protect user passwords against unauthorized access.
