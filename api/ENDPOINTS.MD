# Creating an account

curl https://api.lookout.network/register \
-H "Content-Type: application/json" \
-d '{"username": "admin", "password": "admin", "email": "admin@lookout.network"}'

## Responses
* 401 (Invalid parameters passed. Required: username, email, password)
* 500 (Logged exception)
* 201 (Registration Successful)

# Logging into account

curl https://api.lookout.network/login \
-H "Content-Type: application/json" \
-d '{"username": "admin", "password": "admin"}'

## Responses
* 401 (Invalid Login Details)
* 200 (Successful Login. Returns Auth Token)

