# EyeSpeak
WORK IN PROGRESS


EyeSpeak is an app that provides accessible and easy computer access to the paralytic, allowing them to perform simple computer actions in their daily lives. It is designed to allow for people to be able to type a letter, send an email, browse the internet, play video games, and enjoy the ability to use a computer when they were not able to before.

- Speech Keyboard: Using speech recognition and speech-to-text, user speech is converted into corresponding keystrokes or keyboard commands when specified.  Two modes are included: 1) Typing, the default mode, and 2) Gaming, which allows movement in games to be dictated with user speech.
- Face-Tracking: Using OpenCV and MediaPipe solution, the user's head and face movements are detected.  Mouse movements are done by calculating the pitch (vertical rotation) and yaw (horizontal rotation) of the user's head.  Left clicks or right clicks correspond to a left wink or right wink.
- Eye-Tracking (under revision): Using OpenCV and EyeGestures solution, the user's gaze correponds to mouse movements.  Clicks can also be executed by blinking/winking.
