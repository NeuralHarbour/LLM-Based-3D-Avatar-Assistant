using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class PDT_EffectButton : MonoBehaviour {
	public string button;
	public ParticleSystem ps;
	void Start () {
		ps = GetComponent<ParticleSystem> ();
		ps.Stop(true, ParticleSystemStopBehavior.StopEmittingAndClear);
	}
	public void offOnButton () {
		if (!ps.IsAlive(true)) {
			gameObject.SetActive(false);
			gameObject.SetActive(true);
		}
	}
	void Update () {
		if (Input.GetKeyDown(button))
				offOnButton ();
	}
}