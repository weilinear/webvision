# WebVision
This package provides simple functions to verify and evaluate WebVision dataset. [WebVision Workshop](http://www.vision.ee.ethz.ch/webvision/workshop.html "WebVision Workshop") will be held in conjunction with CVPR 2017.

* Dataset Specification is in config.py.
* Commandline is util.py.
  1. The following command will verify the integrity of the downloaded dataset according to path specified in config.py

     ```$ python util.py --validate```
  2. The following command will evaluate a validation result with top-k accurarcy.

     ```$ python util.py --eval_val /path/to/val.txt --top_k 5```
