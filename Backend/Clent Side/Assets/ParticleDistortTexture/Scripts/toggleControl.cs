using System.Collections;
using UnityEngine;
using UnityEngine.UI;

public class toggleControl : MonoBehaviour {
	public GameObject[] effects;
	ParticleSystem[] fx;
	public Toggle toggleButton;
	public Text toggleText;
	public Button prevButton;
	public Button nextButton;
	public int nonLoop = 19;
	public string removal = "(UnityEngine.ParticleSystem)";
	int count=0;
	
	void Start(){
		fx = new ParticleSystem[effects.Length];
		for (int i = 0 ; i < effects.Length ; i++) {
			fx[i] = effects[i].GetComponent<ParticleSystem>();
		}
		toggleText.text = fx[count].ToString().Replace(removal,"");
		for (count = 1 ; count < fx.Length ; count++) {
			fx[count].Stop(true,ParticleSystemStopBehavior.StopEmittingAndClear);
		}
		count=0;
		fx[0].Play(true);
		if (nonLoop < 0) {
			nonLoop = 1000000;
		}
	}
	
	public void onOff(){
		if (toggleButton.isOn) {
			fx[count].Play(true);
		} else {
			if (count > nonLoop) {
				fx[count].Stop(true,ParticleSystemStopBehavior.StopEmittingAndClear);
				fx[count].Play(true);
				toggleButton.isOn = true;
			} else {
				fx[count].Stop(true);
			}
		}
	}
	
	public void next(){
		fx[count].Stop(true, ParticleSystemStopBehavior.StopEmittingAndClear);
		if (count == fx.Length-1) {
			count = 0;
		} else {
			count++;
		}
		toggleText.text = fx[count].ToString().Replace(removal,"");
		fx[count].Play(true);
		toggleButton.isOn = true;
	}
	
	public void prev(){
		fx[count].Stop(true, ParticleSystemStopBehavior.StopEmittingAndClear);
		if (count == 0) {
			count = fx.Length-1;
		} else {
			count--;
		}
		toggleText.text = fx[count].ToString().Replace(removal,"");
		fx[count].Play(true);
		toggleButton.isOn = true;
	}
}