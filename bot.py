from pyrogram import Client

# api_id = <your-api-id>
# api_hash = <your-api-hash>
proxy = {"hostname": "127.0.0.1", "port":9050}
with open("../aloodak/report.txt", "r") as foo:
	caption = foo.read()
with Client("my_account", api_id, api_hash, proxy=proxy) as app : 
	app.send_photo("@aloodak",photo = "../aloodak/report.png", caption=caption)
