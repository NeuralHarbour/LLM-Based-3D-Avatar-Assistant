using UnityEngine;
using WebSocketSharp;

public class WsClient : MonoBehaviour
{
    // Define an event for notifying other scripts when the server is busy
    public delegate void ServerBusyEventHandler();
    public static event ServerBusyEventHandler OnServerBusy;

    public delegate void MessageReceivedEventHandler(string message);
    public static event MessageReceivedEventHandler OnMessageReceived;

    WebSocket ws;
    private string input;

    private void Start()
    {
        Debug.Log("Client Started");
        ws = new WebSocket("ws://localhost:8080");
        ws.OnOpen += (sender, e) =>
        {
            Debug.Log("WebSocket connection opened to " + ((WebSocket)sender).Url);
        };
        ws.Connect();
        ws.OnMessage += HandleMessageReceived; // Set the callback function for message reception

    }

    private void HandleMessageReceived(object sender, MessageEventArgs e)
    {
        Debug.Log("Message Received from " + ((WebSocket)sender).Url + ", Data : " + e.Data);

        string messageFromServer = e.Data;
        Debug.Log("Message from Python: " + messageFromServer);

        OnMessageReceived?.Invoke(messageFromServer);

        if (messageFromServer == "Sorry I am Busy")
        {
            Debug.Log("Server is busy: ");
        }
    }

    private void Update()
    {
        if (ws == null)
        {
            return;
        }
    }

    public void SendInputToServer(string message)
    {
        if (ws != null && ws.ReadyState == WebSocketState.Open)
        {
            ws.Send(message);
            Debug.Log("Sent message to server: " + message);
        }
        else
        {
            Debug.Log("WebSocket connection is not open.");
        }
    }
}
