using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Linq;
using UnityEngine.VFX;
using TMPro;

public class spch : MonoBehaviour
{
    private WsClient ws;
    private WeatherText wt;
    public HoloPanel hp;
    private ChairController CC;
    WorkoutManager WM;

    public bool shouldSpeak = false;
    private bool startsWithGreeting = false;
    private bool startsWithdayGreeting = false;
    private bool startsWithTime = false;
    private bool weatherreq = false;
    private bool delayStarted = false;
    private bool receivedQuestion = false;
    public bool isSitting = false;

    private Animator animator;
    public Animator chair_animator;

    public Text timetext;
    public Text DateText;
    public Text DayText;
    public TMP_Text weatherConditionText;
    public TMP_Text Temp;
    public TMP_Text Humidity;
    public TMP_Text Wind;


    public delegate void ServerBusyEventHandler();
    public static event ServerBusyEventHandler OnServerBusy;

    public MeshRenderer cubeRenderer;

    public Material sunnyMaterial;
    public Material rainyMaterial;
    public Material hazenight;
    public Material defaultmat;
    public Material scatMaterial;
    public Material brokmaterial;
    public Material mistmaterial;

    private string msg = "";
    private string currentEmotion = "";
    private string currentWeatherCondition = "";
    private string currentTemp = "";
    private string currentHumidity = "";
    private string currentWindSpeed = "";

    private Vector3 initialPosition;
    private Vector3 WeatherPosition;
    private Vector3 initialChairPosition;

    public GameObject gameobjecttomove;
    public GameObject initialpositionobject;
    public GameObject WeatherPositionObject;

    private Spchinstance instance;

    private List<WeatherText> weatherTextInstances = new List<WeatherText>();
    private float delayTime = 2.0f;

    public VisualEffect Entry;

    private float idleTimer = 0.0f;
    private float timeSinceLastSit = 0.0f;
    private float minActionTime = 30.0f; // 30 seconds
    private float maxActionTime = 60.0f; // 60 seconds
    private float _RandomActionTime = 0.0f;



