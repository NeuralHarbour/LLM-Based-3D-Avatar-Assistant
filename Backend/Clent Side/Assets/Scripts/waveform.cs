using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Audio;
using System.Net.Sockets;
using System.IO;
using UnityEngine.UI;
using System;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Text.RegularExpressions;
using WebSocketSharp;

[RequireComponent(typeof(AudioSource))]
public class waveform : MonoBehaviour
{
    WsClient wx;
    Wavcon wv;
    Emitter e;
    spch speech;
    AudioSource _audioSource;

    public int activeCharacterIndex = 0;

    public AudioSource Button;
    public AudioSource loop;
    public AudioSource ButtonRel;
    public AudioClip _audioClip;
    public AudioClip Buttonpress;
    public AudioClip ButtonRelease;
    public AudioClip loopedSound;

    public static float[] _samples = new float[512];
    public static float[] _freqBand = new float[8];
    public static float[] _bandBuffer = new float[8];
    public static float[] _bufferDecrease = new float[8];
    public float voiceDetectionThreshold;
    float[] _freqBandHighest = new float[8];
    public static float[] _audioBand = new float[8];
    public static float[] _audioBandBuffer = new float[8];
    public static float _Amplitude, _AmplitudeBuffer;
    public float _audioProfile;
    float _AmplitudeHighest;
    public float cooldownDuration = 10.0f;
    private float cooldownTimer = 0f;
    float animationDuration = 3.17f;

    [SerializeField] private KeyCode pushToTalkKey = KeyCode.Space;

    //microphone
    public string _selectedDevice;
    public AudioMixerGroup _mixerGroupMicrophone, _mixerGroupMaster;

    private byte[] bytes;

    public Text displayText;
    public Text displayText2;

    Color customColor = new Color(0.2f, 0.7f, 0.4f, 1.0f);
    string message = "";
    string msg = "";

    public bool _useMicrophone;
    private bool isRecording = false;
    private bool responseReceived = false;
    private bool waitingForResponse = false;
    private bool isLooping = false;
    private bool isbusy = false;
    public bool isWakeWordDetected = false;
    private bool hasPlayed = false;
    private bool isCooldown = false;
    bool isCharacterActive = false;

    private readonly object responseLock = new object();
    private readonly object busyLock = new object();
    public GameObject AudioReact;
    public GameObject[] characters = new GameObject[] { };

    public Animator anim;

    public ParticleSystem particles;
    public ParticleSystem Entryparticles;
    public ParticleSystem Surroundparticles;
    private bool haschangedoutfit = false;


    // Start is called before the first frame update
    void Start()
    {
        wv = GameObject.FindGameObjectWithTag("Middleware").GetComponent<Wavcon>();
        wx = GameObject.FindGameObjectWithTag("Middleware").GetComponent<WsClient>();
        e = GameObject.FindGameObjectWithTag("Middleware").GetComponent<Emitter>();
        speech = GameObject.FindGameObjectWithTag("character").GetComponent<spch>();
        if (speech == null)
        {
            Debug.Log("spch script not found on the GameObject with tag 'character'. Make sure the tag and script are set up correctly.");
        }
        else
        {
            Debug.Log("FOUND !!!!!!!");
        }
        if (AudioReact != null)
        {
            AudioReact.SetActive(false);
        }
        InitializeAudioSource();
        displayText.gameObject.SetActive(false);
        displayText2.gameObject.SetActive(false);
        e.StopEffect();
    }

    private void InitializeAudioSource()
    {
        _audioSource = GetComponent<AudioSource>();
        AudioProfile(_audioProfile);

        if (_useMicrophone)
        {
            if (Microphone.devices.Length > 0)
            {
                _selectedDevice = Microphone.devices[0].ToString();
                _audioSource.outputAudioMixerGroup = _mixerGroupMicrophone;
            }
            else
            {
                _useMicrophone = false;
                _audioSource.outputAudioMixerGroup = _mixerGroupMaster;
            }
        }
        else
        {
            _audioSource.outputAudioMixerGroup = _mixerGroupMaster;
            _audioSource.clip = _audioClip;
        }
    }

