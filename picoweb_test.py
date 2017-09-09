import picoweb
import network
wlan=network.WLAN(network.STA_IF)
wlan=network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('see_dum', '0863219053')
while not wlan.isconnected():
  pass
print(wlan.ifconfig()[0])
 
app = picoweb.WebApp(__name__)
 
@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp) 
    yield from resp.awrite("Hello world from picoweb running on the ESP32")
 
app.run(debug=True, host = wlan.ifconfig()[0])