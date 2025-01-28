#uvicorn main:app
import numpy as np
import json
from video_parsing import get_video_information
from frame_handling import get_frame
from color_extraction import KMeans_clustering


from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)


class UserInput1(BaseModel):
    youtube_video_link: str


class UserInput2(BaseModel):
    streaming_link: str
    timestamp: str
    number_of_dominant_colors: int
    
    

  
@app.post("/colors")
async def show_colors(user_input : UserInput2):

    stream_link = user_input.streaming_link
    frame = get_frame(stream_link , user_input.timestamp)
    colors_npfloat32 = KMeans_clustering(user_input.number_of_dominant_colors , frame)
    colors_float = npfloat32_to_float(colors_npfloat32)

    return {'colors' : colors_float}

@app.post("/video")
async def show_video(user_input : UserInput1):

    video_info = get_video_information(user_input.youtube_video_link)

    return {'title' : video_info['title'], 'id' : video_info['id'], 'streaming_link' : video_info['url'] }


def npfloat32_to_float(list_of_lists):
    new_list = []
    for index ,rgb in enumerate(list_of_lists):
        #turning np.float32 type to float so javascript can accept it
        #also turning lists to tuples because pydantic handles them better
        new_list.append(tuple(rgb.astype(float)))
    
    print(new_list)
    return new_list
    
    
    
    
# if __name__ == '__main__':
#     input_ = {
#         'youtube_video_link' : 'https://www.youtube.com/watch?v=ox0hG51uQcs',
#         'timestamp' : '0:07',
#         'number_of_dominant_colors' : 10
#     }
    
#     result = post_(input_)
    
#     print(result['colors'])
#     show(result['image'] , result['colors'])
    
    