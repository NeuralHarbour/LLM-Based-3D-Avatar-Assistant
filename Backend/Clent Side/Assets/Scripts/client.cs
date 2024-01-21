using UnityEngine;
using WebSocketSharp;
using System.Collections;
using System.Net;
using UnityEngine.Networking;

public class WsClient : MonoBehaviour
{
    public delegate void ServerBusyEventHandler();
    public static event ServerBusyEventHandler OnServerBusy;

    public delegate void MessageReceivedEventHandler(string message);
    public static event MessageReceivedEventHandler OnMessageReceived;

    WebSocket ws;
    private string input;

    private const int maxRetryAttempts = 3;
    private int retryCount = 0;

    private bool isCheckingConnection = false;
    private bool isConnecting = false;

    public string country;

    [System.Serializable]
    public class CountryData
    {
        public string ip;
        public string country;
    }

    private void Start()
    {
        Debug.Log("Client Started");
        if (Application.internetReachability != NetworkReachability.NotReachable)
        {
            StartCoroutine("DetectCountry");
            StartWebSocketConnection();
            StartCoroutine(CheckConnectionStatusRoutine());
        }
        else
        {
            Debug.LogWarning("No active internet connection. Switching to offline mode.");
            StartCoroutine(AutoConnectRoutine());
        }
    }

    IEnumerator DetectCountry()
    {
        UnityWebRequest request = UnityWebRequest.Get("https://api.country.is");
        request.chunkedTransfer = false;
        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.ConnectionError || request.result == UnityWebRequest.Result.ProtocolError)
        {
            Debug.Log(request.error);
        }
        else
        {
            if (request.isDone)
            {
                string jsonResponse = request.downloadHandler.text.Trim();
                CountryData countryData = JsonUtility.FromJson<CountryData>(jsonResponse);
                country = countryData.country;
                string ipAddress = countryData.ip;
                Debug.Log("IP Address: " + ipAddress);

            }
        }
    }

    private IEnumerator AutoConnectRoutine()
    {
        while (true)
        {
            yield return new WaitForSeconds(5f);

            if (Application.internetReachability != NetworkReachability.NotReachable)
            {
                Debug.Log("Internet connection detected. Starting WebSocket connection.");
                StartWebSocketConnection();
                StartCoroutine(RetryConnectionRoutine());
                yield break;
            }
            else
            {
                Debug.LogWarning("No active internet connection. Retrying in 5 seconds...");
            }
        }
    }

    private IEnumerator RetryConnectionRoutine()
    {
        while (true)
        {
            yield return new WaitForSeconds(10f);

            if (!isConnecting && (ws == null || ws.ReadyState != WebSocketState.Open))
            {
                Debug.LogWarning("Attempting to reconnect...");

                StartWebSocketConnection();
            }
        }
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
            OnServerBusy?.Invoke();
        }
    }

    private void HandleError(object sender, ErrorEventArgs e)
    {
        Debug.LogError("WebSocket error: " + e.Message);

        if (e.Message.Contains("closed"))
        {
            Debug.LogWarning("WebSocket connection closed unexpectedly. Attempting to reconnect...");

            StartWebSocketConnection();
        }
    }

    private IEnumerator CheckConnectionStatusRoutine()
    {
        while (true)
        {
            yield return new WaitForSeconds(10f);

            if (!isCheckingConnection)
            {
                isCheckingConnection = true;
                CheckInternetConnection();
                isCheckingConnection = false;
            }
        }
    }

    private void CheckInternetConnection()
    {
        if (Application.internetReachability == NetworkReachability.NotReachable)
        {
            Debug.LogWarning("No active internet connection.");

            if (!isConnecting && retryCount < maxRetryAttempts)
            {
                retryCount++;
                Debug.LogWarning($"Retrying connection attempt {retryCount}...");
                StartWebSocketConnection();
            }
            else
            {
                Debug.LogWarning($"Exceeded maximum retry attempts ({maxRetryAttempts}). Switching to offline mode.");
            }
        }
        else
        {
            if (ws == null || ws.ReadyState != WebSocketState.Open)
            {
                retryCount = 0;
                Debug.Log("Back Online");
                StartWebSocketConnection();
            }
        }
    }

    private void StartWebSocketConnection()
    {
        isConnecting = true;

        if (ws != null)
        {
            ws.OnError -= HandleError; // Unsubscribe from the previous WebSocket error event
            ws.Close();
        }

        ws = new WebSocket("ws://localhost:8080");

        ws.OnOpen += (sender, e) =>
        {
            Debug.Log("WebSocket connection opened to " + ((WebSocket)sender).Url);
            isConnecting = false;
        };

        ws.OnMessage += HandleMessageReceived;
        ws.OnError += HandleError; // Subscribe to the WebSocket error event

        ws.Connect();
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
