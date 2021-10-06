import os
import sys
import urllib
import json
import urllib.request
# constants, configure to match your environment

#DevOps_Logs/Analogic Portal/logs
HOST = 'http://localhost:9200'
INDEX = 'devops'
TYPE = 'portal'
IDNUMBER = 1
TMP_FILE_NAME = 'tmp.json'
# for supported formats, see apache tika - http://tika.apache.org/1.4/formats.html
INDEX_FILE_TYPES = ['html','pdf', 'doc', 'docx', 'xls', 'xlsx', 'xml', 'log']

def main():

    indexDirectory = input('Index entire directory [Y/n]: ')
        
    if not indexDirectory:
        indexDirectory = 'y'

    if indexDirectory.lower() == 'y':
        dir = input('Directory to index (relative to script): ')
        INDEX = input('Index: ')
        TYPE = input('Type: ')
        indexDir(dir)

    else:
        fname = input('File to index (relative to script): ')
        createIndexIfDoesntExist()
        indexFile(fname)

def indexFile(fname, ID):
    print ('\nIndexing ' + fname)
    createEncodedTempFile(fname)
    postFileToTheIndex(ID)
    os.remove(TMP_FILE_NAME)
    print ('\n-----------')

def indexDir(dir):

    print ('Indexing dir ' + dir)

    createIndexIfDoesntExist()
    ID = 1
    for path, dirs, files in os.walk(dir):
        for file in files:
            fname = os.path.join(path,file)

            base,extension = file.rsplit('.',1)

            if extension.lower() in INDEX_FILE_TYPES:
                indexFile(fname,ID)
                ID += 1

            else:
                'Skipping {}, not approved file type: {}'.format(fname, extension)

def postFileToTheIndex(ID):
    cmd = 'curl -XPUT "{}/{}/{}/{}" -H "Content-Type: application/json" -d @'.format(HOST,INDEX,TYPE,ID) + TMP_FILE_NAME
    print (cmd)
    os.system(cmd)
    

def createEncodedTempFile(fname):

    file64 = open(fname, "r",encoding='utf-8').read()

    print ('writing JSON with base64 encoded file to temp file {}'.format(TMP_FILE_NAME))
    print(fname)
    f = open(TMP_FILE_NAME, 'w')
    data = { 'file': file64, 'title': fname }
    json.dump(data, f) # dump json to tmp file
    f.close()


def createIndexIfDoesntExist():
    

    #class HeadRequest(urllib.Request):
    #    def get_method(self):
    #        return "HEAD"

    # check if type exists by sending HEAD request to index
    try:
        urllib.request.urlopen(HOST + '/' + INDEX + '/' + TYPE)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print ('Index doesnt exist, creating...')

            os.system('curl -X PUT "{}/{}/{}/_mapping" -d'.format(HOST,INDEX,TYPE) + ''' '{
                  "attachment" : {
                    "properties" : {
                      "file" : {
                        "type" : "attachment",
                        "fields" : {
                          "title" : { "store" : "yes" },
                          "file" : { "term_vector":"with_positions_offsets", "store":"yes" }
                        }
                      }
                    }
                  }
                }' ''')
        else:
            print( 'Failed to retrieve index with error code - %s.' %  e.code)

# kick off the main function when script loads
main()