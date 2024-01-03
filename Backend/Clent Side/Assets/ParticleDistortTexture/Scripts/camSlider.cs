using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class camSlider : MonoBehaviour {
	public Slider mainSlider;
	public float range = 360f;
	public void camX () {
		this.transform.localEulerAngles = new Vector3 (((mainSlider.value) * range)-70f,0f,0f);
	}
	public void camY () {
		this.transform.localEulerAngles = new Vector3 (0f,(mainSlider.value) * range,0f);
	}
}