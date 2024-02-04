using UnityEngine;
using WebSocketSharp;

public class CamSetup : MonoBehaviour
{
    Integrity_Loader IL;
    WebSocket ws;
    bool isWebSocketConnected = false;

    void Start()
    {
        Debug.Log("STARTING CAMERA");
        IL = GameObject.FindGameObjectWithTag("waveform").GetComponent<Integrity_Loader>();

        // Don't connect to WebSocket here, connect only when IL becomes true
        if (IL != null)
        {
            Debug.Log("IL FOUND");
        }
        else
        {
            Debug.Log("IL NOT FOUND");
        }
    }

    void OnDestroy()
    {
        DisconnectFromWebSocket();
    }

    void Update()
    {
        // Check if IL becomes true during runtime
        if (IL != null && IL.End_Flag && !isWebSocketConnected)
        {
            Debug.Log("IL is now true, connecting to WebSocket");
            ConnectToWebSocket();
        }

        // Additional camera-related update code can be placed here if needed
    }

    void ConnectToWebSocket()
    {
        // Connect to WebSocket server
        ws = new WebSocket("ws://localhost:8765");
        ws.OnMessage += OnWebSocketMessage;
        ws.Connect();
        isWebSocketConnected = true;
    }

    void DisconnectFromWebSocket()
    {
        // Disconnect from WebSocket server
        if (ws != null && ws.IsAlive)
        {
            ws.Close();
        }
    }

    void OnWebSocketMessage(object sender, MessageEventArgs e)
    {
        waveform.UpdateReceivedData(e.Data);
    }
}
