using System.Collections;
using System.Collections.Generic;
using ReadSpeaker;
using UnityEngine;
using VoicevoxBridge;

public class Spchinstance : MonoBehaviour
{
    [SerializeField] VOICEVOX voicevox;


    public ElevenlabsAPI elevenlabs;


    string msg = "";
    string x = "";
    string final_message = "";
    public TTSSpeaker speaker_en;
    private bool shouldspeak;
    waveform wv;
    spch facialexpressions;
    int SpeakerId = 3;
    // Start is called before the first frame update
    void Start()
    {
        TTS.Init();
        wv = GameObject.FindGameObjectWithTag("waveform").GetComponent<waveform>();
        facialexpressions = GameObject.FindGameObjectWithTag("character").GetComponent<spch>();
    }


    // Update is called once per frame
    void Update()
    {

        if (shouldspeak) {
            x = wv.language;
            Debug.Log("LANGUAGE OF TTS : " + x);
            if (x == "en" || x == "te")
            {
                final_message = ApplySSMLTags(final_message);
                TTS.Say(final_message,speaker_en,TextType.SSML);
            }
            else if(x == "ja")
            {
                voicevox.PlayOneShot(SpeakerId, final_message);
            }
            else if(x == "zh")
            {
                elevenlabs.GetAudio(msg);
            }
            else if(x == "ru")
            {
                elevenlabs.GetAudio(msg);
            }
            else
            {
                TTS.SayAsync(msg, speaker_en);
            }
        }
        shouldspeak = false;
    }
    public void ReceiveMessage(string messageContent)
    {
        msg = messageContent;
        shouldspeak = true;
        if (msg.StartsWith("AI:"))
        {
            Debug.Log("MESSAGE STARTS WITH AI:");
            final_message = msg.Substring(3).Trim();
        }
        else
        {
            final_message = messageContent;
        }
        Debug.Log("MESSAGE RECIEVED IN INSTANCE : "+final_message);
    }

    string ApplySSMLTags(string text)
    {
        // Define SSML tags for emotions
        Dictionary<string, string> emotionTags = new Dictionary<string, string>
        {
            {"['surprise']", "<prosody pitch='high' contour='surprise' volume='soft' rate='slow'>"},
            {"['joy']", "<prosody pitch='medium' contour='falling' volume='medium' rate='medium'>"},
            {"['fear']", "<prosody pitch='low' contour='rising' volume='medium' rate='medium'>"},
            {"['sadness']", "<prosody pitch='low' contour='falling' volume='soft' rate='slow'>"},
            {"['shame']", "<prosody pitch='medium' contour='falling' volume='soft' rate='medium'>"},
            {"['anger']", "<prosody pitch='high' contour='rising' volume='loud' rate='slow'>"},
            {"['neutral']", "<prosody volume='medium'>"}
        };


        // Iterate through emotion tags and apply SSML tags
        foreach (var emotionTag in emotionTags)
        {
            if (text.Contains(emotionTag.Key))
            {
                text = text.Replace(emotionTag.Key, emotionTag.Value);
                TriggerFacialExpression(emotionTag.Key);
            }
        }

        // Add closing tags
        text += "</prosody>";

        return text;
    }

    void TriggerFacialExpression(string emotion)
    {
        switch (emotion)
        {
            case "['joy']":
                facialexpressions.PlayHappyExpression();
                break;
            case "['sadness']":
                facialexpressions.PlaySadExpression();
                break;
            case "['anger']":
                facialexpressions.PlayAngryExpression();
                break;
            case "['surprise']":
                facialexpressions.PlaySurprisedExpression();
                break;
            default:
                facialexpressions.PlayNeutralExpression();
                break;
        }
    }


}