    private void StartRecording()
    {
        if (_useMicrophone && !_audioSource.isPlaying)
        {
            _audioSource.clip = Microphone.Start(_selectedDevice, false, 10, AudioSettings.outputSampleRate);
            _audioSource.Play();
            isRecording = true;
        }
    }

    private void StopRecording()
    {
        if (isRecording)
        {
            Microphone.End(_selectedDevice);
            var position = Microphone.GetPosition(_selectedDevice);
            float[] samples = new float[_audioSource.clip.samples * _audioSource.clip.channels];
            _audioSource.clip.GetData(samples, 0);
            bytes = EncodeAsWAV(samples, _audioSource.clip.frequency, _audioSource.clip.channels);
            isRecording = false;
            SendRecording(bytes);
        }
    }

    void AudioProfile(float audioProfile)
    {
        for (int i = 0; i < 8; i++)
        {
            _freqBandHighest[i] = audioProfile;
        }
    }

    void BandBuffer()
    {
        for (int g = 0; g < 8; ++g)
        {
            if (_freqBand[g] > _bandBuffer[g])
            {
                _bandBuffer[g] = _freqBand[g];
                _bufferDecrease[g] = 0.005f;
            }
            if (_freqBand[g] < _bandBuffer[g])
            {
                _bandBuffer[g] -= _bufferDecrease[g];
                _bufferDecrease[g] *= 1.2f;
            }
        }
    }

    IEnumerator ChangeOutfitWithAnimation()
    {
        // Play the transition animation before changing characters
        anim = characters[activeCharacterIndex].GetComponent<Animator>();
        if (anim != null)
        {
            // Replace "ischanging" with the actual trigger name in your animator controller
            anim.SetTrigger("ischanging");

            yield return new WaitForSeconds(animationDuration / 2f);

            // Get the normalized time of the current animation
            float normalizedTime = 0f;
            AnimatorStateInfo stateInfo = anim.GetCurrentAnimatorStateInfo(0);
            if (stateInfo.length > 0)
            {
                normalizedTime = stateInfo.normalizedTime;
            }

            // Disable the current character at this halfway point
            characters[activeCharacterIndex].SetActive(false);

            // Change to the next character at the halfway point
            activeCharacterIndex = (activeCharacterIndex + 1) % characters.Length;
            characters[activeCharacterIndex].SetActive(true);

            // Update the active animator in speech script
            anim = characters[activeCharacterIndex].GetComponent<Animator>();
            speech.UpdateActiveAnimator(anim, characters[activeCharacterIndex]);

            // Apply the normalized time to the new character's animation
            if (anim != null)
            {
                anim.Play(stateInfo.fullPathHash, 0, normalizedTime);
            }
        }

        // Wait for the remaining half of the animation duration
        yield return new WaitForSeconds(animationDuration / 2f);

        // Reset the flag
        haschangedoutfit = false;
    }




