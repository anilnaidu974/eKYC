# e-KYC

before running requirements.txt make sure you have CMake installed 
if not already installed, use the below command:

sudo apt-get install cmake (in Ubuntu)

Go to https://cmake.org/download/ link and download suitable file for windows users

# E-Kyc verification process

    1. Fill the e-kyc form (with mendatory fields)
    2. Upload a card (Pan card for now in the form itself)
    3. The form will now be verified against card details
    4. Once verified you will be redirected to Liveliness detection page
    5. Two step liveliness detection includes
        a. gesture matching
        b. eye blink detection
        PS : face recognition and matching is done in both the cases.
    6. Once both these things are verified you have successfully completed the ekyc verification.

# Workflow of text extraction
    1. Preprocess the uploaded card image : setting dpi of images (images of dpi(dots per inch) 300 perform better in ocr).
    2. Thresholding images according to V value in HSV , if the V value is greater than threshold then it is set to white and if not then black
    3. These thresholded images are passed to OCR as input.
    4. Remove the unordered text which includes anything that is not in the range of alphabets or numerals.
    5. Checking if the pan type is new pan or old pan card type.
    6. depending upon the type of pan card the information is extracted based on there relative location.
    7. Formatting the received text to remove any adultrated data.

# Workflow of Gesture Matching
    1. Specified a div tag in frontend to capture gesture(this is the roi of specific height and width)
    2. get the same roi in the backend from the image in a frame
    3. By spcifying a range of skin color we can create a mask and get the hand part
    4. Get contours and create a convex hull around it.
    5. Define area of hull and area of hand
    6. Find the persentage of area not covered by hand in the hull i.e arearatio
    7. Find defects in convex hull w.r.t hand i.e convexity defect (which is any cavity in the object)
    8. Depending upon calculation of number of defects and area ratio threshold we specify the type of defect.

# Workflow of Eye blink detection
    1. first we identify the location of eyes in the image
    2. Once the location is identified we can calculate the eye ratio
    3. The eye ratio is close to 0 when eyes are closed and constant when open
    4. Depending upon the number of times the ratio fluctuates we calculate the number of blinks.