    // Start is called before the first frame update
    void Start()
    {
        ws = GameObject.FindGameObjectWithTag("Middleware").GetComponent<WsClient>();
        hp = GameObject.FindGameObjectWithTag("WeatherDisp").GetComponent<HoloPanel>();
        WeatherText[] weatherTexts = GameObject.FindGameObjectsWithTag("WeatherTexts")
                                         .Select(obj => obj.GetComponent<WeatherText>())
                                         .ToArray();
        instance = GameObject.FindGameObjectWithTag("Speech").GetComponent<Spchinstance>();
        CC = GameObject.FindGameObjectWithTag("Chair").GetComponent<ChairController>();
        if (weatherTexts.Length > 0)
        {
            foreach (WeatherText weatherText in weatherTexts)
            {
                if (weatherText != null)
                {
                    weatherTextInstances.Add(weatherText);
                    weatherText.Hide();
                }
            }
        }
        else
        {
            Debug.Log("No WeatherText instances found.");
        }
        WsClient.OnMessageReceived += HandleMessageReceived;
        animator = GameObject.FindGameObjectWithTag("Player").GetComponent<Animator>();
        timetext.gameObject.SetActive(false);
        initialPosition = initialpositionobject.transform.position;
        WeatherPosition = WeatherPositionObject.transform.position;
        Debug.Log("Weather position : " + WeatherPosition);
        Debug.Log("initial position : " + initialPosition);
        if (hp != null)
        {
            Debug.Log("Holo Panel found on " + hp);
            hp.Hidden();
        }
        else
        {
            Debug.LogWarning("HoloPanel reference not assigned.");
        }
        WM = GameObject.FindGameObjectWithTag("waveform").GetComponent<WorkoutManager>();
    }
    public void UpdateActiveAnimator(Animator newAnimator, GameObject newCharacter)
    {
        animator = newAnimator;
        gameobjecttomove = newCharacter;
    }
    public void StopVisualEffectAtAnimationEnd()
    {
        Entry.Stop();
    }
    public void StartVisualEffect()
    {
        Entry.Play();
    }
    public void Update()
    {
        _RandomActionTime += Time.deltaTime;
        if (_RandomActionTime >= Random.Range(minActionTime, maxActionTime))
        {
            _RandomActionTime = 0f;
            Debug.Log("Performing a random Action");
            List<System.Action> randomActions = new List<System.Action>
            {
                WalKAround,
                Checkthephone,
                SitDownRandomly,
                Humm,
                CleanThearea,
                playvideogame,
                listentomusic,
            };

            // Select a random function and execute it
            if(!isSitting && !WM._isworkoutmode)
            {
                int randomIndex = Random.Range(0, randomActions.Count);
                randomActions[randomIndex].Invoke();
            }
        }

        if (shouldSpeak)
        {
            shouldSpeak = false; // Reset the flag after speaking
            if (greeting())
            {
                Debug.Log("Received a greeting");
                playgreeting();
            }
            if(timegreeting()) {
                playtimegreeting();
                Debug.Log("Recieved a Time greeting");
            }
            string extractedTime = CheckTime(msg);
            if (!string.IsNullOrEmpty(extractedTime))
            {
                Debug.Log("Received Time: " + extractedTime);
                DisplayText(extractedTime, timetext, displayTime: 5.0f);
            }
            string extractedDate = CheckDate(msg);
            if (!string.IsNullOrEmpty(extractedDate))
            {
                Debug.Log("Received Time: " + extractedDate);
                DisplayText(extractedDate, DateText, displayTime: 5.0f);
            }
            string extractedDay = CheckDay(msg);
            if (!string.IsNullOrEmpty(extractedDay))
            {
                Debug.Log("Received Day: " + extractedDay);
                DisplayText(extractedDay, DayText, displayTime: 5.0f);
            }
            if(weatherreq)
            {
                hp.active();
                hp.OpenUp();
                delayStarted = false;
                if (!delayStarted)
                {
                    StartCoroutine(DelayedWeatherTextActivation(delayTime));
                    delayStarted = true;
                }
                if (!string.IsNullOrEmpty(currentWeatherCondition) && !string.IsNullOrEmpty(currentTemp) && !string.IsNullOrEmpty(currentHumidity) && !string.IsNullOrEmpty(currentWindSpeed))
                {
                    Debug.Log("Current Weather Condition in Update: " + currentWeatherCondition);
                    weatherConditionText.text = currentWeatherCondition;
                    Temp.text = currentTemp + " °C";
                    Humidity.text = currentHumidity + " %";
                    Wind.text = currentWindSpeed + " m/s";

                    if (currentWeatherCondition == "broken clouds")
                    {
                        cubeRenderer.material = brokmaterial;
                    }
                    else if (currentWeatherCondition == "haze")
                    {
                        cubeRenderer.material = hazenight;
                    }
                    else if (currentWeatherCondition == "mist")
                    {
                        cubeRenderer.material = mistmaterial;
                    }
                    else
                    {
                        cubeRenderer.material = defaultmat;
                    }
                    currentWeatherCondition = "";

                }
                playweatheranim();
            }
            /*
            if (receivedQuestion)
            {

                receivedQuestion = false;
            }
            */

        }
    }

    private void SitDownRandomly()
    {
        Debug.Log("Character is sitting down");

        isSitting = true;

        CC.ShowChair();

        StartCoroutine(SitDownAnimation());


    }

    IEnumerator SitDownAnimation()
    {
        animator.applyRootMotion = true;
        yield return new WaitForSeconds(1f);
        if (Random.value > 0.5)
        {
            animator.SetTrigger("SitDown");
            yield return new WaitForSeconds(0.5f);
            animator.SetTrigger("Idle(Sit)");
            yield return new WaitForSeconds(2f);
            chair_animator.SetTrigger("StartFloat");
        }
        else
        {
            // Set triggers without playing animation
            animator.Play("SitDownVar1");
            yield return new WaitForSeconds(2f);
            chair_animator.SetTrigger("StartFloat");
        }
        // Get initial positions
        Vector3 initialCharacterPosition = gameobjecttomove.transform.position;
        initialChairPosition = chair_animator.transform.position;
        Vector3 positionOffset = initialChairPosition - initialCharacterPosition;
        StartCoroutine(StandUpTimer(30.0f, 60.0f));

        // Continuously update the character's position to match the chair's position
        while (true)
        {
            if (isSitting)
            {
                Vector3 newPosition = chair_animator.transform.position - positionOffset;
                newPosition += chair_animator.transform.forward * 0f;
                gameobjecttomove.transform.position = newPosition;
            }
            else
            {
                Vector3 newPosition = gameobjecttomove.transform.position;
                newPosition.y -= 0.07f;
                gameobjecttomove.transform.position = newPosition;
                break; // Exit the loop
            }
            yield return null;
        }

    }


