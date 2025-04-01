//////////////////////////////////////////////////////
///        © Copyright 2023 - ReForge Mode         ///
/// See the LICENSE file for licensing information ///
//////////////////////////////////////////////////////

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

#if UNITY_EDITOR
using UnityEditor;

namespace NotEnoughBlendshape
{
    /// <summary>
    /// Compare the vertices of two models and create a Blendshape from the difference
    /// </summary>
    public class BlendshapeCreator : MonoBehaviour
    {
        public SkinnedMeshRenderer sourceMeshRenderer;
        public SkinnedMeshRenderer targetMeshRenderer;          //The default model to create blendshapes to
        public string newBlendshapeName = "Custom Blendshape";

        private Mesh sourceMesh;
        private Mesh targetMesh;

        public int CreateBlendshape()
        {
            sourceMesh = sourceMeshRenderer.sharedMesh;
            targetMesh = targetMeshRenderer.sharedMesh;


            //Initialize the blendshape array and iterate through vertices to calculate the delta
            List<Vector3> deltaVertices = new List<Vector3>();
            for (int i = 0; i < targetMesh.vertexCount; i++)
            {
                Vector3 delta = sourceMesh.vertices[i] - targetMesh.vertices[i];
                deltaVertices.Add(delta);
            }

            //Create the blendshape and add it to the source mesh
            try
            {
                targetMesh.AddBlendShapeFrame(newBlendshapeName, 100f, deltaVertices.ToArray(), null, null);
            }
            catch(ArgumentException ex)
            {
                //Handle the exception here
                Debug.LogError("The number of Source and Target models vertices don't match! " +
                               "This is because the model was exported from VRoid Studio with <b>\"Delete Transparent Meshes\"</b> option checked. " +
                               "This option is enabled by default in the <b>\"Reduce Polygon\"</b> export settings. " +
                               "Make sure to uncheck it first and export the model again into this Unity project!\n\n" + ex.Message);

                // Stop the function on error
                return 0;
            }

            EditorUtility.DisplayDialog("Success!", "Success! New blendshape has been created!", "Yay!");

            //Assign a new unique name
            newBlendshapeName = NEBLiteUtilities.FindUniqueName(newBlendshapeName);

            return 1;
        }
    }
}
#endif