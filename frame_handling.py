import cv2 #open cv for extracting and analysing frames.
import matplotlib.pyplot as plt

print('frame_handling.py')

    
# def serialize_frame_array(frame):
    
#     serialized_frame = pickle.dumps(frame)
    
#     return serialized_frame

def from_BGR_to_RGB(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

def convert_timestamp_to_sec(timestamp):

    [minutes , seconds] = timestamp.split(':')
    
    #print(minutes , seconds)
    return int(minutes) * 60 + int(seconds)

def get_frame(stream_link , time_in_ms):
    time_in_ms = int(time_in_ms)
    
    cap = cv2.VideoCapture(stream_link)
    print('opencv class is called successfully \n')

    #pass start time
    cap.set(cv2.CAP_PROP_POS_MSEC, time_in_ms)

    #pass end time which is the same as my start time 
    while True and cap.get(cv2.CAP_PROP_POS_MSEC) <= (time_in_ms):
            success, img = cap.read()
            img = from_BGR_to_RGB(img)
            break
    cap.release()
    
    print('end of frame_handling.py')

    return img





#insert into database the video title
#db.insert('FRAMES' , ['id'] , [id])

# print('insert your timestamp')
# timestamp = input() #format is --:--
# timestamp_in_sec = convert_timestamp_to_sec(timestamp)



# #start capturing of frames.
# cap = cv2.VideoCapture(stream_link)
# print('opencv class is called successfully \n')

# count = 1
# frame_num = 0
# #pass start time
# cap.set(cv2.CAP_PROP_POS_MSEC, timestamp_in_sec * 1000)

# #pass end time which is the same as my start time 
# while True and cap.get(cv2.CAP_PROP_POS_MSEC) <= (timestamp_in_sec * 1000):
#         success, img = cap.read()
#         img = from_BGR_to_RGB(img)
#         #cv2.imshow("Image", img)
#         #cv2.waitKey(0)
#         break
        
        
# while cap.isOpened():
    
#     grabbed, frame = cap.read()
#     if count % (fps * 30) == 0: #skipping half a minute
        
#         #In OpenCV, images are represented as 3 dimensional numpy arrays. 
#         # First two dimensions represent the number of pixels along the width 
#         # and the height of the image (number of columns and rows respectively in the numpy array) 
#         # and the third dimension represents the depth of color for the image.
#         #print(f'this is frame number {frame_num}:\n {str(frame)} \n')
        
#         #to be able to store my array in my database
        
#         frame_rgb = from_BGR_to_RGB(frame)
#         serialized_frame = serialize_frame_array(frame_rgb)
        
        
#         #insert frame into my database
#         #provide: table name , column name (frame_1, frame_2,..), value of frame in its serialized form, id of column
#         db.insert('FRAMES' , ["id" , "title" , f"frame_{frame_num}"] , [id, title , serialized_frame])
        
        
#         #this is a count for frames, helpful to create db column names and identify how many frames where captured.
#         frame_num += 1
#         print(frame_num)
        
#         cv2.waitKey(1)
        
#     count += 1
    

# cap.release()






