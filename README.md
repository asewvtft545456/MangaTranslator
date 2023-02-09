# MangaTranslator
This is a program that translates manga primary from Japanese to English (tho it can also trans other languages to english).


# Installation
Clone or download the repository.
I recommend running the program within a virtual environment.

If you're using VScode, open the repository, go to the command pallete, type "Create Environment", and click.
Vscode will create the virtual environment and install everything in requirement.txt. If it doesn't type "pip install -r requirements.txt" in the terminal.

If you don't have VScode, open the repo within your IDE and go to the terminal:
1) Type "virtualenv venv"
2) Then activate the virtual environment by typing ".venv\Scripts\activate"
3) Finally, install the required packages by typing "pip install -r requirements.txt"
4) Run Main.py

# Manga Translator
<img width="958" alt="image" src="https://user-images.githubusercontent.com/69278077/211099677-dd379e6d-bd13-4b0d-bd21-9fd0a16d02a7.png">
This is what the App looks like.
On the left, there are four buttons, Automatic, Manual, settings button, and a twitter button.

# Automatic Translation
By default, the app is set to automatic translation.
You can manipulate the automatic translation by clicking on the automatic button as seen below.

<img width="960" alt="image" src="https://user-images.githubusercontent.com/69278077/211103025-e0edbf01-1aa4-4e8c-877b-87d7d5f520f4.png">
The "Combine Overlap" checkbox combines overlapping rectangle and "Combine Neighbors" checkbox combines rectangles within a certain distance, which is decided by the slider. The "Retranslate current page" checkbox translates a single page if you don't like how that page turned out.
Example of automatic translation:
<img width="959" alt="image" src="https://user-images.githubusercontent.com/69278077/211103416-f477dbd3-d2b0-4694-899d-92e51b427ff0.png">

# Manual Translation
You can manually translate by clicking on the Manual button. You draw rectangles on the text you want translated.
On the left, you change the color of the rectangles, the text, etc.

Before:
<img width="960" alt="image" src="https://user-images.githubusercontent.com/69278077/211103970-567fb100-cfa5-4d82-bf34-a4d0fcb1e57a.png">

After:

<img width="958" alt="image" src="https://user-images.githubusercontent.com/69278077/211103803-e8b966fe-8131-4edc-97e5-ad8323dce7cb.png">

# Settings button
The most important thing here is that you can change the translator. By default it is set to Bing.

# Twitter button
When you click on the the button, a bar will appear at the top. You can download "manga" from twitter.
<img width="959" alt="image" src="https://user-images.githubusercontent.com/69278077/211104107-0fd81112-0f97-4ad9-b823-cf2ac41be847.png">
You need to sign up on https://developer.twitter.com to the API key and other required keys.

Example of a valid link would be: https://twitter.com/sanka_kumaru/status/1589452581910335488


