using UnityEngine;
using TMPro;
using System.Collections;
using System.Collections.Generic;

public class TextManager : MonoBehaviour
{
    private AutoDetectVoice ws;
    private string previousText = "";
    public TextMeshProUGUI displayText;
    public bool wakewordDetected = false;
    [SerializeField] private bool bypasswakeword = false;
    public TextMeshProUGUI wakeWordPromptText;
    AutoDetectVoice av;
    private string currentCheatCode = "";
    private float cheatCodeResetTime = 2f;
    private float lastKeyPressTime;
    private bool processNextMessage = false;
    WsClient wsock;
    Integrity_Loader IL;

    string receivedText = "";
    string language = "";

    public string intent;

    public delegate void SystemStateChangeHandler(bool isActive);
    public event SystemStateChangeHandler OnSystemStateChange;
    public string currentReceivedText;

    public bool isSystemActive = false;
    void Start()
    {
        ws = FindObjectOfType<AutoDetectVoice>();
        wsock = FindObjectOfType<WsClient>();
        displayText.gameObject.SetActive(false);
        wakeWordPromptText.gameObject.SetActive(false);
        IL = FindObjectOfType<Integrity_Loader>();

    }

    void Update()
    {
        if (IL.End_Flag)
        {
            HandleCheatCodes();
            currentReceivedText = ws.receivedText;
            language = ws.language;
            if (!string.IsNullOrEmpty(currentReceivedText))
            {
                if (currentReceivedText != previousText)
                {
                    Debug.Log("Detected Language : " + language);
                    Debug.Log("Received Response: " + currentReceivedText);


                    if (currentReceivedText.ToLower() == "start" && language == "en")
                    {
                        SetSystemState(true);
                        HideWakeWordPrompt();
                        Debug.Log("System activated! Waiting for the next command.");

                    }
                    else if (!isSystemActive)
                    {
                        ShowWakeWordPrompt();
                    }
                    else if (wakewordDetected && processNextMessage)
                    {
                        processNextMessage = false;
                        HideWakeWordPrompt();
                        DisplayText(currentReceivedText, displayText, 5f, 36);
                        //wsock.SendInputToSecondaryServer(currentReceivedText);
                        if ((currentReceivedText.ToLower() == "quit" || currentReceivedText.ToLower() == "stop"))
                        {
                            SetSystemState(false);
                            HideWakeWordPrompt();
                        }
                        else
                        {
                            string classifiedIntent = MenuItem_KODEZ_Class.Intent_Classifier(currentReceivedText);
                            Debug.Log($"Classified Intent: {classifiedIntent}");
                            intent = classifiedIntent;

                        }
                    }
                    else if (wakewordDetected)
                    {
                        DisplayText(currentReceivedText, displayText, 5f, 36);
                        //wsock.SendInputToSecondaryServer(currentReceivedText);
                        if ((currentReceivedText.ToLower() == "quit" || currentReceivedText.ToLower() == "stop"))
                        {
                            SetSystemState(false);
                            HideWakeWordPrompt();
                        }
                        else
                        {
                            string classifiedIntent = MenuItem_KODEZ_Class.Intent_Classifier(currentReceivedText);
                            Debug.Log($"Classified Intent: {classifiedIntent}");
                            intent = classifiedIntent;
                        }
                    }
                    previousText = currentReceivedText;
                }
                else if (isSystemActive && wakewordDetected && !processNextMessage)
                {
                    DisplayText(currentReceivedText, displayText, 5f, 36);
                }
                ws.receivedText = null;
            }
        }
    }

    private void SetSystemState(bool active)
    {
        isSystemActive = active;
        wakewordDetected = active;
        processNextMessage = active;
        OnSystemStateChange?.Invoke(active);
    }

    private void HandleCheatCodes()
    {
        if (Input.anyKeyDown)
        {
            if (Time.time - lastKeyPressTime > cheatCodeResetTime)
            {
                currentCheatCode = "";
            }

            lastKeyPressTime = Time.time;
            currentCheatCode += Input.inputString.ToLower();

            if (currentCheatCode.EndsWith("bpwk"))
            {
                ToggleBypassWakeword();
                currentCheatCode = "";
            }
        }
    }

    public void ToggleBypassWakeword()
    {
        bypasswakeword = !bypasswakeword;
        Debug.Log($"Bypass Wakeword: {bypasswakeword}");

        if (bypasswakeword)
        {
            wakewordDetected = true;
            SetSystemState(true);
            HideWakeWordPrompt();
        }
        else
        {
            wakewordDetected = false;
        }
    }

    private void ShowWakeWordPrompt()
    {
        Debug.Log("Wakeword not detected");
        wakeWordPromptText.gameObject.SetActive(true);
        DisplayText("Please say the wakeword", wakeWordPromptText, 5f, 40);
    }

    private void HideWakeWordPrompt()
    {
        wakeWordPromptText.gameObject.SetActive(false);
    }

    private IEnumerator DisplayTextWithTypewriting(string text, TextMeshProUGUI textComponent, float typingSpeed, int fontSize)
    {
        textComponent.gameObject.SetActive(true);
        textComponent.fontSize = fontSize;
        for (int i = 0; i < text.Length; i++)
        {
            textComponent.text = text.Substring(0, i + 1);
            yield return new WaitForSeconds(typingSpeed);
        }
    }

    public void DisplayText(string text, TextMeshProUGUI textComponent, float displayTime, int fontSize)
    {
        StartCoroutine(DisplayTextWithTypewriting(text, textComponent, typingSpeed: 0.05f, fontSize));
        StartCoroutine(HideTextAfterSeconds(textComponent, displayTime));
    }

    private IEnumerator HideTextWithTypewriting(TextMeshProUGUI textComponent, float typingSpeed)
    {
        for (int i = textComponent.text.Length; i >= 0; i--)
        {
            textComponent.text = textComponent.text.Substring(0, i);
            yield return new WaitForSeconds(typingSpeed);
        }
        textComponent.gameObject.SetActive(false);
    }

    private IEnumerator HideTextAfterSeconds(TextMeshProUGUI textComponent, float displayTime)
    {
        yield return new WaitForSeconds(displayTime);
        StartCoroutine(HideTextWithTypewriting(textComponent, typingSpeed: 0.05f));
    }
}
