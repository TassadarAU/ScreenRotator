import subprocess
cmdpipe = subprocess.Popen("xinput --list | grep 'AT Translated' ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#xinput --list | grep 'AT Translated' 


#result = {}
for row in cmdpipe.stdout.readline():
    print row
    if '() ' in row:
        key, value = row.split('() ')
        result[key.strip(' .')] = value.strip()
#print result