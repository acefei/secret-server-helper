# secret-server-helper
Python wrapper for Thycotic Secret Server API

### Install
git clone this repo, keep pip module up to date and run the following:
```
cd scripts/update_secrets
python3 -m pip install -U pip
python3 -m pip install .
```

### Usage
```
# Get a secret by id
secret-server-helper -u <secret server user> -p <secret server pass> -s <secret server url> -i <secret id>

# Get a field value for specific field name
secret-server-helper -u <secret server user> -p <secret server pass> -s <secret server url> -i <secret id> -f <secret field name>

# Update a secret field
secret-server-helper -u <secret server user> -p <secret server pass> -s <secret server url> -i <secret id> -f <secret field name> -v <new value>
```
