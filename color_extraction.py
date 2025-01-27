
import numpy as np
import cv2
import matplotlib.pyplot as plt
import pickle 

print('color_extraction.py')

def KMeans_clustering(k , img):
    height , width, _ = np.shape(img)
    imgarr_reshaped = np.reshape(img , (height * width, 3))
    imgarr = np.float32(imgarr_reshaped)
    
    cv2.setRNGSeed(32)
    number_of_clusters = k
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER , 10 , 1.0)
    # flags = cv2.KMEANS_RANDOM_CENTERS
    flags = cv2.KMEANS_PP_CENTERS
    compactness, labels , centroids = cv2.kmeans(imgarr, number_of_clusters, None, criteria, 10, flags)

    
    return sorted_centroids(labels, centroids) 


def sorted_centroids(labels, centroids):
    from collections import Counter
    
    label_frequency_counter = Counter(labels.flatten())
        
    sorted_frequencies = sorted(label_frequency_counter.items(), key = lambda x: x[1], reverse = True) #a list of tuples
    sorted_labels_list = [label for label,freq in sorted_frequencies]
    
    sorted_centroids_list  = centroids[sorted_labels_list]
    
    return sorted_centroids_list


# def show2(title , arr):
    
#     imsize = cv2.resize(arr , (600 , 400))
#     cv2.imshow(title , imsize)
    
#     cv2.waitKey(1)
#    # cv2.destroyAllWindows()



# def show(image_numpy_array , color_stack):
#     height , width, _ = np.shape(image_numpy_array)

#     fig,axs = plt.subplots(ncols = 1 , nrows = 2, height_ratios=[4, 1])
    
#     axs[0].imshow(image_numpy_array , interpolation='nearest')
#     axs[1].imshow(color_stack,  aspect='auto')
#     axs[0].axis('off')
#     axs[1].axis('off')
    
#     plt.show(block = True)


# def deserialize(serialized_frame):
    
#     img = pickle.loads(serialized_frame)
    
#     return img


# def create_bar(height, width, color):
    
#     bar = np.zeros((height, width, 3), np.uint8)
#     bar[:] = color
#     r , g, b = int(color[0]) , int(color[1]) , int(color[2])
    
#     return bar , (r,g,b)
    

# def extract_colors(img , number_of_dominant_colors):
#     height , width, _ = np.shape(img)
#     #print(height , width)

#     imgarr_reshaped = np.reshape(img , (height * width, 3))
#     imgarr = np.float32(imgarr_reshaped)
    
#     color_centroids = KMeans_clustering(number_of_dominant_colors , imgarr)
    
#     #create our color bar
#     bars = []
#     rgb_values = []

#     for index, row in enumerate(color_centroids):
#         bar , rgb = create_bar(50 , 50 , row)
        
#         bars.append(bar)
#         rgb_values.append(rgb)
        
#     colors_stack = np.hstack(bars)
    
#     return colors_stack
        
    
