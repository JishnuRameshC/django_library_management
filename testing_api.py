import requests
import base64

url = "https://joj-text-to-speech.p.rapidapi.com/"

payload = {
	"input": { "text": "Mary and Samantha arrived at the bus station early but waited until noon for the bus." },
	"voice": {
		"languageCode": "en-US",
		"name": "en-US-News-L",
		"ssmlGender": "FEMALE"
	},
	"audioConfig": { "audioEncoding": "MP3" }
}

headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "8032b05005mshf883e9806120ae0p1bd0d2jsnec5e114af9ea",
	"X-RapidAPI-Host": "joj-text-to-speech.p.rapidapi.com"
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    # Decode the base64 audio content
    audio_content = base64.b64decode(response.json()['audioContent'])
    
    # Save the audio to a file
    with open("output.mp3", "wb") as audio_file:
        audio_file.write(audio_content)
    
    print("Audio saved as output.mp3")
else:
    print("Error:", response.text)
