import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import openai
# print(string)
# Set your OpenAI API key
openai.api_key = "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"
# Set up your API credentials
CLIENT_SECRETS_FILE = "C:\\Users\\teams\\Downloads\\client_secret_714872599520-4fu4u56gt21n95236q5vl9uimdm6vqii.apps.googleusercontent.com.json"

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


#Change name base on vidoe
Hostname = "Shawn Ryan"
Guestname = "Mark Zuck"

def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server()
    return googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def upload_video(youtube, file_path, title, description, category_id, privacy_status):
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': privacy_status
        }
    }

    media_file = os.path.abspath(file_path)
    videos_insert_request = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media_file
    )

    response = videos_insert_request.execute()
    print(f"Video '{response['snippet']['title']}' was successfully uploaded.")

    
    
    
def read_srt_file(file_path):
    words = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(2, len(lines), 4):
            line = lines[i].strip()
            #print(line)
            words.append(line)
    combined_string = ' '.join(words)
    return combined_string

# Main program
srt_file_path = r"C:\Users\teams\Untitled Folder\output.srt"  # Replace with your SRT file path
string = read_srt_file(srt_file_path)

    
    
    
    



def generate_title(prompt,Hostname,Guestname):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Create a clicbate youtube video title using podcast clips transcript. Make sound intresting"},
            {"role": "user", "content": prompt.lower()},
            {"role": "assistant", "content": "Host name = {}, Guest name{}".format(Hostname,Guestname)}
        ]
    )

    reply = response['choices'][0]['message']['content']
    return reply


def generate_description(prompt,Hostname,Guestname):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=150,
        messages=[
            {"role": "system", "content": "Create a video description using podcast clip transcript. Make it catchy"},
            {"role": "user", "content": prompt.lower()},
            {"role": "assistant", "content": "Host name = {}, Guest name{}".format(Hostname,Guestname)}
        ]
    )

    reply = response['choices'][0]['message']['content']
    return reply

# Example usage:
user_input = string
generated_title = generate_title(user_input,Hostname, Guestname)
generated_description = generate_description(user_input,"Shawn Ryan", "Mark Zuck")

print("\nGenerated Title:")
print(generated_title)

print("\nGenerated Description:")
print(generated_description)
    
    
    
    
def start_upload(file_path):
    service = get_authenticated_service()

    title = generated_title.split(":", 1)[1].strip() if ":" in generated_title else generated_title
    description = generated_description
    category_id = '22'  # See YouTube API documentation for category IDs
    privacy_status = 'private'  # 'private', 'public', or 'unlisted'

    upload_video(service, file_path, title, description, category_id, privacy_status)

# In[ ]:




