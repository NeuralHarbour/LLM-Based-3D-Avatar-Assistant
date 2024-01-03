using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Blink : MonoBehaviour
{
    public SkinnedMeshRenderer skinnedMesh;
    public int blendshapeIndex;

    [Header("Properties")]
    public float blinkInterval = 5.0f;  //time until the next blink
    public float blinkEyeCloseDuration = 0.06f; //how long the eye stays closed during blinking
    public float blinkOpeningSeconds = 0.03f; //the speed of eye opening in the animation
    public float blinkClosingSeconds = 0.1f;  //the speed of eye closing in the animation

    public Coroutine blinkCoroutine;

    private void Awake()
    {
        blendshapeIndex = GetBlendshapeIndex("Fcl_EYE_Close");
    }

    private int GetBlendshapeIndex(string blendshapeName)
    {
        Mesh mesh = skinnedMesh.sharedMesh;
        int blendshapeIndex = mesh.GetBlendShapeIndex(blendshapeName);
        return blendshapeIndex;
    }

    private IEnumerator BlinkRoutine()
    {
        //This is an infinite loop coroutine
        while (true)
        {
            //Wait until we need to blink
            yield return new WaitForSeconds(blinkInterval);

            //Close eyes
            var value = 0f;
            var closeSpeed = 1.0f / blinkClosingSeconds;
            while (value < 1)
            {
                skinnedMesh.SetBlendShapeWeight(blendshapeIndex, value * 100);
                value += Time.deltaTime * closeSpeed;
                yield return null;
            }
            skinnedMesh.SetBlendShapeWeight(blendshapeIndex, 100);

            //Wait to open our eyes
            yield return new WaitForSeconds(blinkEyeCloseDuration);

            //Open eyes
            value = 1f;
            var openSpeed = 1.0f / blinkOpeningSeconds;
            while (value > 0)
            {
                skinnedMesh.SetBlendShapeWeight(blendshapeIndex, value * 100);
                value -= Time.deltaTime * openSpeed;
                yield return null;
            }
            skinnedMesh.SetBlendShapeWeight(blendshapeIndex, 0);
        }
    }

    private void OnEnable()
    {
        blinkCoroutine = StartCoroutine(BlinkRoutine());
    }

    private void OnDisable()
    {
        if (blinkCoroutine != null)
        {
            StopCoroutine(blinkCoroutine);
            blinkCoroutine = null;
        }
    }
}