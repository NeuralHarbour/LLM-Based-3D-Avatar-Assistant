using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Emitter : MonoBehaviour
{
    public Renderer renderer;
    public Color emissionColor;
    public float maxEmissionIntensity;
    public float minEmissionIntensity; 
    public float cycleDuration = 5.0f;

    private Material material;
    private float timeElapsed = 0.0f;
    private bool isEffectRunning = true;

    private Color originalEmissionColor;

    void Start()
    {
        if (renderer == null)
        {
            renderer = GetComponent<Renderer>();
        }
        material = renderer.material;
        originalEmissionColor = emissionColor;
        // Ensure the material uses emission.
    }



    void Update()
    {
        if (isEffectRunning)
        {
            controller();
        }
    }

    void controller()
    {
        timeElapsed += Time.deltaTime;
        float t = Mathf.PingPong(timeElapsed, cycleDuration) / cycleDuration;

        float modifiedMinEmissionIntensity = Mathf.Pow(minEmissionIntensity, 1.0f);
        float modifiedMaxEmissionIntensity = Mathf.Pow(maxEmissionIntensity, 1.5f);

        float currentEmissionIntensity = Mathf.Lerp(modifiedMinEmissionIntensity, modifiedMaxEmissionIntensity, t);

        material.SetColor("_EmissionColor", emissionColor * currentEmissionIntensity);
    }



    public void StartEffect()
    {
        isEffectRunning = true;
    }

    public void StopEffect()
    {
        isEffectRunning = false;

        material.SetColor("_EmissionColor", emissionColor * Mathf.Pow(2.0F, 3f));
    }
    public void ChangeEmissionColor(Color newEmissionColor)
    {
        emissionColor = newEmissionColor;
        timeElapsed += Time.deltaTime;
        float t = Mathf.PingPong(timeElapsed, cycleDuration) / cycleDuration; // Value between 0 and 1.

        // Calculate emission intensity based on the ping-pong value.
        float currentEmissionIntensity = Mathf.Lerp(minEmissionIntensity, maxEmissionIntensity, t);
        // Apply the new emission color to the material's emission color.
        material.SetColor("_EmissionColor", emissionColor * Mathf.Pow(2.0F, 3.5f));
    }
    public void ResetEmissionColor()
    {
        emissionColor = originalEmissionColor;
        material.SetColor("_EmissionColor", emissionColor * Mathf.Pow(1.5F, 3.5f));
    }
    public void HideEmission()
    {
        material.DisableKeyword("_EMISSION");
    }
    public void showEmission()
    {
        material.EnableKeyword("_EMISSION");
    }

}
