using System;
using System.Collections;
using System.Text;
using Newtonsoft.Json;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.Networking;

public class ElevenlabsAPI : MonoBehaviour
{
    [SerializeField]
    private string _voiceId;
    [SerializeField]
    private string _apiKey;
    [SerializeField]
    private string _apiUrl = "https://api.elevenlabs.io";

    private AudioClip _audioClip;

    // If true, the audio will be streamed instead of downloaded
    // Unfortunately, Unity has some problems with streaming audio
    // but I left this option here in case you want to try it.
    public bool Streaming = true;

    [Range(0, 4)]
    public int LatencyOptimization;

    // This event is used to broadcast the received AudioClip
    public UnityEvent<AudioClip> AudioReceived;

    public ElevenlabsAPI(string apiKey, string voiceId)
    {
        _apiKey = apiKey;
        _voiceId = voiceId;
    }

    public void GetAudio(string text)
    {
        StartCoroutine(DoRequest(text));
    }

    IEnumerator DoRequest(string message)
    {
        var postData = new TextToSpeechRequest
        {
            text = message,
            model_id = "eleven_monolingual_v1"
        };

        // TODO: This could be easily exposed in the Unity inspector,
        // but I had no use for it in my work demo.
        var voiceSetting = new VoiceSettings
        {
            stability = 0,
            similarity_boost = 0,
            style = 0.5f,
            use_speaker_boost = true
        };
        postData.voice_settings = voiceSetting;
        var json = JsonConvert.SerializeObject(postData);
        var uH = new UploadHandlerRaw(Encoding.ASCII.GetBytes(json));
        var stream = (Streaming) ? "/stream" : "";
        var url = $"{_apiUrl}/v1/text-to-speech/{_voiceId}{stream}?optimize_streaming_latency={LatencyOptimization}";
        var request = UnityWebRequest.PostWwwForm(url, json);
        var downloadHandler = new DownloadHandlerAudioClip(url, AudioType.MPEG);
        if (Streaming)
        {
            downloadHandler.streamAudio = true;
        }
        request.uploadHandler = uH;
        request.downloadHandler = downloadHandler;
        request.SetRequestHeader("Content-Type", "application/json");
        request.SetRequestHeader("xi-api-key", _apiKey);
        request.SetRequestHeader("Accept", "audio/mpeg");
        yield return request.SendWebRequest();

        if (request.result != UnityWebRequest.Result.Success)
        {
            Debug.LogError("Error downloading audio: " + request.error);
            yield break;
        }
        AudioClip audioClip = downloadHandler.audioClip;
        AudioReceived.Invoke(audioClip);
        request.Dispose();
    }

    [Serializable]
    public class TextToSpeechRequest
    {
        public string text;
        public string model_id; // eleven_monolingual_v1
        public VoiceSettings voice_settings;
    }

    [Serializable]
    public class VoiceSettings
    {
        public int stability; // 0
        public int similarity_boost; // 0
        public float style; // 0.5
        public bool use_speaker_boost; // true
    }
}