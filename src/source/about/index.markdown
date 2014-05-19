---
layout: page
title: "about"
date: 2014-05-14 08:56
comments: false
sharing: true
footer: true
---

{% img center http://scottsievert.github.io/images/tree-orig.png 440 %}

I'm rather interested in adaptive sampling and the new techniques compressed
sensing brings to the table. There are interesting places to look in any
signal, and most of our energy (aka time or money) should be focused there.

For example, thermal images are relatively simple; why not focus on the edges? That's where the detail, the most pertinent information lies. Or determining ages from a family portrait: the faces hold the information we're interested in. Prof. Jarvis Haupt, the advisor of our lab, has done [a great talk][talk] on finding the most interesting information.


This concept of detecting and estimating data present in a signal and using it to your advantage seems so natural and fascinates me, the reason I'll be getting my doctorate in it. My most up to date "course of life," my CV, is available [here][CV].

### Projects
My [Github][git] contains almost all of the code I work on. It has everything from research activities to small projects to this website.

#### Some specific projects of mine: 

* [iSparse][isparse]. An iOS app that reconstructs an image from *random* pixel
  samples. This relies on the image being [sparse][sparse] in the wavelet
  basis, meaning it relies on most of the image being of similar color.
* [IRcamera][ir]. A thermal camera that reconstructs an image after choosing
  the *best* places to look along with corresponding hardware. In essence, a
  "smarter" version of iSparse. This relies on the same assumptions as iSparse
  but adaptively chooses where to sample based on the Haar wavelet
  tree structure.
* [python-drawnow][drawnow]. Similar to MATLAB's `drawnow`.


[sparse]:https://en.wikipedia.org/wiki/Sparse_matrix
[drawnow]:https://github.com/scottsievert/python-drawnow
[git]:https://github.com/scottsievert
[talk]:http://nuit-blanche.blogspot.com/2013/08/sahd-compressive-saliency-sensing.html
[isparse]:https://github.com/scottsievert/iSparse
[ir]:https://github.com/scottsievert/IRcamera
[CV]:https://www.dropbox.com/s/lk0kifmjtzyq0y4/Scott_Sievert_CV.pdf
