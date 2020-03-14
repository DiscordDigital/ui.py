# ui.py
A basic dynamic terminal parser with arrow key and touch support using python3 ncurses.

## How to use:

1. Download ui.py to a linux or linux subsystem.
2. Make sure python3 is installed.
3. Run "python3 ui.py sample" to create an example file.
4. Load the example file with "python3 ui.py sample_ui.txt"
5. Test the terminal by click or using arrow keys.
6. Modify the sample_ui.txt and rename it to create a menu you like.

## Use cases:

* Use it to make shortcuts to some of your favorite linux commands
* Simplify user interfaces for remote servers. You can use ui.py through SSH with touch support.
* Create a touch menu in iOS apps like [iSH](https://github.com/tbodt/iSH) or any other terminal that has mouse support.

### Bugs

* Resizing the window may cause graphic bugs, terminal crashing or worse.\
  I've implemented some code to prevent that as much as possible, help would be appreciated.
*  If you size the objects higher than the screen size the code will fail, it's not a huge issue at the moment.
* Resizing will cause the cursor to appear on windows bash.exe even though it's technically disabled.
* The window may flash a little as you resize it, I could improve that in the future but I'd rather have the terminal resizing working fully before.
* Parsing invalid files will cause the terminal to crash.

#### What's not working and will probably never work

1. Support for Windows Python3 because Python3 ncurses is only for linux.
2. Touch scrolling, as a click is one interval and that'll reduce accuracy in selection dramatically.

**If your terminal crashes just enter the terminal command "reset" without the quotation marks.\
The terminal will reset and restore it's functionality. You may also restart the terminal if you prefer that.**
