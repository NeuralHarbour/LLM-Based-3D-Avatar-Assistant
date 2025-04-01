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
    public class BlendshapeTransfer : MonoBehaviour
    {
        public SkinnedMeshRenderer sourceMeshRenderer;
        public SkinnedMeshRenderer targetMeshRenderer;

        [HideInInspector] public GameObject sourceModel;
        [HideInInspector] public GameObject targetModel;
        [HideInInspector] public Mesh sourceMesh;
        [HideInInspector] public Mesh targetMesh;

        public bool isAdvancedMode = false;

        public int CopyBlendshape()
        {
            sourceMesh = sourceMeshRenderer.sharedMesh;
            targetMesh = targetMeshRenderer.sharedMesh;

            Vector3[] deltaVertices = new Vector3[sourceMesh.vertexCount];
            Vector3[] deltaNormals = new Vector3[sourceMesh.vertexCount];
            Vector3[] deltaTangents = new Vector3[sourceMesh.vertexCount];

            //For every blendshapes...
            for (int shapeIndex = 0; shapeIndex < sourceMesh.blendShapeCount; shapeIndex++)
            {
                string shapeName = sourceMesh.GetBlendShapeName(shapeIndex);

                // Don't copy if target already has a blend shape with this name. (It throws an exception.)
                if (targetMesh.GetBlendShapeIndex(shapeName) < 0)
                {
                    //For every frames in each blendshape...
                    //Copy across the keyframes in the blendshape (most have 1 keyframe).
                    int frameCount = sourceMesh.GetBlendShapeFrameCount(shapeIndex);
                    for (int frameIndex = 0; frameIndex < frameCount; frameIndex++)
                    {
                        float frameWeight = sourceMesh.GetBlendShapeFrameWeight(shapeIndex, frameIndex);

                        try 
                        { 
                            sourceMesh.GetBlendShapeFrameVertices(shapeIndex, frameIndex, deltaVertices, deltaNormals, deltaTangents);
                            targetMesh.AddBlendShapeFrame(shapeName, frameWeight, deltaVertices, deltaNormals, deltaTangents); 
                        }
                        catch (ArgumentException ex)
                        {
                            //Handle the exception here
                            Debug.LogError("The number of Source and Target models vertices don't match! " +
                                           "This is because the model was exported from VRoid Studio with <b>\"Delete Transparent Meshes\"</b> option checked. " +
                                           "This option is enabled by default in the <b>\"Reduce Polygon\"</b> export settings. " +
                                           "Make sure to uncheck it first and export the model again into this Unity project!\n\n" + ex.Message);

                            // Stop the function on error
                            return 0;
                        }
                    }
                }
            }

            //Save the changes to the target mesh
            //EditorUtility.SetDirty(targetModel);
            //AssetDatabase.SaveAssets();
            //AssetDatabase.Refresh();

            EditorUtility.DisplayDialog("Success!", sourceMesh.blendShapeCount + " blendshapes have been copied successfully!", "Yay!");

            return 1;
        }
    }
}
#endif