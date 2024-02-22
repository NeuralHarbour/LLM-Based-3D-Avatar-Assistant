using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BoredBehaviour : StateMachineBehaviour
{
    [SerializeField]
    private float _timeUntilBored;

    [SerializeField]
    private int _numberofBoredAnimations;

    private bool isbored;
    private float idletime;
    private int _boredAnimation;
    // OnStateEnter is called when a transition starts and the state machine starts to evaluate this state
    override public void OnStateEnter(Animator animator, AnimatorStateInfo stateInfo, int layerIndex)
    {
        ResetIdle();
    }

    // OnStateUpdate is called on each Update frame between OnStateEnter and OnStateExit callbacks
    override public void OnStateUpdate(Animator animator, AnimatorStateInfo stateInfo, int layerIndex)
    {
        if(!isbored) {
            idletime += Time.deltaTime;

            if (idletime > _timeUntilBored && stateInfo.normalizedTime % 1 < 0.02f)
            {
                isbored = true;
                _boredAnimation = Random.Range(1, _numberofBoredAnimations + 1);
                _boredAnimation = _boredAnimation * 2 - 1;

                animator.SetFloat("BoredAnimation", _boredAnimation - 1);
            }
        }
        else if(stateInfo.normalizedTime % 1 > 0.98)
        {
            ResetIdle();
        }
        animator.SetFloat("BoredAnimation", _boredAnimation,0.2f,Time.deltaTime);
    }

    private void ResetIdle()
    {
        if(isbored)
        {
            _boredAnimation--;
        }
        isbored = false;
        idletime = 0;
    }

}
