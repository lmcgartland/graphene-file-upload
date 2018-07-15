## Running the django example

1.  Create a new virtual environment `python3 -m venv venv`
2.  Source the virtual environment `source venv/bin/activate`
3.  Install the requirements `pip install -r requirements.txt`
4.  Run the app `python3 manage.py runserver`

While the app is running, run the following curl command in another terminal,
and confirm that the app is printing the correct values, and returning the
correct result:

```bash
curl http://localhost:8000/graphql \
  -F operations='{"query": "mutation ($file: Upload) { myUpload(fileIn: $file) { ok }}", "variables": { "file": null }}' \
  -F map='{ "0": ["variables.file"]}' \
  -F 0=@requirements.txt
```
