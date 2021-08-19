# Conf-thief
This Module will connect to Confluence's API using an access token, export to PDF, and download the Confluence documents that the target has access to.  It allows you to use a dictionary/keyword search file to search all files in the target Confluence for potentially sensitive data.  It will output exfiltrated PDFs to the ./loot directory\
For detailed instructions, see my blog post [here](https://antman1p-30185.medium.com/stealing-all-of-the-confluence-things-94bd96a84dc0)
## Dependencies
`pip install requests`
## Usage
```
python3 conf_thief.py [-h] -c <TARGET URL> -u <Target Username> -p <API ACCESS TOKEN> -d <DICTIONARY FILE PATH> [-a] "<UA STRING>"


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
	-a "<DESIRED UA STRING>", --user-agent "<DESIRED UA STRING>"
		The User-Agent string you wish to send in the http request.
		You can use the latest chrome for MacOS for example: -a "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
		Default is "python-requests/2.25.1"

	-h, --help
		show this help message and exit
```
## TODO
- Threading
- Logging
- ~~Use actual pdf file names~~
- Map keyword searches to downloaded files
