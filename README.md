# Conf-thief
This Module will connect to Confluence's API using an access token, export to PDF, and download the Confluence documents that the target has access to.  It allows you to use a dictionary/keyword search file to search all files in the target Confluence for potentially sensitive data.  It will output exfiltrated PDFs to the ./loot directory
## Dependencies
`pip install atlassian-python-api`
## Usage
```
python3 conf_thief.py [-h] -c <TARGET URL> -u <Target Username> -p <API ACCESS TOKEN> -d <DICTIONARY FILE PATH>

arguments:
        -c <TARGET CONFLUENCE URL>, --url <TARGET CONFLUENCE URL>
                The URL of target Confluence account
        -u <TARGET CONFLUENCE ACCOUNT USERNAME>, --user <TARGET USERNAME>
                The username of target Confluence account
        -p <TARGET CONFLUENCE ACCOUNT API ACCESS TOKEN>, --accesstoken <TARGET CONFLUENCE ACCOUNT API ACCESS TOKEN>
                The API Access Token of target Confluence account
        -d <DICTIONARY FILE PATH>, --dict <DICTIONARY FILE PATH>
                Path to the dictionary file.
                You can use the provided dictionary, per example: "-d ./dictionaries/secrets-keywords.txt"

optional arguments:
        -h, --help
                show this help message and exit
```
## TODO
- Threading
