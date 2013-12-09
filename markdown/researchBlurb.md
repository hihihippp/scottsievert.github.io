### Thermal Camera
Current thermal cameras, meaning infrared (IR) cameras are often very expensive
(4,000-40,000 dollars), but a Raspberry Pi, stepper motors,  single sensor
and some complicated signal processing is only about 400 bucks. Making a camera
that goes to *every* pixel location is easy, but results in a [not-so-great
picture][bad_pic] and a long exposure time. Using edge detection through the
Haar wavelet transform, we're able to get a better image with a shorter
exposure time and less cost.

[bad_pic]:https://raw.github.com/scottsievert/IRcamera/master/temp.rpi/IRcamera/full.png

### iPhone app
Under the direction of Prof. Jarvis Haupt, I have made [an app][app] to show other
cross-disciplinary fields what is possible with signal processing. It takes an
image, then randomly deletes some data and then reconstructs the original
image through the Fast Iterative Shrinkage-Thresholding Algorithm (FISTA). This
work is parallel in many ways to image in-painting, but has much broader
implications.

[app]:https://github.com/scottsievert/iSparse

### Granular Flows 
I wrote a [C++ program][c++] to analyze a granular flow of
two different sized sands. This analysis required the use of a high speed
camera and tracked many different sand particles (using a light's reflection).
It converted to real units, corrected for camera distortion, found the flow
direction and elimented erronous date -- an intensive process. Because this
anaylsis tracked so many particles, it took a long time. I deployed the
computer vision program (which I modified) to find these particles on Amazon's
EC2 servers to reduce the computation time.

[c++]:https://github.com/scottsievert/Granular-Flows-Image-Analysis

#### Undergraduate Research Opportunities (UROP)
**Piezoelectric wind energy scheme, optimizing for width and separation**: Advisor: Prof. Robbins, [report][wind].
<p>
**Stripes in granular flows under special conditions, and seeing the effects of
speed and angular velocity**: Advisor: Prof. Hill,
[report][gran].


##### Class Explorations
[Estimating the weather from remote locations.](blog/Predicting Weather.html)


[wind]:http://purl.umn.edu/120427
[gran]:http://purl.umn.edu/113663

