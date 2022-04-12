import requests
import subprocess
version = input("Enter Blaze Version ")
device = input("Enter Device Code Name ")
buildDate = input("Enter BuildDate ")
type = input("Vanilla or Gapps? ")
print()
def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

if __name__ == "__main__":
    file_id =input("Enter File ID ")
    destination = "Blaze-v%s-%s-%s-%s-OFFICIAL.zip"%(version,device,buildDate,type)
    download_file_from_google_drive(file_id, destination)
    print("Do You Want Upload Those Files")
    choice = input("Your Choice(yes/no) ")
    if choice == "yes":
        username=input("Enter Your SourceForge username ")
        subprocess.run("scp %s  %s@frs.sourceforge.net:/home/frs/project/projectblaze/%s/"%(destination,username,device), shell="True")
    else:
        print("Bye Bye")
    