using UnityEngine;
using ReadSpeaker;

public class TTS_Readspeaker_ : MonoBehaviour
{
    public TTSSpeaker speaker; // Reference to the TTS speaker
    private Langchain_control lc;    // Reference to the TextManager
    private string currentMsg; // Stores the latest message to be spoken
    private string lastMsg;    // Tracks the previous message to detect changes

    void Start()
    {
        // Initialize TTS system
        TTS.Init();
        lc = FindObjectOfType<Langchain_control>();

        if (lc == null)
        {
            Debug.LogError("TextManager not found!");
        }

        lastMsg = string.Empty;
    }

    void Update()
    {
        // Continuously check for new messages
        GetCurrentText();

        // If there's a new message, speak it
        if (!string.IsNullOrEmpty(currentMsg) && currentMsg != lastMsg)
        {
            Debug.Log("New Message Obtained: " + currentMsg);
            TTS.Say(currentMsg, speaker);

            // Update the last message to avoid repeating the same message
            lastMsg = currentMsg;
        }
    }

    private void GetCurrentText()
    {
        if (lc != null)
        {
            currentMsg = lc.response;
        }
    }
}