    // Update is called once per frame
    void Update()
    {
        GetSpectrumAudioSource();
        MakeFrequencyBands();
        BandBuffer();
        createAudioBands();
        GetAmplitude();
        if (isWakeWordDetected)
        {
            e.showEmission();
            if (characters.Length > 0)
            {
                characters[activeCharacterIndex].SetActive(true);
            }
            if (haschangedoutfit)
            {
                StartCoroutine(ChangeOutfitWithAnimation());
                haschangedoutfit = false;
            }
            if (!hasPlayed)
            {
                anim.Play("Entry");
                speech.StartVisualEffect();
                hasPlayed = true;
            }
            else
            {
                speech.StopVisualEffectAtAnimationEnd();
                if (!Entryparticles.isPlaying && anim.GetCurrentAnimatorStateInfo(0).IsName("Entry"))
                {
                    Entryparticles.Play();
                    Surroundparticles.Play();
                }
                else if (Entryparticles.isPlaying && !anim.GetCurrentAnimatorStateInfo(0).IsName("Entry"))
                {
                    Entryparticles.Stop();
                    Surroundparticles.Stop();
                }
            }
            if (Input.GetKeyDown(pushToTalkKey) && !isCooldown)
            {
                Debug.Log("Push");
                StartRecording();
                wv.ShowTalkingImage();
                wv.ShowCubes();
                wv.HideRecogObject();
                isCooldown = true;
                cooldownTimer = cooldownDuration;
                Debug.Log("Cooldown Started");

                e.ChangeEmissionColor(customColor);
                particles.Play();

                if (Buttonpress != null)
                {
                    Button.PlayOneShot(Buttonpress);
                }
            }

            if (isCooldown)
            {
                cooldownTimer -= Time.deltaTime;
                if (cooldownTimer <= 0f)
                {
                    isCooldown = false;
                    Debug.Log("Cooldown Ended");
                    wv.HideRecogObject();
                    if (e != null)
                    {
                        e.StopEffect();
                    }

                    if (isLooping)
                    {
                        StopLoopedSound();
                        isLooping = false; // Reset the looping flag when cooldown ends
                    }
                }
            }

            if (!isLooping && Input.GetKeyUp(pushToTalkKey))
            {
                ButtonRel.PlayOneShot(ButtonRelease);
                StopRecording();

                if (!isLooping)
                {
                    StartCoroutine(StartLoopedSoundWithDelay(2.0f));
                    isLooping = true; // Set the looping flag when space bar is released
                }
                if (speech.shouldSpeak == true)
                {
                    Debug.Log("TRUE!!!!");
                }
                wv.HideTalkingImageDelayed(8.0f);
                wv.HideCubes();
                wv.ShowRecogObject();
                e.ResetEmissionColor();
                e.StartEffect();
                particles.Stop();
            }
        }
        else
        {
            e.HideEmission();
            wv.HideCubes();
            foreach (GameObject character in characters)
            {
                character.SetActive(false);
            }
            speech.StopVisualEffectAtAnimationEnd();
            if (Input.GetKeyDown(pushToTalkKey))
            {
                Debug.Log("PUSHED BEFORE WAKEWORD");
                StartRecording();
            }
            if (Input.GetKeyUp(pushToTalkKey))
            {
                StopRecording();
            }
        }
        IEnumerator StartLoopedSoundWithDelay(float delayDuration)
        {
            yield return new WaitForSeconds(delayDuration);
            StartLoopedSound();
        }

        IEnumerator PlayLoopedSound()
        {
            while (isCooldown && !responseReceived)
            {
                loop.PlayOneShot(loopedSound);
                yield return new WaitForSeconds(loopedSound.length);
            }
            StopLoopedSound();
        }

        void StartLoopedSound()
        {
            StartCoroutine(PlayLoopedSound());
        }

        void StopLoopedSound()
        {
            StopCoroutine("PlayLoopedSound");
            loop.Stop();
        }
    }
    void GetSpectrumAudioSource()
    {
        _audioSource.GetSpectrumData(_samples, 0, FFTWindow.Blackman);
    }
    void createAudioBands()
    {
        for (int i = 0; i < 8; i++)
        {

            if (_freqBand[i] > _freqBandHighest[i])
            {

                _freqBandHighest[i] = _freqBand[i];
            }
            _audioBand[i] = (_freqBand[i] / _freqBandHighest[i]);
            _audioBandBuffer[i] = (_bandBuffer[i] / _freqBandHighest[i]);
        }
    }

