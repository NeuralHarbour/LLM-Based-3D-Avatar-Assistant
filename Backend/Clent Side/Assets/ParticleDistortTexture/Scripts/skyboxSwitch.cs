using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class skyboxSwitch : MonoBehaviour {
	public Toggle toggleButton;
	public Camera mainCam;
	public void skyboxOrSolid () {
		if (toggleButton.isOn) {
			mainCam.clearFlags = CameraClearFlags.Skybox;
		} else {
			mainCam.clearFlags = CameraClearFlags.SolidColor;
		}
	}
}
