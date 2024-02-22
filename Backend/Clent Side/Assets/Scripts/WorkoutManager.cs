using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WorkoutManager : MonoBehaviour
{
    public Animator animator;
    private spch _animfunctions;
    private waveform wv;
    public bool _isworkoutmode = false;
    float _transitionAnimLen = 3.5f;
    public GameObject WorkoutCharacter;

    int characterIndex = 0;
    // Start is called before the first frame update
    void Start()
    {
        _animfunctions = GameObject.FindGameObjectWithTag("character").GetComponent<spch>();
        wv = GameObject.FindGameObjectWithTag("waveform").GetComponent<waveform>();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void ReceiveActiveCharacterIndex(int activeCharacterIndex)
    {
        characterIndex = activeCharacterIndex;
        Debug.Log("Received active character index: " + characterIndex);
    }

    public void StartWorkoutMode()
    {
        if (!_animfunctions.isSitting)
        {
            _isworkoutmode = true;
            StartCoroutine(SwitchToWorkOutMode());
        }
        else
        {
            Debug.Log("Character Is Sitting");
        }
    }

    IEnumerator SwitchToWorkOutMode()
    {
        GameObject[] characters = wv.characters;
        animator.SetTrigger("SportsMode");
        _animfunctions.StartVisualEffect();
        yield return new WaitForSeconds(_transitionAnimLen / 1.4f);
        float normalizedTime = 0f;
        AnimatorStateInfo stateInfo = animator.GetCurrentAnimatorStateInfo(0);
        if (stateInfo.length > 0)
        {
            normalizedTime = stateInfo.normalizedTime;
        }
        characters[characterIndex].SetActive(false);
        WorkoutCharacter.SetActive(true);

        animator = WorkoutCharacter.GetComponent<Animator>();

        if (animator != null)
        {
            animator.Play(stateInfo.fullPathHash, 0, normalizedTime);
        }

        animator.applyRootMotion = false;
        yield return new WaitForSeconds(_transitionAnimLen / 2f);
        animator.SetTrigger("Idle");
    }

}
