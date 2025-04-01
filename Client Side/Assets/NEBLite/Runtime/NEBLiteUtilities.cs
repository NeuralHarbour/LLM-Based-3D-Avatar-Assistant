using System.Collections;
using System.Collections.Generic;

#if UNITY_EDITOR
using UnityEditor;
using UnityEngine;

namespace NotEnoughBlendshape
{
    /// <summary>
    /// Contains all helper functions needed in NEBTool, like comparing two models, multiply Vector3, etc.
    /// </summary>
    public static class NEBLiteUtilities
    {
        /// <summary>
        /// Compare two gameobjects. This also compares if the same object is the 
        /// instanced model or asset model in the Project Window.
        /// </summary>
        /// <param name="model1"></param>
        /// <param name="model2"></param>
        /// <returns>True if the model is the same. Returns false otherwise.</returns>
        public static bool CheckIsModelDifferent(GameObject model1, GameObject model2)
        {
            if (model1 == null || model2 == null)
            {
                return true;
            }

            if (model1 == model2)
            {
                return false;
            }

            string prefabAssetPath1 = PrefabUtility.GetPrefabAssetPathOfNearestInstanceRoot(model1);
            string prefabAssetPath2 = PrefabUtility.GetPrefabAssetPathOfNearestInstanceRoot(model2);

            if (prefabAssetPath1 == null || prefabAssetPath2 == null)
            {
                return true;
            }

            if (prefabAssetPath1 == prefabAssetPath2)
            {
                return false;
            }

            return true;
        }

        /// <summary>
        /// Multiply all Vector3 in Vector3 array with a float.
        /// </summary>
        /// <param name="arrayList"></param>
        /// <param name="value"></param>
        /// <returns></returns>
        public static Vector3[] MultiplyVector3Array(Vector3[] arrayList, float value)
        {
            for (int i = 0; i < arrayList.Length; i++)
            {
                arrayList[i] *= value;
            }
            return arrayList;
        }

        /// <summary>
        /// Sum up every Vector3 element in two arrays.
        /// </summary>
        /// <param name="a"></param>
        /// <param name="b"></param>
        /// <returns>A new summed Vector3</returns>
        public static Vector3[] AddVector3Array(Vector3[] a, Vector3[] b)
        {
            Vector3[] result = new Vector3[a.Length];
            for (int i = 0; i < a.Length; i++)
            {
                result[i] = a[i] + b[i];
            }
            return result;
        }

        /// <summary>
        /// Given a name, return a new string that adds the number at the end of the input name.
        /// </summary>
        /// <param name="input"></param>
        /// <returns></returns>
        public static string FindUniqueName(string input)
        {
            //Find if there's a number at the end of the input string
            int lastNumberIndex = input.Length - 1;
            while (lastNumberIndex >= 0 && char.IsDigit(input[lastNumberIndex]))
            {
                lastNumberIndex--;
            }
            lastNumberIndex++;
            string baseString = input.Substring(0, lastNumberIndex);
            string numberString = input.Substring(lastNumberIndex);

            //Add that number by one if it ends with a number or just add 0.
            if (int.TryParse(numberString, out int existingNumber))
            {
                int newNumber = existingNumber + 1;
                string newString = baseString + newNumber.ToString();
                return newString;
            }
            else
            {
                return input + "0";
            }
        }
    }
}
#endif