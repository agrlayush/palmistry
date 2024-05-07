# Fortune On Your Hand: View-Invariant Machine Palmistry
## Summary
Our *Palmistry principal lines detection software* is implemented by 4 steps below. 
Our main challenge was to read the principal lines on a palm regardless of the **view direction** and **illumination**:   
1) Warping a tilted palm image  
2) Detecting principal lines on a palm  
3) Classifying the lines  
4) Measuring the length of each line  
<img width="1362" alt="model_architecture" src="https://user-images.githubusercontent.com/81272473/208795260-48ba6c8f-92a1-4b01-9471-6a4703ad0aff.png">
For palm image rectification, we used MediaPipe to extract interest points and implemented warping with the points. For principal line detection, we built a deep learning model and trained the model with palm image dataset. For line classification, we used K-means clustering to allocate each pixel to specific line. For length measurement, we set a threshold for each principal line with the landmarks obtained by MediaPipe.

## Environment
The codes are written based on Python 3.7.6. These are the requirements for running the codes:
- torch
- torchvision
- scikit-image
- opencv-python
- pillow-heif
- mediapipe

In order to install the requirements, run `pip install -r ./code/requirements.txt`.

## Run
1. Before running the codes, **a palm image for input(.heic or .jpg)** should be prepared in the `./code/inputs` directory. We provided four sample inputs.
2. Run `read_palm.py` by the command below. After running the code, result files will be saved in the `./code/results` directory.
```bash
> python ./code/read_palm.py --input [filename].[jpg, heic]
```

## To run the Streamlit Application
```bash
> streamlit run app.py
```

## Results
<img width="1371" alt="standard" src="https://user-images.githubusercontent.com/81272473/208797334-9cf56f18-01b1-46e5-9bab-5a38a696d05f.png">
<img width="1361" alt="tilted" src="https://user-images.githubusercontent.com/81272473/208797357-fe007daf-0d24-48b0-80af-21d79b64db4a.png">

## Line Segment implementation
Update: 22.12.03 21:57
- Assumption
  - The line never reaches the border of the image (in this case, scikit's skeletonize often does not work. Even if it is skeletonized, the grouping algorithm needs to be slightly modified)
  - There can be at most one point where the lines intersect (according to the test case. It can be handled with some additional implementation)

- line grouping
  - return value : list of lines, each lines are also a list of pixels
  ```
  example : [ [[1, 2], [2, 3]], [[10, 11], [11, 11]] ]
  ```
  
  explanation of implementation
     1. Count non-zero values among the 8 pixels around all pixels.
     2. The count result is divided into 0: not on the line, 1: end of the line, 2: middle of the line, 3: intersection of the line.
     3. Starting from the pixel at the end of the line, search the surrounding 8 pixels, following pixels whose count is not 0 and that have not been visited.
     4. As you proceed, you will reach a pixel with a count of 1 or 3.
     5. If the pixel is 1, one line has been found, so save it and exclude it from the for statement to prevent reverse search. For the 3 pixels, the line should be saved separately for later action.
     6. Check whether lines ending in 3 can be connected: Check the difference between the start and end points and save all combinations with opposite directions in the line.
     7. Return the saved lines
    
## Issues
  - There are cases where skeletonize attaches a line that was not attached (1 case, one line appears slightly long) -> Additional testing is required
   - Processing of broken lines is ambiguous: Currently, it is ignored and proceeded with. It can be done by calculating the gradient of the grouped lines, but if done incorrectly, strange lines may be connected to each other. It seems like a good idea to hide cases like this...
