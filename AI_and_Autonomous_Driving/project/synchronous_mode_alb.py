#!/usr/bin/env python

# Copyright (c) 2019 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import glob
import os
import sys





try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import logging
import random

try:
    import pygame
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')

try:
    import numpy as np
except ImportError:
    raise RuntimeError('cannot import numpy, make sure numpy package is installed')

try:
    import queue
except ImportError:
    import Queue as queue


def draw_image(surface, image):
    array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (image.height, image.width, 4))
    array = array[:, :, :3]
    array = array[:, :, ::-1]
    image_surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
    surface.blit(image_surface, (0, 0))


def get_font():
    fonts = [x for x in pygame.font.get_fonts()]
    default_font = 'ubuntumono'
    font = default_font if default_font in fonts else fonts[0]
    font = pygame.font.match_font(font)
    return pygame.font.Font(font, 14)


def should_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                return True
    return False

NUM = 0 
s = 'wrong image time-stampstamp: frame=%d, image.frame=%d'

#import queue

def main_carla():
    actor_list = []
    pygame.init()

    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)

    world = client.get_world()

    print('enabling synchronous mode.')
    settings = world.get_settings()
    settings.synchronous_mode = True
    world.apply_settings(settings)

    try:
        m = world.get_map()
        start_pose = random.choice(m.get_spawn_points())
        waypoint = m.get_waypoint(start_pose.location)

        blueprint_library = world.get_blueprint_library()
        
        #### Vehicle 
        vehicle = world.spawn_actor(random.choice(blueprint_library.filter('vehicle.*')), start_pose)
        actor_list.append(vehicle)
        #vehicle.set_simulate_physics(False)
        vehicle.apply_control(carla.VehicleControl(throttle=0.1, steer=0.0))
        vehicle.set_autopilot(False)
        
        
        #### Camera 
        camera = world.spawn_actor(
            blueprint_library.find('sensor.camera.rgb'),
            carla.Transform(carla.Location(x=-5.5, z=2.8), carla.Rotation(pitch=-15)),
            attach_to=vehicle)
        actor_list.append(camera)

        # Make sync queue for sensor data.
        image_queue = queue.Queue()
        camera.listen(image_queue.put)

        frame = None

        display = pygame.display.set_mode((800, 600),
            pygame.HWSURFACE | pygame.DOUBLEBUF)
        
        font = get_font()

        clock = pygame.time.Clock()

        while True:
            if should_quit():
                return

            clock.tick()
            world.tick()
            ts = world.wait_for_tick()

            if frame is not None:
                if ts.frame_count != frame + 1:
                    logging.warning('frame skip!')

            frame = ts.frame_count
            #####################################
            while True:
                image = image_queue.get()
                if image.frame_number == ts.frame_count:
                    break
                logging.warning(s,ts.frame_count,image.frame_number)
                

            draw_image(display, image)
            
            try:
                result = globals.q.get(False)
                #print(result)
                globals.veh_st.aply_control(vehicle)
                
            except queue.Empty:
                # Handle empty queue here
                pass
            else:
                # Handle task here and call q.task_done()
                globals.q.task_done()
            #print(NUM)
            text_surface = font.render('% 5d FPS' % clock.get_fps(), True, (255, 255, 255))
            display.blit(text_surface, (8, 10))
            
            text_autopilot= font.render('Autopilot = %s' % ('On' if globals.veh_st.autopilot else 'Off'), True, (255, 255, 255))
            display.blit(text_autopilot, (8, 25))
            
            pygame.display.flip()
            ##########################################
    finally:
        print('\ndisabling synchronous mode.')
        settings = world.get_settings()
        settings.synchronous_mode = False
        world.apply_settings(settings)

        print('destroying actors.')
        for actor in actor_list:
            actor.destroy()

        pygame.quit()
        print('done.')

from threading import Thread
from random import randint
import time


from AICA_V5_new import AICA_class, AICA_init_and_work


import globals 
  
if __name__ == '__main__':
    #global aica
    #aica = AICA_class(q)
    globals.initialize() 
    
    carla_thread = Thread(target=main_carla)
    carla_thread.daemon = True
    carla_thread.start()
    
    time.sleep(5)
    
    AICA_thread = Thread(target=AICA_init_and_work())
    AICA_thread.daemon = True
    AICA_thread.start()
    

#carla_thread = Thread(target=main_carla)#,name=name,args=(args))
   #AICA_thread = Thread(target=aica.run_app2)

#time.sleep(4)
#NUM = 6
#time.sleep(5)
#   
   # Wait for the threads to finish...
   #carla_thread.join()
#http://sebastiandahlgren.se/2014/06/27/running-a-method-as-a-background-thread-in-python/