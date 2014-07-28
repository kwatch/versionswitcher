

gae_home = prop('gae_home', '/usr/local/google_appengine')
python   = prop('python', 'python')

@recipe
@spices("-p port: server port (default 8080)")
def server(c, *args, **kwargs):
    """start dev_appserver.py"""
    port = kwargs.get('p', 8080)
    system(c%"$(python) $(gae_home)/dev_appserver.py --port=$(port) .")

@recipe
@spices("--cron: upload only 'cron.yaml'")
@spices("--index: upload only 'index.yaml'")
def upload(c, *args, **kwargs):
    """upload to appengine"""
    if kwargs.get('cron'):
        system(c%"$(python) $(gae_home)/appcfg.py update_cron .")
    elif kwargs.get('index'):
        system(c%"$(python) $(gae_home)/appcfg.py update_indexes .")
    else:
        system(c%"$(python) $(gae_home)/appcfg.py update .")


#|$ python /usr/local/google_appengine/appcfg.py update .
#|Application: versionswitcher; version: 4097.
#|Host: appengine.google.com
#|
#|Beginning update of app: versionswitcher, version: 4097
#|Scanning files on local disk.
#|Initiating update of app: versionswitcher, version: 4097
#|Email: kwatch@gmail.com
#|Password for kwatch@gmail.com: 
#|Cloning 18 static files.
#|Cloning 20 application files.
#|Uploading 21 files and blobs.
#|Uploaded 21 files and blobs
#|Precompilation starting.
#|Precompilation completed.
#|Deploying new version.
#|Checking if new version is ready to serve.
#|Will check again in 1 seconds.
#|Checking if new version is ready to serve.
#|Will check again in 2 seconds.
#|Checking if new version is ready to serve.
#|Will check again in 4 seconds.
#|Checking if new version is ready to serve.
#|Will check again in 8 seconds.
#|Checking if new version is ready to serve.
#|Will check again in 16 seconds.
#|Checking if new version is ready to serve.
#|Closing update: new version is ready to start serving.
#|Completed update of app: versionswitcher, version: 4097
