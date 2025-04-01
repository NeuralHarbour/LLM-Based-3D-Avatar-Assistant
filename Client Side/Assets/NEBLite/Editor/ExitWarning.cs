//////////////////////////////////////////////////////
///        © Copyright 2023 - ReForge Mode         ///
/// See the LICENSE file for licensing information ///
//////////////////////////////////////////////////////

#if UNITY_EDITOR
using UnityEngine;
using UnityEditor.SceneManagement;
using UnityEditor;


/// <summary>
/// Reminds the user to export VRM files before exiting.
/// Because for some reason, any modifications to the original mesh of the model are not saved on Unity exit.
/// </summary>
[InitializeOnLoad]
public static class ExitWarning
{
    static ExitWarning()
    {
        EditorApplication.wantsToQuit += OnWantsToQuit;
    }

    private static bool OnWantsToQuit()
    {
        bool shouldQuit = EditorUtility.DisplayDialog(
            "NEB Reminder",

            "Modified blendshapes in your VRM models are not saved when Unity is closed. " +
            "Make sure that you have exported your VRM model before closing Unity.\n\n" +
            "Are you sure you want to close Unity?",

            "Yes, close Unity",
            "No, stay in Unity"
        );

        return shouldQuit;
    }
}
#endif