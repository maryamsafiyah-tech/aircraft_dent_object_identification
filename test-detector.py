from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
# import pandas as pd
import csv  

#path to file containing image file
path = r'C:\Users\Student\miniconda3\AI-102-AIEngineer\18-object-detection\Python\test-detector\Case 1'

def main():
    from dotenv import load_dotenv

    try:
        # Get Configuration Settings
        load_dotenv()
        prediction_endpoint = os.getenv('PredictionEndpoint')
        prediction_key = os.getenv('PredictionKey')
        project_id = os.getenv('ProjectID')
        model_name = os.getenv('ModelName')

        # Authenticate a client for the training API
        credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
        prediction_client = CustomVisionPredictionClient(endpoint=prediction_endpoint, credentials=credentials)

        # Load image and get height, width and channels
        # path = r’C:\Users\Student\miniconda3\AI-102-AIEngineer\18-object-detection\Python\test-detector\Case 1’        
        # for image in os.listdir(path):
        
        image_file = 'IMG_2625.JPG'
        print('Detecting objects in', image_file)
        image = Image.open(image_file)
        h, w, ch = np.array(image).shape

        # Detect objects in the test image
        with open(image_file, mode="rb") as image_data:
            results = prediction_client.detect_image(project_id, model_name, image_data)

        # Create a figure for the results
        fig = plt.figure(figsize=(8, 8))
        plt.axis('off')

        # Display the image with boxes around each detected object
        draw = ImageDraw.Draw(image)
        lineWidth = int(w/100)
        color = 'magenta'
        for prediction in results.predictions:
            # Only show objects with a > 50% probability
            if (prediction.probability*100) > 50:
                # Box coordinates and dimensions are proportional - convert to absolutes
                left = prediction.bounding_box.left * w 
                top = prediction.bounding_box.top * h 
                height = prediction.bounding_box.height * h
                width =  prediction.bounding_box.width * w
                volume = height*width
                # Draw the box
                points = ((left,top), (left+width,top), (left+width,top+height), (left,top+height),(left,top))
                draw.line(points, fill=color, width=lineWidth)
                # Add the tag name and probability
                plt.annotate(prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100),(left,top), backgroundcolor=color)
                header = ['box_left', 'box_top', 'height', 'width', 'volume']
                data = [left, top, height, width, volume]

                with open('dent_data.csv', 'a', encoding='UTF8') as f:
                    writer = csv.writer(f)

                    # write the header
                    writer.writerow(header)

                    # write the data
                    writer.writerow(data)
        volume +=volume
        plt.imshow(image)
        outputfile = 'output.jpg'
        fig.savefig(outputfile)
        print('Results saved in ', outputfile)
        print('The total detection volume for dent =',volume)
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()
