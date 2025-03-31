<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/NeuralHarbour/LLM-Based-3D-Avatar-Assistant">
    <img src="Images/logo_new.png" alt="Logo" width="450" height="160">
  </a>
</div>

<h3 align="center">LLM Based Holographic Assistant</h3>
<p align="center">Shaping Perspectives Shifting Realities</p>

<div align="center">
    <a href="https://github.com/NeuralHarbour/LLM-Based-3D-Avatar-Assistant" target="_blank">
        <img src="https://img.shields.io/badge/made_with-%E2%9D%A4-red?style=for-the-badge&labelColor=pink" alt="madewithlove">
    </a>
    <h4>Follow Us</h4>
    <a href="https://huggingface.co/NeuralHarbourAI" target="_blank">
        <img src="https://img.shields.io/badge/🤗%20-Spaces-yellow.svg?style=for-the-badge" alt="Huggingface Spaces">
    </a>
    <a href="https://x.com/NeuralHarbourAI" target="_blank">
        <img src="https://img.shields.io/badge/X-%2312100E.svg?style=for-the-badge&logo=x&logoColor=white" alt="X">
    </a>
    <a href="https://www.linkedin.com/company/neuralharbour-ai/?viewAsMember=true" target="_blank">
        <img src="https://img.shields.io/badge/LinkedIn-%230A66C2.svg?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
    </a>
    <a href="https://instagram.com/neuralharbourai" target="_blank">
        <img src="https://img.shields.io/badge/Instagram-%23E4405F.svg?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram">
    </a>
</div>

<p align="center">
  <a href="https://count.getloli.com" target="_blank">
    <img alt="Moe Counter!" src="https://count.getloli.com/@Moe-counter.github?name=Moe-counter.github&theme=booru-lewd&padding=7&offset=7&align=top&scale=1&pixelated=0&darkmode=auto">
  </a>
</p>


<!-- ABOUT THE PROJECT -->
## About The Project

A virtual waifu / assistant that you can speak to through your mic and it'll speak back to you! Has many features such as:

* You can speak to her with a mic
* It can speak back to you
* It can recognize gestures and perform appropriate actions based on it
* Has dynamic voice controls
* Has short-term memory and long-term memory
* Can open apps
* Smarter than you
* Multilingual
* Can learn psychology
* Can recognize different people
* Can sing,dance do lot of other stuff.
* Can control your smart home like Alexa
* Dynamic animations

More features I'm planning to add soon in the [Roadmap](https://github.com/NeuralHarbour/LLM-Based-3D-Avatar-Assistant/v2.0#roadmap). Also, here's a summary of how it works for those of you who want to know:

First the speech which is obtained from the mic is first passed into the OpenAI Whisper model for detecting the language of the speech and then its passed on to the speech recognizer, 
the response is then sent to the client via a websocket, the transcribed text is then sent to gemini LLM, and the response from Jenna is printed to the unity console and appended to conversation_log.json, 
and finally, the response is spoken by our finedtuned Parler TTS with the expressions for the face of the character and voice and the animation will be dynamically generated for the character by our own custom animation model which we are currently working on. For the time being we are using preset animations.

Created Based on our publication
https://ieeexplore.ieee.org/document/10576146

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [Python](https://www.python.org)
* [Langchain 3.0](https://github.com/langchain-ai/langchain)
* [Whisper](https://openai.com/research/whisper)
* [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
* [PocketSphinx](https://pypi.org/project/pocketsphinx/)
* [Parler TTS](https://github.com/huggingface/parler-tts)
* [HyperDB](https://github.com/jdagdelen/hyperDB)
* [Sentence Transformers](https://github.com/UKPLab/sentence-transformers)
* [Tuya Cloud IoT](https://iot.tuya.com/)
* [Unity 2024](https://unity.com/)
* Unity C#
* Rust
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

1. [Install Python 3.10.11](https://www.python.org/downloads/release/python-31011/) and set it as an environment variable in PATH For both Pythonscripting and Default python shell
2. [Install GIT](https://git-scm.com/downloads)
3. [Install CUDA 11.7 if you have an Nvidia GPU](https://developer.nvidia.com/cuda-11-7-0-download-archive?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exe_local)
4. [Install Visual Studio Community 2022](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community&channel=Release&version=VS2022&source=VSLandingPage&cid=2030&passive=false) and select `Desktop Development with C++` in the install options
5. Install Unity
6. Install [FFMPEG](https://ffmpeg.org/)
7. Unity packages such as UniVRM,ULipSync,PythonScripting, Readspeaker TTS(Temporary)

## How to run / Steps to reproduce
<br>
1. Create a new project in unity with URP Settings
<br>
<br>
<img src="Images/Step1.png" alt="Step1" width="600" height="280">
<br>
2. Replace the assets folder with the one in this branch
<br>
<br>
3. Open the Unity Scene from the scenes folder
<br>
<br>
<img src="Images/Step3.png" alt="Step3" width="600" height="280">
<br>
4. Insert the API keys into the .env files
<br>
<br>
<img src="Images/Step4.png" alt="Step4" width="600" height="280">
<br>
5. Run the STT service using: <strong>python STT.py</strong>
<br>
<br>
6. Launch the app by clicking on the play button
<br>
<br>
7. Wait for the application to download the required models on the first start
<br>
<br>
8. Say 'Start' to activate or 'Stop' to deactivate works like an OS
<br>
<br>
<img src="Images/Output.png" alt="output" width="280" height="500">
<br>

Compiled EXE version coming soon !!!

<!-- ROADMAP -->
## Roadmap

- [x] Long-term memory
- [x] Time and date awareness
- [ ] mixed reality integration
- [x] Gatebox-style hologram
- [x] Dynamic Voice like GPT4o
- [ ] Alexa-like smart home control
- [x] Multilingual
- [ ] Mobile version
- [x] Easier setup
- [ ] Compiling into one exe
- [x] Localized
- [ ] Home Control
- [ ] Outfit Change
- [ ] Add custom skills
- [ ] Music Player
- [ ] Different modes
- [ ] Face Recognition
- [ ] Dynamic Animations
- [X] OS like working
- [X] Wakeword detection
- [ ] Mood recognition
- [ ] Weather Forecast

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GNU Affero General Public License v3.0 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact and Socials

E-mail: support@neuralharbour.com
<br>
Project Link: [https://github.com/NeuralHarbour/LLM-Based-3D-Avatar-Assistant/v2.0](github.com/NeuralHarbour/LLM-Based-3D-Avatar-Assistant/v2.0)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Choose an Open Source License](https://choosealicense.com)
* [AI Waifu Vtuber](https://github.com/ardha27/AI-Waifu-Vtuber)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