    void GetAmplitude()
    {
        float _CurrentAmplitude = 0;
        float _CurrentAmplitudeBuffer = 0;
        for (int i = 0; i < 8; i++)
        {
            _CurrentAmplitude += _audioBand[i];
            _CurrentAmplitudeBuffer += _audioBandBuffer[i];
        }
        if (_CurrentAmplitude > _AmplitudeHighest)
        {
            _AmplitudeHighest = _CurrentAmplitude;
        }

        _Amplitude = _CurrentAmplitude / _AmplitudeHighest;
        _AmplitudeBuffer = _CurrentAmplitudeBuffer / _AmplitudeHighest;

    }

    void MakeFrequencyBands()
    {
        int count = 0;

        for (int i = 0; i < 8; i++)
        {
            float average = 0;
            int samplecount = (int)Mathf.Pow(2, i) * 2;

            if (i == 7)
            {
                samplecount += 2;
            }
            for (int j = 0; j < samplecount; j++)
            {
                average += _samples[count] * (count + 1);
                count++;
            }

            average /= count;
            _freqBand[i] = average * 10;
        }
    }

    private byte[] EncodeAsWAV(float[] samples, int frequency, int channels)
    {
        using (var memoryStream = new MemoryStream(44 + samples.Length * 2))
        {
            using (var writer = new BinaryWriter(memoryStream))
            {
                writer.Write("RIFF".ToCharArray());
                writer.Write(36 + samples.Length * 2);
                writer.Write("WAVE".ToCharArray());
                writer.Write("fmt ".ToCharArray());
                writer.Write(16);
                writer.Write((ushort)1);
                writer.Write((ushort)channels);
                writer.Write(frequency);
                writer.Write(frequency * channels * 2);
                writer.Write((ushort)(channels * 2));
                writer.Write((ushort)16);
                writer.Write("data".ToCharArray());
                writer.Write(samples.Length * 2);

                foreach (var sample in samples)
                {
                    writer.Write((short)(sample * short.MaxValue));
                }
            }
            return memoryStream.ToArray();
        }
    }
    private IEnumerator DisplayTextWithTypewriting(string text, Text textComponent, float typingSpeed, int fontSize)
    {
        textComponent.gameObject.SetActive(true);
        textComponent.fontSize = fontSize;

        for (int i = 0; i < text.Length; i++)
        {
            textComponent.text = text.Substring(0, i + 1);
            yield return new WaitForSeconds(typingSpeed);
        }
    }

    private void DisplayText(string text, Text textComponent, float displayTime, int fontSize)
    {
        StartCoroutine(DisplayTextWithTypewriting(text, textComponent, typingSpeed: 0.05f, fontSize));
        StartCoroutine(HideTextAfterSeconds(textComponent, displayTime));
    }

    private IEnumerator HideTextWithTypewriting(Text textComponent, float typingSpeed)
    {
        for (int i = textComponent.text.Length; i >= 0; i--)
        {
            textComponent.text = textComponent.text.Substring(0, i);
            yield return new WaitForSeconds(typingSpeed);
        }

        textComponent.gameObject.SetActive(false);
    }

    private IEnumerator HideTextAfterSeconds(Text textComponent, float displayTime)
    {
        yield return new WaitForSeconds(displayTime);
        StartCoroutine(HideTextWithTypewriting(textComponent, typingSpeed: 0.05f));
    }

    private void OnEnable()
    {
        spch.OnServerBusy += HandleServerBusy;
    }

    private void OnDisable()
    {
        spch.OnServerBusy -= HandleServerBusy;
    }

    private void HandleServerBusy()
    {
        msg = "Server is busy";
    }

