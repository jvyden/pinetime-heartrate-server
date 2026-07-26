window.addEventListener('load', function () {
  const heartRateElem = document.getElementById("heartrate");
  const websocketUrlElem = document.getElementById("websocket-url");

  let protocol = "ws:";

  if (location.protocol == "https:")
    protocol = "wss:";

  const websocketUrl = `${protocol}//${location.host}/`;
  websocketUrlElem.innerText = websocketUrl;

  const ws = new WebSocket(websocketUrl);

  ws.addEventListener("message", (event) => {
    heartRateElem.innerText = event.data + " BPM";
  });
});
