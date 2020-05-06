import requests
from io import BytesIO
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder


#CAPTURA UMA IMAGEM DA INTERNET
r = requests.get("https://spn14.meraki.com/stream/jpeg/snapshot/e9cb97094d5fba39VHOTgzMmE5OTFlMTA2OTRhOTRhYWYxNWRkODkzYzZkNjYwNDVmMWRkZmUwODBhYTA4OGIzN2EyZTljN2QxMmM3MIHssWvjCHt1UFy3VnIn9GRlP6fXWlSsMUiyOhFgoYkdz3ljMtjIKWCzoGa-xPZxPiWglGYcaZQVfXJkoy-fB0LUtN6TDJJZGeAgYMIeczMyRqDmocw22jtLZAOrmfCahm71wRjRyH2nAA-m496b4kR2yZ0F40dxNAw21ap8gzaO-dJoZDM6TJHikwv2gJdVpDVAU_SoSMI1Lrqw9QlK8DA")

print("Status: ", r.status_code)

image = Image.open(BytesIO(r.content))


#TRANSFERE PARA UM FILE
print(image.size, image.format, image.mode)
path = "./image" + image.format

#SALVA A IMAGEM
try:
    image.save(path, image.format)
except IOError:
    print("Cannot save image")



#POSTA NO WEBEX TEAMS
m = MultipartEncoder({'roomId': 'Y2lzY29zcGFyazovL3VzL1JPT00vMTZkNWEzYzUtYTcyMC0zMDlkLTg1NDAtZjZhNzJiNWU2Njhj',
                      'text': 'example attached',
                      'files': ('image' + image.format, open('image' + image.format, 'rb'),
                      'image/'+ image.format)})

r = requests.post('https://api.ciscospark.com/v1/messages', data=m,
                  headers={'Authorization': 'ZjZlM2YzMzctZmQ3ZC00OWRhLTgzODItMzIzODI3NTM3ZDY1NDllZTI1ZDItM2Ew_PF84_9f031aba-6be6-431f-9917-cb1f996f5b45',
                  'Content-Type': m.content_type})