    IEnumerator StandUpTimer(float minDelay, float maxDelay)
    {
        float delay = Random.Range(minDelay, maxDelay);
        yield return new WaitForSeconds(delay);

        StandUp();
    }

    void StandUp()
    {
        Debug.Log("Character is standing up");
        StartCoroutine(StandingUp());
    }

    IEnumerator StandingUp()
    {
        isSitting = false;
        animator.applyRootMotion = true;
        chair_animator.SetTrigger("ChairDown");
        animator.SetTrigger("standup");
        yield return new WaitForSeconds(5f);
        chair_animator.SetTrigger("Disappear");
        yield return new WaitForSeconds(1.85f);
        animator.applyRootMotion = false;
        StartCoroutine(ReturnToInitialPosition(0.5f));
        CC.HideChair();

    }

    private void WalKAround()
    {
        Debug.Log("Decided to walk around");
    }

    private void Checkthephone()
    {
        Debug.Log("Decided to check the phone");
    }

    private void Humm()
    {
        Debug.Log("Decided to Humm some music");
    }

    private void CleanThearea()
    {
        Debug.Log("Decided to clean the area");
    }

    private void playvideogame()
    {
        Debug.Log("Decided to play videogame");
    }
    private void listentomusic()
    {
        Debug.Log("Decided to listen to music ");
    }

    // Unsubscribe from the event when this script is disabled or destroyed
    private void OnDisable()
    {
        WsClient.OnMessageReceived -= HandleMessageReceived;
    }

    // Handle the received message
    public void HandleMessageReceived(string message)
    {
        // Initialize variables
        string msg = string.Empty;
        bool shouldSpeak = false;

        // Set the whole message
        msg = message.Trim();

        // Set the flag to indicate that speech should be executed
        shouldSpeak = true;

        // Call the ReceiveMessage method
        instance.ReceiveMessage(msg);

        // Check if the message ends with a question mark
        bool isQuestion = msg.EndsWith("?");

        if (isQuestion)
        {
            Debug.Log("Received a Question");
            //receivedQuestion = true;
        }

        // Handle server busyness
        if (HandleServerBusy(message))
        {
            OnServerBusy?.Invoke();
        }

        // Call various methods to handle greetings, time-related queries, weather queries, etc.
        GreetCheck(message);
        TimeGreetCheck(message);
        CheckTime(message);
        CheckDate(message);
        CheckDay(message);
        CheckWeather(message);
    }


    public void Emotion(string emotion)
    {
        currentEmotion = emotion.ToLower();
    }
    public void PlayHappyExpression()
    {
        Debug.Log("Playing happy animation");
        animator.SetTrigger("Joy");
        StartCoroutine(ReturnToNeutralAfterDelay());
    }

    public void PlaySadExpression()
    {
        Debug.Log("Playing sad animation");
        animator.SetTrigger("Sad");
        StartCoroutine(ReturnToNeutralAfterDelay());
    }

    public void PlayAngryExpression()
    {
        Debug.Log("Playing angry animation");
        animator.SetTrigger("Angry");
        StartCoroutine(ReturnToNeutralAfterDelay());
    }

    public void PlaySurprisedExpression()
    {
        Debug.Log("Playing surprise animation");
        animator.SetTrigger("surprised");
        StartCoroutine(ReturnToNeutralAfterDelay());
    }
    public void PlayNeutralExpression()
    {
        animator.SetTrigger("DefaultExp");
    }

    private IEnumerator ReturnToNeutralAfterDelay()
    {
        yield return new WaitForSeconds(2.0f);
        Debug.Log("Returning to neutral animation");
        animator.SetTrigger("DefaultExp");
    }
    public void GreetCheck(string message)
    {
        string[] greetings = { "hello", "hi", "hey", "greetings" };

        string lowercaseMessage = message.ToLower();
        startsWithGreeting = false;
        foreach (string greeting in greetings)
        {
            if (lowercaseMessage.StartsWith(greeting))
            {
                startsWithGreeting = true;
                break;
            }
        }
    }

