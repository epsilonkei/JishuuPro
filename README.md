# JishuuPro
My works in JishuuPro
* JishuuPro is a small project for 3rd students in Department of Mechano-Informatics, The University of Tokyo.
* In this project, I developed a fully automatic arm robot to solving Pazudora([パズドラ](https://ja.wikipedia.org/wiki/パズル%26ドラゴンズ)) - a smartphone game.

## Images
Here are some images from my work

### Sketch and CAD data
<p float="left">
  <img src="https://github.com/epsilonkei/JishuuPro/blob/master/images/Sketch.jpg" alt="Sketch" 
  width="whatever" height=400>
  <img src="https://github.com/epsilonkei/JishuuPro/blob/master/images/CAD.png" alt="CAD_design" 
  width="whatever" height=400>
</p>

### Solenoid and Circuit
<p float="left">
  <img src="https://github.com/epsilonkei/JishuuPro/blob/master/images/Solenoid.jpg" alt="Solenoid" 
  width="whatever" height=520>
  <img src="https://github.com/epsilonkei/JishuuPro/blob/master/images/Circuit.jpg" alt="Circuit" 
  width="whatever" height=520>
</p>

### Image Processing with HSV Filter
#### Full Original Image and Cropped Image
<p float="left">
  <img src="https://github.com/epsilonkei/JishuuPro/blob/master/images/full_image.jpg" 
  alt="Full Original Image" width="whatever" height=290>
  <img src="https://github.com/epsilonkei/JishuuPro/blob/master/images/cropped_image.jpg" 
  alt="Cropped Image" width="whatever" height=290>
</p>

#### HSV Filter result
<p float="left">
  <img src="https://github.com/epsilonkei/JishuuPro/blob/master/images/red.jpg" 
  alt="Red Filter" width="whatever" height=180>
  <img src="https://github.com/epsilonkei/JishuuPro/blob/master/images/blue.jpg" 
  alt="Blue Filter" width="whatever" height=180>
  <img src="https://github.com/epsilonkei/JishuuPro/blob/master/images/green.jpg" 
  alt="Green Filter" width="whatever" height=180>
</p>

<p float="left">
  <img src="https://github.com/epsilonkei/JishuuPro/blob/master/images/pink.jpg" 
  alt="Pink Filter" width="whatever" height=180>
  <img src="https://github.com/epsilonkei/JishuuPro/blob/master/images/yellow.jpg" 
  alt="Yellow Filter" width="whatever" height=180>
  <img src="https://github.com/epsilonkei/JishuuPro/blob/master/images/violet.jpg" 
  alt="Violet Filter" width="whatever" height=180>
</p>


### Pazudora Solver
#### Example 1:
<img src="https://github.com/epsilonkei/JishuuPro/blob/master/images/pazu_quiz1.gif" 
  alt="Pazudora quiz 1" width="whatever" height=320>
#### Example 2:
<img src="https://github.com/epsilonkei/JishuuPro/blob/master/images/pazu_quiz2.gif" 
  alt="Pazudora quiz 2" width="whatever" height=320>

### Machine Overview
<img src="https://github.com/epsilonkei/JishuuPro/blob/master/images/Machine_overview.jpg" alt="Machine Overview" 
  width="whatever" height=580>

### Snapshot from demo
<img src="https://github.com/epsilonkei/JishuuPro/blob/master/images/Snapshot_from_demo.png" alt="Snapshot from demo" 
  width="whatever" height=450>

## Demo
You can see a demo of my project [here](https://www.youtube.com/watch?v=YnBVweda7Wo)

## Memo for demo 
* Raspberry Pi need RPi.GPIO for driving motor, solenoid ... To install run
```
sudo pip install rpi.gpio
```
or
```
sudo apt-get install python-rpi.gpio
```
* There are a lot of unnecessary and duplicated code in this repository.
* For running demo, the minimum necessary code are put in ```PazuSolverMachine``` directory
* For camera position adjust: ```python camera_adjust.py```
* Running demo command (probably):
  * In Rasberrry Pi: ```python Machineclient.py```
  * In PC: 
    * for only one solving step: ```python PCserver.py``` 
    * for solving continuously: ```python PCserverMulti.py```