    private async void SendRecording(byte[] audioBytes)
    {
        waitingForResponse = true;

        // Create a cancellation token source with a timeout of 5 seconds
        CancellationTokenSource cancellationTokenSource = new CancellationTokenSource();
        cancellationTokenSource.CancelAfter(7000);

        string receivedText = await Task.Run(async () =>
        {
            string response = "";

            try
            {
                using (var ws = new WebSocket("ws://127.0.0.1:8888"))
                {
                    ws.Connect();

                    // Send audio data to Python server
                    ws.Send(audioBytes);

                    TaskCompletionSource<bool> messageReceived = new TaskCompletionSource<bool>();

                    // Receive response from Python server
                    ws.OnMessage += (sender, e) =>
                    {
                        response = e.Data;
                        messageReceived.SetResult(true);
                    };

                    // Wait for either a response or timeout
                    await Task.WhenAny(messageReceived.Task, Task.Delay(-1, cancellationTokenSource.Token));

                    // Close connection
                    ws.Close();
                }
            }
            catch (Exception e)
            {
                Debug.LogError("Error: " + e.Message);
            }

            return response;
        });
        lock (responseLock)
        {
            if (cancellationTokenSource.IsCancellationRequested)
            {
                // Handle timeout case
                DisplayText("Server Is Busy", displayText2, displayTime: 7.0f,30);
            }
            else
            {
                string pattern = @"\[([^\[\]]*?)\]$";

                Match match = Regex.Match(receivedText, pattern);

                string language = "";
                string textToSend = receivedText;

                if (match.Success)
                {
                    language = match.Groups[1].Value;
                    receivedText = receivedText.Substring(0, match.Index).Trim();
                }
                Debug.Log("ASR Response: " + receivedText);
                Debug.Log("LANGAUGE: " + language);
                if (receivedText == "start" || receivedText == "起きる" || receivedText == "开始" || receivedText == "hola amigo" || receivedText == "nначинать")
                {
                    Debug.Log("WakeWord Detected");
                    isWakeWordDetected = true;
                }
                else if (isWakeWordDetected)
                {
                    wx.SendInputToServer(textToSend);
                    responseReceived = true;
                    DisplayText(receivedText, displayText2, displayTime: 7.0f,30);
                    if (receivedText.Contains("play") && receivedText.Split(' ').Length > 1)
                    {
                        Debug.Log("Received text contains more words after 'play'");
                        AudioReact.SetActive(true);
                    }
                    else if (receivedText == "pause")
                    {
                        Debug.Log("Received pause");
                        StartCoroutine(HideAfterDelay(0.5f));
                    }
                    else if (receivedText == "resume")
                    {
                        Debug.Log("Received resume");
                        AudioReact.SetActive(true);
                    }
                    else if (receivedText == "stop")
                    {
                        Debug.Log("Stop");
                        StartCoroutine(HideAfterDelay(0.5f));
                    }
                    else if (receivedText == "change look")
                    {
                        haschangedoutfit = true;
                    }

                }
                else
                {
                    if (ContainsJapaneseCharacters(receivedText) && language == "ja")
                    {
                        DisplayText("ウェイクワードを言ってください", displayText, displayTime: 3.0f,50);
                    }
                    else if(language == "zh")
                    {
                        DisplayText("說出喚醒詞", displayText, displayTime: 5.0f,60);
                    }
                    else if(language == "es")
                    {
                        DisplayText("Por favor di la palabra de activación", displayText, displayTime: 3.0f,25);
                    }
                    else if (language == "ru")
                    {
                        DisplayText("Пожалуйста, скажи слово пробуждения", displayText, displayTime: 3.0f, 46);
                    }
                    else
                    {
                        DisplayText("Please Say The Wakeword", displayText, displayTime: 3.0f,30);
                    }
                    
                }
            }

        }
    }

    bool ContainsJapaneseCharacters(string input)
    {
        foreach (char c in input)
        {
            // Japanese characters Unicode ranges
            if ((c >= 0x4E00 && c <= 0x9FFF) ||     // Kanji characters
                (c >= 0x3040 && c <= 0x309F) ||     // Hiragana characters
                (c >= 0x30A0 && c <= 0x30FF))       // Katakana characters
            {
                return true;
            }
        }
        return false;
    }

    IEnumerator HideAfterDelay(float delay)
    {
        yield return new WaitForSeconds(delay);
        AudioReact.SetActive(false);
    }

    private bool IsResponseReceived()
    {
        lock (responseLock)
        {
            return responseReceived;
        }
    }
}