    public void TimeGreetCheck(string message)
    {
        string[] greetings = { "Good Morning", "morning", "Top of the morning", "afternoon", "Good Afternoon", "Good Evening", "Evening" };

        string lowercaseMessage = message.ToLower();
        startsWithdayGreeting = false;

        foreach (string greeting in greetings)
        {
            if (lowercaseMessage.StartsWith(greeting.ToLower()))
            {
                startsWithdayGreeting = true;
                break;
            }
        }
    }

    public string CheckTime(string message)
    {
        string[] timemsg = { "The time is" };
        string lowercaseMessage = message.ToLower();

        foreach (string time in timemsg)
        {
            if (lowercaseMessage.StartsWith(time.ToLower()))
            {
                return message.Replace("The time is", "").Trim();
            }
        }
        return string.Empty;
    }
    public string CheckDate(string message)
    {
        string[] datemsg = { "Today is","Yesterday was","Tomorrow is", "Yes, yesterday was", "Yes, tomorrow will be","it is" };
        string lowercaseMessage = message.ToLower();

        foreach (string date in datemsg)
        {
            if (lowercaseMessage.StartsWith(date.ToLower()))
            {
                return message.Replace(date, "").Trim();
            }
        }
        return string.Empty;
    }

    public string CheckDay(string message)
    {
        string[] daymsg = { "Today is","Yesterday was","Tomorrow is" };
        string lowercaseMessage = message.ToLower();

        foreach (string day in daymsg)
        {
            if (lowercaseMessage.StartsWith(day.ToLower()))
            {
                return message.Replace(day, "").Trim();
            }
        }
        return string.Empty;
    }
    public void CheckWeather(string message)
    {
        string[] daymsg = { "Here is today's weather forecast.", "Let's take a look at today's weather.", "Checking the weather for today.", "Today's forecast is as follows.", "The weather outlook for today." };
        string lowercaseMessage = message.ToLower();
        weatherreq = false;
        foreach (string day in daymsg)
        {
            if (lowercaseMessage.StartsWith(day.ToLower()))
            {
                weatherreq = true;
                ExtractWeatherInfo(message);
                break;
            }
        }
    }
    public void ExtractWeatherInfo(string message)
    {
        string weatherCondition = string.Empty;
        int temperatureStartIndex = message.IndexOf("Temperature stands at");
        if (temperatureStartIndex != -1)
        {
            int temperatureEndIndex = message.IndexOf("°C", temperatureStartIndex);
            if (temperatureEndIndex != -1)
            {
                string temperatureSubstring = message.Substring(temperatureStartIndex, temperatureEndIndex - temperatureStartIndex);
                string temperature = temperatureSubstring.Replace("Temperature stands at comfortable ", "").Trim();
                currentTemp = temperature;
                Debug.Log("Temperature: " + temperature);
            }
        }

        int humidityStartIndex = message.IndexOf("humidity level of");
        if (humidityStartIndex != -1)
        {
            int humidityEndIndex = message.IndexOf("%", humidityStartIndex);
            if (humidityEndIndex != -1)
            {
                string humiditySubstring = message.Substring(humidityStartIndex, humidityEndIndex - humidityStartIndex);
                string humidity = humiditySubstring.Replace("humidity level of ", "").Trim();
                currentHumidity = humidity;
                Debug.Log("Humidity: " + humidity);
            }
        }

        int windSpeedStartIndex = message.IndexOf("breeze blowing at");
        if (windSpeedStartIndex != -1)
        {
            int windSpeedEndIndex = message.IndexOf("m/s", windSpeedStartIndex);
            if (windSpeedEndIndex != -1)
            {
                string windSpeedSubstring = message.Substring(windSpeedStartIndex, windSpeedEndIndex - windSpeedStartIndex);
                string windSpeed = windSpeedSubstring.Replace("breeze blowing at ", "").Trim();
                currentWindSpeed = windSpeed;
                Debug.Log("Wind Speed: " + windSpeed);
            }
        }

        int descriptionStartIndex = message.IndexOf("The overall condition is described as");

        if (descriptionStartIndex != -1)
        {
            string conditionSubstring = message.Substring(descriptionStartIndex + "The overall condition is described as".Length).Trim();
            char[] delimiters = { '.', '\n' };
            int endIndex = conditionSubstring.IndexOfAny(delimiters);

            weatherCondition = endIndex != -1 ? conditionSubstring.Substring(0, endIndex).Trim() : conditionSubstring.Trim();
            currentWeatherCondition = weatherCondition;
            Debug.Log("Weather Condition: " + weatherCondition);
        }
    }


