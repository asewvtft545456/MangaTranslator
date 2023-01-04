# MangaTranslator
This is a program that translates manga primary from Japanese to English (tho it can also trans other languages to english).


# Installation
Clone or download the repository.
I recommend running the program within a virtual environment.

If you're using VScode, open the repository, go to the command pallete, type "Create Environment", and click.
Vscode will create the virtual environment and install everything in requirement.txt .

If you don't have VScode, open the repo within your IDE and go to the terminal:
1) Type "virtualenv venv"
2) Then activate the virtual environment by typing ".venv\Scripts\activate"
3) Finally, install the required packages by typing "pip install -r requirements.txt"

#Manga Translator
<img width="956" alt="image" src="https://user-images.githubusercontent.com/69278077/210460952-7684f6c5-efa3-4607-b6f2-f13980a01bff.png">
This is what the App looks like.
On the left, there are four buttons, Automatic, Manual, settings button, and a twitter button.

#Automatice Translation
By default, the app is set to automatic translation.
You can manipulate the automatic translation by clicking on the automatic button as seen below.
<img width="948" alt="image" src="https://user-images.githubusercontent.com/69278077/210461481-3e81c362-ade2-4836-9a34-188a2862de32.png">
The "Combine Overlap" checkbox combines overlapping rectangle and "Combine Neighbors" checkbox combines rectangles within a certain distance, which is decided by the slider. The "Retranslate current page" checkbox translates a single page if you don't like how that page turned out.
Example of automatic translation:
<img width="956" alt="image" src="https://user-images.githubusercontent.com/69278077/210462537-f7f853c7-ba1a-46a2-839a-5aead55cb638.png">

#Manual Translation
You can manually translate by clicking on the Manual button. You draw rectangles on the text you want translated.
Before:

<img width="960" alt="image" src="https://user-images.githubusercontent.com/69278077/210467473-fcf90aad-cd17-4c4e-af02-b795b112828f.png">

On the left, you change the color of the rectangles, the text, etc.

After:
<img width="960" alt="image" src="https://user-images.githubusercontent.com/69278077/210470169-ffe6b043-e9b3-4920-8c8c-c381f2c468ea.png">

#Settings button
The most important thing here is that you can change the translator. By default it is set to Bing.

#Twitter button
When you click on the the button, a bar will appear at the top. You can download "manga" from twitter.
<img width="945" alt="image" src="https://user-images.githubusercontent.com/69278077/210465637-d52a8f34-417b-4b4a-af28-131661562529.png">
Example of a valid link would be: https://twitter.com/sanka_kumaru/status/1589452581910335488


