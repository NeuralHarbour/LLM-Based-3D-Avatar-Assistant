using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Wavcon : MonoBehaviour
{
    public Image talkingImage;
    public GameObject cube1;
    public GameObject cube2;
    public GameObject cube3;
    public GameObject cube4;
    public GameObject cube5;
    public GameObject Recog;

    public float fadeDuration = 0.5f; // Duration of the fade-out effect in seconds
    private Coroutine fadeCoroutine;

    private Color initialColor; // Store the initial color
    private float initialAlpha; // Store the initial alpha

    private bool isFading = false;

    // Start is called before the first frame update
    void Start()
    {
        if (talkingImage != null)
        {
            initialColor = talkingImage.color;
            initialAlpha = initialColor.a;
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void ShowTalkingImage()
    {
        if (talkingImage != null)
        {
            talkingImage.color = initialColor; // Restore the initial color
            talkingImage.gameObject.SetActive(true);
        }
    }

    public void HideTalkingImageDelayed(float delayInSeconds)
    {
        if (talkingImage != null)
        {
            if (isFading)
            {
                StopCoroutine(fadeCoroutine);
                isFading = false;
            }
            fadeCoroutine = StartCoroutine(FadeOutImage(delayInSeconds));
        }
    }

    private IEnumerator FadeOutImage(float delay)
    {
        isFading = true;

        yield return new WaitForSeconds(delay);

        float t = 0;

        while (t < fadeDuration)
        {
            t += Time.deltaTime;
            Color newColor = Color.Lerp(initialColor, Color.clear, t / fadeDuration);
            newColor.a = Mathf.Lerp(initialAlpha, 0, t / fadeDuration);
            talkingImage.color = newColor;
            yield return null;
        }

        Color finalColor = Color.clear;
        finalColor.a = 0;
        talkingImage.color = finalColor;
        talkingImage.gameObject.SetActive(false);

        isFading = false;
    }

    public void HideTalkingImage()
    {
        if (talkingImage != null && talkingImage.gameObject.activeSelf)
        {
            talkingImage.gameObject.SetActive(false);
        }
    }
    public void HideRecogObject()
    {
        Recog.gameObject.SetActive(false);
    }
    public void ShowRecogObject()
    {
        Recog.gameObject.SetActive(true);
    }

    public void ShowCubes()
    {
        cube1.gameObject.SetActive(true);
        cube2.gameObject.SetActive(true);
        cube3.gameObject.SetActive(true);
        cube4.gameObject.SetActive(true);
        cube5.gameObject.SetActive(true);
    }

    public void HideCubes()
    {
        cube1.gameObject.SetActive(false);
        cube2.gameObject.SetActive(false);
        cube3.gameObject.SetActive(false);
        cube4.gameObject.SetActive(false);
        cube5.gameObject.SetActive(false);
    }
}