    private bool timegreeting()
    {
        return startsWithdayGreeting;
    }
    private bool greeting()
    {
        return startsWithGreeting;
    }
    private void playtimegreeting()
    {
        animator.SetTrigger("Bow");
        StartCoroutine("StopgreetAnimation");
    }
    private void playgreeting()
    {
        animator.SetTrigger("IsWaving");
        StartCoroutine("StopgreetAnimation");
    }
    private void playquestionanimation()
    {
        animator.SetTrigger("Concern");
        StartCoroutine("StopgreetAnimation");
    }
    IEnumerator StopgreetAnimation()
    {
        yield return new WaitForSeconds(3);
        animator.SetTrigger("Idle");
    }

    private IEnumerator DelayedWeatherTextActivation(float delay)
    {
        yield return new WaitForSeconds(delay);

        foreach (WeatherText weatherText in weatherTextInstances)
        {
            weatherText.Active();
            weatherText.LoadText();
        }
    }
    private IEnumerator MoveToObject(GameObject objectToMove, Vector3 targetPosition, float duration)
    {
        float elapsedTime = 0;
        Vector3 startingPosition = objectToMove.transform.position;

        // Play the movement animation or trigger walk animation
        animator.SetTrigger("walkstrafe");

        while (elapsedTime < duration)
        {
            objectToMove.transform.position = Vector3.Lerp(startingPosition, targetPosition, (elapsedTime / duration));
            elapsedTime += Time.deltaTime;
            yield return null;
        }
        // Ensure the object reaches the exact target position
        
        animator.SetTrigger("Idle");
        objectToMove.transform.position = targetPosition;
        objectToMove.transform.rotation = Quaternion.Euler(0, 190, 0);

        yield return StartCoroutine(CheckIdleAnimation(23.0f));
    }

    private IEnumerator CheckIdleAnimation(float minIdleTime)
    {
        float elapsedTime = 0.0f;
        while (elapsedTime < minIdleTime)
        {
            elapsedTime += Time.deltaTime;
            yield return null;
        }
        animator.applyRootMotion = false;
        animator.SetTrigger("walkreverse");
        StartCoroutine(ReturnToInitialPosition(0.5f));

    }

    private IEnumerator ReturnToInitialPosition(float duration)
    {
        float timer = 0.0f;
        Vector3 startPosition = gameobjecttomove.transform.position;
        while (timer < duration)
        {
            timer += Time.deltaTime;
            float t = timer / duration;
            gameobjecttomove.transform.position = Vector3.Lerp(startPosition, initialPosition, t);
            yield return null;
        }
        // Ensure the object reaches the exact initial position
        gameobjecttomove.transform.position = initialPosition;
        animator.SetTrigger("Idle");
        gameobjecttomove.transform.rotation = Quaternion.Euler(0, 180, 0);
        yield return new WaitForSeconds(2f);
        animator.applyRootMotion = true;
    }


    private void playweatheranim()
    {
        StartCoroutine(MoveToObject(gameobjecttomove, WeatherPosition, 0.55f));
    }

    public bool HandleServerBusy(string message)
    {
        if (message == "Sorry I am Busy")
        {
            Debug.Log("Received Server is busy FROM SPCH");
            return true;
        }
        else
        {
            return false;
        }
    }
    private IEnumerator DisplayTextWithTypewriting(string text, Text textComponent, float typingSpeed)
    {
        textComponent.gameObject.SetActive(true);

        for (int i = 0; i < text.Length; i++)
        {
            textComponent.text = text.Substring(0, i + 1);
            yield return new WaitForSeconds(typingSpeed);
        }
    }

    private void DisplayText(string text, Text textComponent, float displayTime)
    {
        StartCoroutine(DisplayTextWithTypewriting(text, textComponent, typingSpeed: 0.05f));
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
}
