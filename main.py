# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 14:58:59 2022

@author: get gd nub
"""

from soco import SoCo
import soco
import pygame
import time
import pygame
import cv2 
import numpy as np
import os
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
import tensorflow as tf
from object_detection.utils import config_util
from object_detection.protos import pipeline_pb2
from google.protobuf import text_format


#-------------------------------SET UP SONOS SPEAKERS---------------------------------------------------------------------------------------------------
device = soco.discover()
device

device = device.pop()
device.player_name

device.volume
device.volume = 57
#device.play()
#device.stop()
#device.status_light(led_on)

#-------------------------------SET UP OPEN CV---------------------------------------------------------------------------------------------------

WORKSPACE_PATH = 'Tensorflow/workspace'
SCRIPTS_PATH = 'Tensorflow/scripts'
APIMODEL_PATH = 'Tensorflow/models'
ANNOTATION_PATH = WORKSPACE_PATH+'/annotations'
IMAGE_PATH = WORKSPACE_PATH+'/images'
MODEL_PATH = WORKSPACE_PATH+'/models'
PRETRAINED_MODEL_PATH = WORKSPACE_PATH+'/pre-trained-models'
CONFIG_PATH = MODEL_PATH+'/my_ssd_mobnet/pipeline.config'
CHECKPOINT_PATH = MODEL_PATH+'/my_ssd_mobnet/'

CUSTOM_MODEL_NAME = 'my_ssd_mobnet' 
CONFIG_PATH = MODEL_PATH+'/'+CUSTOM_MODEL_NAME+'/pipeline.config'
config = config_util.get_configs_from_pipeline_file(CONFIG_PATH)

#-------------------------------LOAD MODEL---------------------------------------------------------------------------------------------------

# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(CONFIG_PATH)
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(CHECKPOINT_PATH, 'ckpt-11')).expect_partial()

@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections


category_index = label_map_util.create_category_index_from_labelmap(ANNOTATION_PATH+'/label_map.pbtxt')

# Setup capture
cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#-------------------------------RUN PYGAME---------------------------------------------------------------------------------------------------

def controller():
    
    pygame.init()
    
    #Pygame variables and fuctions
    clock = pygame.time.Clock()
    fps = 60
    
    #set panel size
    bottom_panel = 150
    screen_width = 800
    screen_height = 400 + bottom_panel
    screen = pygame.display.set_mode((screen_width, screen_height))
    
    #load sounds
    jitsu_input = pygame.mixer.Sound('files/Sounds/jutsu_input.mp3') 
    jitsu_complete = pygame.mixer.Sound('files/Sounds/jutsu_complete.wav')
       
    #load images
    background_img = pygame.image.load('files/Background/background.png').convert_alpha()
    stamp_img = pygame.image.load('files/Icons/stamp.png').convert_alpha()   
                        
    def draw_bg():
        screen.blit(background_img, (0, 0))
       
    def correct3():
        phase3 = True
        while phase3:
            ret, frame = cap.read()
            image_np = np.array(frame)
            
            input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
            detections = detect_fn(input_tensor)
            
            num_detections = int(detections.pop('num_detections'))
            detections = {key: value[0, :num_detections].numpy()
                          for key, value in detections.items()}
            detections['num_detections'] = num_detections
        
            # detection_classes should be ints.
            detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
            
            detections['num_detections'] = num_detections
            detections['hehe'] = np.array([(detections['detection_classes'] + 1),
                                           detections['detection_scores']])                                                
            
            label_id_offset = 1
            image_np_with_detections = image_np.copy()
        
            viz_utils.visualize_boxes_and_labels_on_image_array(
                        image_np_with_detections,
                        detections['detection_boxes'],
                        detections['detection_classes']+label_id_offset,
                        detections['detection_scores'],
                        category_index,
                        use_normalized_coordinates=True,
                        max_boxes_to_draw=5,
                        min_score_thresh=.5,
                        agnostic_mode=False)
        
            cv2.imshow('object detection',  cv2.resize(image_np_with_detections, (800, 600)))
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                break
            
            if detections['hehe'][1][0] > 0.5:
                     if detections['hehe'][0][0] == 12.0:
                        screen.blit(stamp_img, (575, 115))
                        jitsu_complete.play()
                        time.sleep(1)
                        device.play()
                        
                                                       
            pygame.display.update()    
       
                             
            
    def correct2():
        correct2 = True
        while correct2:
            ret, frame = cap.read()
            image_np = np.array(frame)
            
            input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
            detections = detect_fn(input_tensor)
            
            num_detections = int(detections.pop('num_detections'))
            detections = {key: value[0, :num_detections].numpy()
                          for key, value in detections.items()}
            detections['num_detections'] = num_detections
        
            # detection_classes should be ints.
            detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
            
            detections['num_detections'] = num_detections
            detections['hehe'] = np.array([(detections['detection_classes'] + 1),
                                           detections['detection_scores']])                                                
            
            label_id_offset = 1
            image_np_with_detections = image_np.copy()
        
            viz_utils.visualize_boxes_and_labels_on_image_array(
                        image_np_with_detections,
                        detections['detection_boxes'],
                        detections['detection_classes']+label_id_offset,
                        detections['detection_scores'],
                        category_index,
                        use_normalized_coordinates=True,
                        max_boxes_to_draw=5,
                        min_score_thresh=.5,
                        agnostic_mode=False)
        
            cv2.imshow('object detection',  cv2.resize(image_np_with_detections, (800, 600)))
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                break
            
            if detections['hehe'][1][0] > 0.5:
                    if detections['hehe'][0][0] == 6.0:
                        screen.blit(stamp_img, (410, 115))
                        jitsu_input.play()
                        correct3()
                            
            pygame.display.update()    
                            
       
    def correct1():
        correct1 = True
        while correct1:
            ret, frame = cap.read()
            image_np = np.array(frame)
            
            input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
            detections = detect_fn(input_tensor)
            
            num_detections = int(detections.pop('num_detections'))
            detections = {key: value[0, :num_detections].numpy()
                          for key, value in detections.items()}
            detections['num_detections'] = num_detections
        
            # detection_classes should be ints.
            detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
            
            detections['num_detections'] = num_detections
            detections['hehe'] = np.array([(detections['detection_classes'] + 1),
                                           detections['detection_scores']])                                                
            
            label_id_offset = 1
            image_np_with_detections = image_np.copy()
        
            viz_utils.visualize_boxes_and_labels_on_image_array(
                        image_np_with_detections,
                        detections['detection_boxes'],
                        detections['detection_classes']+label_id_offset,
                        detections['detection_scores'],
                        category_index,
                        use_normalized_coordinates=True,
                        max_boxes_to_draw=5,
                        min_score_thresh=.5,
                        agnostic_mode=False)
        
            cv2.imshow('object detection',  cv2.resize(image_np_with_detections, (800, 600)))
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                break         
            
            if screen.blit(stamp_img, (78, 115)):
                if detections['hehe'][1][0] > 0.5:
                        if detections['hehe'][0][0] == 9.0:
                            screen.blit(stamp_img, (245, 115))
                            jitsu_input.play()
                            correct2()
                            
            pygame.display.update()
            
    
      
       
    
    iot_remote = True
    while iot_remote:
        
        clock.tick(fps) 
   
        #-------------------------------RUN OPENCV WEBCAM---------------------------------------------------------------------------------------------------
        
        #run opencv in back ground
        ret, frame = cap.read()
        image_np = np.array(frame)
        
        input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
        detections = detect_fn(input_tensor)
        
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                      for key, value in detections.items()}
        detections['num_detections'] = num_detections
    
        # detection_classes should be ints.
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
        
        detections['num_detections'] = num_detections
        detections['hehe'] = np.array([(detections['detection_classes'] + 1),
                                       detections['detection_scores']])
        
        #fireball jitsu phrase
        
        label_id_offset = 1
        image_np_with_detections = image_np.copy()
    
        viz_utils.visualize_boxes_and_labels_on_image_array(
                    image_np_with_detections,
                    detections['detection_boxes'],
                    detections['detection_classes']+label_id_offset,
                    detections['detection_scores'],
                    category_index,
                    use_normalized_coordinates=True,
                    max_boxes_to_draw=5,
                    min_score_thresh=.5,
                    agnostic_mode=False)
    
        cv2.imshow('object detection',  cv2.resize(image_np_with_detections, (800, 600)))
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break
        
        #-------------------------------DRAW PYGAME FEATURES---------------------------------------------------------------------------------------------------
        
        #draw background
        draw_bg()
        
        if detections['hehe'][1][0] > 0.5:
                if detections['hehe'][0][0] == 11.0:
                    jitsu_input.play() 
                    screen.blit(stamp_img, (75, 115))   
                    correct1()   
                    
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                iot_remote = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False
    
        pygame.display.update()
        
controller()
        
            
