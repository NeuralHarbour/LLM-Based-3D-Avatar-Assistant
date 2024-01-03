using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;


namespace AGIA
{ 
public class AGIAFree_sample : MonoBehaviour
    {
        public Animator animator;
        public int animBase;
        public int animLayer;

	    // Use this for initialization
	    void Start ()
        {

            animator = GetComponent<Animator>();
            animator.SetInteger("animBaseInt", 1);

        }
	
	    // Update is called once per frame
	    void Update ()
        {
		
	    }

        public void animBaseChange()
        {
            animator.SetInteger("animOtherInt", 0);

            var clickedButton = EventSystem.current.currentSelectedGameObject.name;

            if(clickedButton == "Generic_01")
            {
                animator.SetInteger("animBaseInt", 1);
            }
            else if (clickedButton == "Angry_01")
            {
                animator.SetInteger("animBaseInt", 2);
            }
            else if (clickedButton == "Brave_01")
            {
                animator.SetInteger("animBaseInt", 3);
            }
            else if (clickedButton == "Calm_01")
            {
                animator.SetInteger("animBaseInt", 4);
            }
            else if (clickedButton == "Concern_01")
            {
                animator.SetInteger("animBaseInt", 5);
            }
            else if (clickedButton == "Energetic_01")
            {
                animator.SetInteger("animBaseInt", 6);
            }
            else if (clickedButton == "Energetic_02")
            {
                animator.SetInteger("animBaseInt", 7);
            }
            else if (clickedButton == "Pitiable_01")
            {
                animator.SetInteger("animBaseInt", 8);
            }
            else if (clickedButton == "Surprised_01")
            {
                animator.SetInteger("animBaseInt", 9);
            }
        }

        public void animLayerChange()
        {
            var clickedButton = EventSystem.current.currentSelectedGameObject.name;

            if (clickedButton == "Reset")
            {
                animator.Play("Layer_start", 1, 0.0f);
            }

            else if (clickedButton == "LookAway_01")
            {
                animator.Play("Layer_look_away", 1, 0.0f);
            }

            else if (clickedButton == "NoddingOnce_01")
            {
                animator.Play("Layer_nodding_once", 1, 0.0f);
            }

            else if (clickedButton == "SwingingBody_01")
            {
                animator.Play("Layer_swinging_body", 1, 0.0f);
            }

        }

        public void animOtherChange()
        {
            animator.SetInteger("animBaseInt", 0);

            var clickedButton = EventSystem.current.currentSelectedGameObject.name;
            if (clickedButton == "walking_01")
            {
                animator.SetInteger("animOtherInt", 1);
            }

            else if (clickedButton == "WavingArm_01")
            {
                animator.SetInteger("animOtherInt", 2);
            }


        }
    }
}
