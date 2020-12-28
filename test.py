#C:/Users/Pichau/AppData/Local/Programs/Python/Python37/python.exe
# some_file.py
import sys,time
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/Downloads/0_Projetos/2020/0_addon/KeyFramePro_connection')

from keyframe_pro_client import KeyframeProClient
kpro_client = KeyframeProClient()
kpro_client.connect()
kpro_client.initialize()
kpro_client.get_range()

kpro_client.get_bookmarks(include_empty_timelines=True)

if kpro_client.connect() and kpro_client.initialize():
    kpro_client.get_range()

# Create a new timeline

    kpro_client.new_project(empty=True)
    timeline = kpro_client.add_timeline('My Timeline')

    sources = []
    sources.append(kpro_client.import_file(filepath))

    for source in sources:
        kpro_client.insert_element_in_timeline(source['id'], timeline['id'])

    # Make the timeline active in viewer A
    kpro_client.set_active_in_viewer(timeline['id'], 0)

#----------------------




#filepath = 'D:/Downloads/0_exercicios/Animation/Animation Workflow & Body Mechanics/shots/01-stomp-jump/render/1_stomp_spline_v2 0001.png'

filepath = bpy.context.scene.render.frame_path(frame=1) #pega endereco completo do render a partir do frame 1
#1_stomp_spline_v2 0371.png

viewport_anim = kpro_client.import_file(filepath)
#kpro_client.get_sources()
kpro_client.set_active_in_viewer(viewport_anim['id'], 0) #viewport A
kpro_client.set_active_in_viewer(viewport_anim['id'], 1) #viewport B



method to split

path = bpy.context.scene.render.filepath
full = bpy.context.scene.render.frame_path(frame=1)

split_temp = full.split('\\')
split_temp[len(split_temp)-1]

address=''
for n in range(0,len(split_temp)):
    if n == 0:
        address = split_temp[n]
    elif n != len(split_temp)-1:
        address=address + '\\'+ split_temp[n]
    else:
        address=address + '\\'+'A-' + split_temp[n]


kpro_client = KeyframeProClient()
# pegar o que esta no viewer A
if kpro_client.connect() and kpro_client.initialize():
    view_a = kpro_client.get_active_in_viewer(0)
    view_a['id']


    view_b = kpro_client.get_active_in_viewer(1)
    view_b['id']


    # kpro_client.set_viewer_layout(layout="single")
    # kpro_client.set_viewer_layout(layout="horizontal")
    kpro_client.set_viewer_layout(layout="vertical")
    view_a = kpro_client.get_active_in_viewer(0)


    kpro_client.set_active_in_viewer(view_a['id'], 0)



#C:/Users/Pichau/AppData/Local/Programs/Python/Python37/python.exe
# some_file.py
import sys,time
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/Downloads/0_Projetos/2020/0_addon/KeyFramePro_connection')
from keyframe_pro_client import KeyframeProClient
kpro_client = KeyframeProClient()
if kpro_client.connect() and kpro_client.initialize():
    view_a = kpro_client.get_active_in_viewer(0)


>>> view_a
{'duration': 1.7083330154418945, 'frame': 1, 'id': '{d2d9b16d-f9ce-4f80-a6aa-53f2fcefdc73}', 'is_source': True, 'name': 'A####.png 1-41', 'parent_id': '{7224ac20-42b2-4904-95df-aa581aca864d}', 'parent_index': 8, 'path': 'C:/tmp/A####.png 1-41', 'range_end': 41, 'range_start': 1, 'total_frames': 41}
>>> view_a = kpro_client.get_active_in_viewer(0)
[KPRO][ERROR] "get_active_in_viewer" timed out.
>>> if kpro_client.connect() and kpro_client.initialize():
...     view_a = kpro_client.get_active_in_viewer(0)
...
Traceback (most recent call last):
  File "D:\Downloads\0_Projetos\2020\0_addon\KeyFramePro_connection\keyframe_pro_client.py", line 107, in send
    self.__class__.kpro_socket.sendall(msg_str.encode())
ConnectionAbortedError: [WinError 10053] Uma conexão estabelecida foi anulada pelo software no computador host
>>> view_a = kpro_client.get_active_in_viewer(0)
>>> view_a
{'duration': 1.7083330154418945, 'frame': 1, 'id': '{eb292455-023e-4fa4-8243-e679f43a1afe}', 'is_source': True, 'name': 'B####.png 1-41', 'parent_id': '{7224ac20-42b2-4904-95df-aa581aca864d}', 'parent_index': 9, 'path': 'C:/tmp/B####.png 1-41', 'range_end': 41, 'range_start': 1, 'total_frames': 41}

kpro_client.set_active_in_viewer('{d2d9b16d-f9ce-4f80-a6aa-53f2fcefdc73}', 0)
kpro_client.set_active_in_viewer('{eb292455-023e-4fa4-8243-e679f43a1afe}', 0)