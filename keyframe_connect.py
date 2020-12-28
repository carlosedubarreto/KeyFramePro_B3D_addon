import datetime
import os
import shutil
import subprocess
import sys
import time
import traceback
import bpy
from bpy import context
from bpy.app.handlers import persistent
from . keyframe_pro_client import KeyframeProClient
# from . panel import Panel_kfp



global percent_render_var
def load_video(context, filepath, use_some_setting):
    kpro_client = KeyframeProClient()
    if kpro_client.connect() and kpro_client.initialize():
    # Create a new timeline

        kpro_client.new_project(empty=True)
        timeline = kpro_client.add_timeline('My Timeline')

        sources = []
        sources.append(kpro_client.import_file(filepath))

        for source in sources:
            kpro_client.insert_element_in_timeline(source['id'], timeline['id'])

        # Make the timeline active in viewer A
        kpro_client.set_active_in_viewer(timeline['id'], 0)
    return {'FINISHED'}

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
class ImportSomeData(Operator, ImportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "import_test.some_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Import Some Data"

    # ImportHelper mixin class uses this
    filename_ext = ".mp4"

    filter_glob: StringProperty(
        default="*.mp4",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting: BoolProperty(
        name="Example Boolean",
        description="Example Tooltip",
        default=True,
    )

    type: EnumProperty(
        name="Example Enum",
        description="Choose between two items",
        items=(
            ('OPT_A', "First Option", "Description one"),
            ('OPT_B', "Second Option", "Description two"),
        ),
        default='OPT_A',
    )

    def execute(self, context):
        return load_video(context, self.filepath, self.use_setting)



from datetime import datetime, timedelta 
class Play_video(bpy.types.Operator):
    bl_idname = "view3d.play"
    bl_label = "Play"
    bl_description = "Play on KeyframePro"

    def execute(self, context):
        kpro_client = KeyframeProClient()
        if kpro_client.connect() and kpro_client.initialize():
            # kpro_client.set_frame(100, audio=False, from_range_start=False)
            kpro_client.set_playing(True, play_forwards=True)
            bpy.context.scene.frame_set(kpro_client.get_frame() - offset_kfp)

            # while kpro_client.connect():
                # print('kf frame :', kpro_client.get_frame())
        return{'FINISHED'}



class Stop_video(bpy.types.Operator):
    bl_idname = "view3d.stop"
    bl_label = "stop"
    bl_description = "Stop Playing on KeyFrame"

    def execute(self, context):
        kpro_client = KeyframeProClient()
        if kpro_client.connect() and kpro_client.initialize():
            kpro_client.set_playing(False, play_forwards=True)
            bpy.context.scene.frame_set(kpro_client.get_frame() - offset_kfp)
        return{'FINISHED'}


class First_frame(bpy.types.Operator):
    bl_idname = "view3d.first_frame"
    bl_label = "First Frame"
    bl_description = "Go to First Frame on Keyframe Pro"

    def execute(self, context):
        kpro_client = KeyframeProClient()
        if kpro_client.connect() and kpro_client.initialize():
            frames = kpro_client.get_range()
            kpro_client.set_frame(frames[0], audio=False, from_range_start=False)
            bpy.context.scene.frame_set(kpro_client.get_frame() - offset_kfp)
        return{'FINISHED'}

class Last_frame(bpy.types.Operator):
    bl_idname = "view3d.last_frame"
    bl_label = "Last Frame"
    bl_description = "Go to Last Frame on Keyframe Pro"

    def execute(self, context):
        kpro_client = KeyframeProClient()
        if kpro_client.connect() and kpro_client.initialize():
            frames = kpro_client.get_range()
            kpro_client.set_frame(frames[1], audio=False, from_range_start=False)
            bpy.context.scene.frame_set(kpro_client.get_frame() - offset_kfp)
        return{'FINISHED'}

class Prev_frame(bpy.types.Operator):
    bl_idname = "view3d.prev_frame"
    bl_label = "Previous Frame"
    bl_description = "Go to previous Frame on Keyframe Pro"

    def execute(self, context):
        kpro_client = KeyframeProClient()
        if kpro_client.connect() and kpro_client.initialize():
            frame = kpro_client.get_frame()
            kpro_client.set_frame(frame-1, audio=False, from_range_start=False)
            bpy.context.scene.frame_set(kpro_client.get_frame() - offset_kfp)
        return{'FINISHED'}

class Next_frame(bpy.types.Operator):
    bl_idname = "view3d.next_frame"
    bl_label = "Next Frame"
    bl_description = "Go to prenext Frame on Keyframe Pro"

    def execute(self, context):
        kpro_client = KeyframeProClient()
        if kpro_client.connect() and kpro_client.initialize():
            frame = kpro_client.get_frame()
            kpro_client.set_frame(frame+1, audio=False, from_range_start=False)
            bpy.context.scene.frame_set(kpro_client.get_frame() - offset_kfp)
        return{'FINISHED'}

class Register_Timer(bpy.types.Operator):
    bl_idname = "view3d.register_timer"
    bl_label = "register"
    bl_description = "Register Timer"

    def execute(self, context):
        bpy.app.timers.register(frame_kfp_to_bl.frame_kfp_get)
        return{'FINISHED'}

class Unregister_Timer(bpy.types.Operator):
    bl_idname = "view3d.unregister_timer"
    bl_label = "unregister"
    bl_description = "Unregister Timer"

    def execute(self, context):
        bpy.app.timers.unregister(frame_kfp_to_bl.frame_kfp_get)
        return{'FINISHED'}

class frame_bl_to_kfp(bpy.types.Operator):
    bl_idname = "view3d.frame_bl_to_kfp"
    bl_label = "frame"
    bl_description = "frame from Blender to Keyframe"

    def execute(self, context):
        kpro_client = KeyframeProClient()
        if kpro_client.connect() and kpro_client.initialize():
            # frame = bpy.data.scenes["Scene"].frame_current
            frame = bpy.context.scene.frame_current + offset_kfp
            kpro_client.set_frame(frame, audio=False, from_range_start=False)
            # kpro_client.set_frame(frame, audio=context.scene.my_tool.bool_sound, from_range_start=False)
            # kpro_client.set_playing(False, play_forwards=True)
        return{'FINISHED'}


class frame_kfp_to_bl(bpy.types.Operator):
    bl_idname = "view3d.frame_kfp_to_bl"
    bl_label = "frame"
    bl_description = "frame from KeyFrame to Blender"

    def execute(self, context):
        kpro_client = KeyframeProClient()
        if kpro_client.connect() and kpro_client.initialize():
            # frame = bpy.data.scenes["Scene"].frame_current
            frame = kpro_client.get_frame() - offset_kfp
            bpy.context.scene.frame_set(frame)
        return{'FINISHED'}



    global frame_kfp,kfp_change_bl,bl_change_kfp,frame_bl,offset_bl,offset_kfp
    frame_kfp = 0
    frame_bl = 0
    kfp_change_bl = 0
    bl_change_kfp = 0
    offset_bl = 0
    offset_kfp = 0
    # TIMER
    # toca pelo timeline keyframepro
    def frame_kfp_get():
        global frame_kfp,frame_bl, kfp_change_bl, bl_change_kfp
        kpro_client = KeyframeProClient()
        if kpro_client.connect() and kpro_client.initialize():
            frame_kfp_actual = kpro_client.get_frame()
            frame_bl_actual = bpy.context.scene.frame_current

            # frame_bl = frame_bl #+ offset_kfp
            # frame_bl_actual = frame_bl_actual #+ offset_kfp

            # frame_kfp = frame_kfp #- offset_kfp
            # frame_kfp_actual = frame_kfp_actual #- offset_kfp

       
        if abs(frame_kfp - frame_kfp_actual) > abs(frame_bl - frame_bl_actual):
            kfp_change_bl =1
        if abs(frame_kfp - frame_kfp_actual) < abs(frame_bl - frame_bl_actual):
            bl_change_kfp =1


        # Se entra no IF se frame KFP tiver mudado (estaria tocando)
        if kpro_client.connect() and kpro_client.initialize():
            # if frame_kfp != frame_kfp_actual:

            if kfp_change_bl ==1:
                if frame_kfp != 0: #ignore fake change
                    bpy.context.scene.frame_set(frame_kfp_actual - offset_kfp)  #se houve alteracao do kfp, mudar no blender
                    frame_kfp = frame_kfp_actual
                    frame_bl = frame_kfp_actual - offset_kfp
                else:
                    frame_kfp = frame_kfp_actual

            # if frame_bl != frame_bl_actual:
            if bl_change_kfp ==1:
                kpro_client.set_frame(frame_bl_actual + offset_kfp, audio=False, from_range_start=False)
                frame_kfp = frame_bl_actual + offset_kfp
                frame_bl = frame_bl_actual 
        
        kfp_change_bl = 0
        bl_change_kfp = 0

        return 0.1
    # bpy.app.timers.register(frame_kfp_get,persistent=True)
    # bpy.app.timers.register(frame_kfp_get)


    # # Handler Pre
    # # teopricamente deveria certificar que apenas a opção correta seja executada
    # @persistent
    # def my_handler_pre(scene):
    #     global kfp_change_bl,bl_change_kfp
    #     # if kfp_change_bl == 1:
    #     if bpy.context.screen.is_animation_playing:
    #         bl_change_kfp = 0
    #         print('1.1-kfp_change_bl == 1','kfp_change_bl',kfp_change_bl, 'bl_change_kfp',bl_change_kfp)
    #     else:
    #         kfp_change_bl = 0
    #         print('1.2-kfp_change_bl != 1','kfp_change_bl',kfp_change_bl, 'bl_change_kfp',bl_change_kfp)
    #     # if not bpy.context.screen.is_animation_playing:
    #     #     bl_change_kfp = 0
    #     #     print('pre_anim_not','kfp_change_bl',kfp_change_bl, 'bl_change_kfp',bl_change_kfp)
    #     # else: 
    #     #     kfp_change_bl = 0
    #     #     print('pre_anim','kfp_change_bl',kfp_change_bl, 'bl_change_kfp',bl_change_kfp)
    # bpy.app.handlers.frame_change_pre.append(my_handler_pre)


    # # HANDLER POST
    # # toca pelo timeline blender
    # @persistent
    # def frame_bldr_get(scene): 
    #     print('2.0-frame_bldr_get')
    #     global kfp_change_bl,bl_change_kfp
    #     if kfp_change_bl != 1:
    #         kpro_client = KeyframeProClient()
    #         # if kpro_client.connect() and kpro_client.initialize() and bpy.context.screen.is_animation_playing:
    #         if kpro_client.connect() and kpro_client.initialize():
    #             bl_change_kfp = 1
    #             # print('kfp_change_bl',kfp_change_bl, 'bl_change_kfp',bl_change_kfp,'|play anim :', bpy.context.screen.is_animation_playing ,'|f_kf :',kpro_client.get_frame())
    #             print('2.1-kfp_change_bl',kfp_change_bl, 'bl_change_kfp',bl_change_kfp,'|f_kf :',kpro_client.get_frame())
    #             kpro_client.set_frame(scene.frame_current, audio=False, from_range_start=False) 
    # bpy.app.handlers.frame_change_post.append(frame_bldr_get)

# class Set_offset_bl(bpy.types.Operator):
#     bl_idname = "view3d.set_offset_bl"
#     bl_label = "offset blender"
#     bl_description = "set offset on blender"

#     def execute(self, context):
#         global offset_bl
#         offset_bl = bpy.context.scene.frame_current
#         return{'FINISHED'}

class Set_offset_kfp(bpy.types.Operator):
    bl_idname = "view3d.set_offset_kfp"
    bl_label = "offset keyframepro"
    bl_description = "set offset on KeyFrame Pro"

    def execute(self, context):
        global offset_kfp
        kpro_client = KeyframeProClient()
        if kpro_client.connect() and kpro_client.initialize():
            offset_kfp = kpro_client.get_frame()
        #move the timeline position to begin
        bpy.context.scene.frame_set(0) #joga logo a timeline direto pra inicio
        return{'FINISHED'}

    def send_offset():
        global offset_kfp
        return str(offset_kfp)

class Clear_offset(bpy.types.Operator):
    bl_idname = "view3d.clear_offset"
    bl_label = "clear offset"
    bl_description = "clear offset"

    def execute(self, context):
        global offset_kfp,offset_bl
        offset_kfp = 0
        offset_bl = 0
        kpro_client = KeyframeProClient()
        if kpro_client.connect() and kpro_client.initialize():
            bpy.context.scene.frame_set(kpro_client.get_frame())
        return{'FINISHED'}

class Prev_bookmark(bpy.types.Operator):
    bl_idname = "view3d.prev_bookmark"
    bl_label = "Previous Bookmark"
    bl_description = "Previous Bookmark"

    def execute(self, context):
        kpro_client = KeyframeProClient()
        if kpro_client.connect() and kpro_client.initialize():
            all_bkmark = kpro_client.get_bookmarks(include_empty_timelines=True)
            # print('bookmarks :',all_bkmark[0]['bookmarks'])

            for a in range(0,len(all_bkmark)):
                # print(all_bkmark[a]['name'])
                if all_bkmark[a]['name']=='My Timeline':
                    # bkmark = all_bkmark[a]['bookmarks']
                    bkmark_book = all_bkmark[a]['bookmarks']
                    bkmark_annot = all_bkmark[a]['annotations']
                    bkmark = bkmark_book + bkmark_annot
                    bkmark.sort()

                    # print(bkmark)
            
            frame_ref = kpro_client.get_frame()
            frame_temp = 0
            row_temp = -1 #iniciando com valor menor para ser sempre o valor anterior
            for b in range(0,len(bkmark)):

                # print('bmark valor :',bkmark[b], 'frameref :',frame_ref)
                if frame_temp == 0:
                    if frame_ref < bkmark[0]:
                        frame_temp = bkmark[len(bkmark)-1]
                    elif frame_ref == bkmark[b] and len(bkmark)>1 :
                        if b==0:
                            frame_temp = bkmark[len(bkmark)-1]
                        else:
                            frame_temp = bkmark[row_temp]
                    elif frame_ref > bkmark[b] and len(bkmark)==(b+1) :
                        frame_temp = bkmark[b]
                    elif frame_ref > bkmark[b] and frame_ref < bkmark[b+1] :
                        frame_temp = bkmark[b]
                row_temp = row_temp + 1    
            frame_final = frame_temp
            bpy.context.scene.frame_set(frame_final - offset_kfp) #define valor do bookmark no blender
            kpro_client.set_frame(frame_final, audio=False, from_range_start=False) #valor no kfp
        return{'FINISHED'}

class Next_bookmark(bpy.types.Operator):
    bl_idname = "view3d.next_bookmark"
    bl_label = "Next Bookmark"
    bl_description = "Next Bookmark"

    def execute(self, context):
        kpro_client = KeyframeProClient()
        if kpro_client.connect() and kpro_client.initialize():
            all_bkmark = kpro_client.get_bookmarks(include_empty_timelines=True)
            # print('bookmarks :',all_bkmark[0]['bookmarks'])

            for a in range(0,len(all_bkmark)):
                # print(all_bkmark[a]['name'])
                if all_bkmark[a]['name']=='My Timeline':
                    # bkmark = all_bkmark[a]['bookmarks']
                    bkmark_book = all_bkmark[a]['bookmarks']
                    bkmark_annot = all_bkmark[a]['annotations']
                    bkmark = bkmark_book + bkmark_annot
                    bkmark.sort()

                    # print(bkmark)
            
            frame_ref = kpro_client.get_frame()
            frame_temp = 0
            # row_temp = -1 #iniciando com valor menor para ser sempre o valor anterior
            for b in range(0,len(bkmark)):

                # print('bmark valor :',bkmark[b], 'frameref :',frame_ref)
                if frame_temp == 0:
                    if frame_ref < bkmark[0]:
                        frame_temp = bkmark[0]
                    elif frame_ref == bkmark[b] and len(bkmark)>1 :
                        if b==len(bkmark)-1: # se b == ultimo bookmark
                            frame_temp = bkmark[0]
                        else:
                            frame_temp = bkmark[b+1]
                    elif frame_ref > bkmark[b] and len(bkmark)==(b+1) :
                        frame_temp = bkmark[0]
                    elif frame_ref > bkmark[b] and frame_ref < bkmark[b+1] :
                        frame_temp = bkmark[b+1]
                # row_temp = row_temp + 1    
            frame_final = frame_temp
            bpy.context.scene.frame_set(frame_final - offset_kfp) #define valor do bookmark no blender
            kpro_client.set_frame(frame_final, audio=False, from_range_start=False) #valor no kfp
        return{'FINISHED'}

from subprocess import Popen
class Open_keyframe(bpy.types.Operator):
    bl_idname = "view3d.open_software"
    bl_label = "Open KF"
    bl_description = "Open KeyFrame Software"

    def execute(self, context):
        Popen("C:/Program Files/Keyframe Pro/bin/KeyframePro.exe")
        return{'FINISHED'}


class Render_Viewport_PortA (bpy.types.Operator):
    bl_idname = "view3d.viewport_animation_port_a"
    bl_label = "Viewport Animation Port A"
    bl_description = "Render Viewport Animation on Port A"

    def execute(self, context):
        kpro_client = KeyframeProClient()
        if kpro_client.connect() and kpro_client.initialize():
            # bpy.ops.render.opengl(animation=True,  sequencer=False,  view_context=True)
            # filepath = bpy.context.scene.render.frame_path(frame=1) #pega endereco completo do render a partir do frame 1
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
                    # address=address + '\\'+'A'+'\\'
                    address=address + '\\'+'A'
            # filepath = address

            original_folder = bpy.context.scene.render.filepath
            bpy.context.scene.render.filepath = address

            
            render_original = bpy.context.scene.render.resolution_percentage


            scene = context.scene
            # mytool = scene.my_tool
            percentage = scene.percentage
            percent_render_var = percentage.percentage

            bpy.context.scene.render.resolution_percentage = percent_render_var
            # print('render panel A percentage :',percent_render_var)

            bpy.ops.render.opengl(animation=True,  view_context=True)
            
            full = bpy.context.scene.render.frame_path(frame=1)
            filepath = full
            viewport_anim = kpro_client.import_file(filepath)

            # kpro_client.set_viewer_layout(layout="vertical")

            kpro_client.set_active_in_viewer(viewport_anim['id'], 0) #viewport A
            # kpro_client.set_active_in_viewer(viewport_anim['id'], 1) #viewport B
            
            bpy.context.scene.render.filepath = original_folder
            bpy.context.scene.render.resolution_percentage = render_original
            kpro_client.set_active_in_viewer(viewport_anim['id'], 0) #viewport A
        return{'FINISHED'}

class Render_Viewport_PortB (bpy.types.Operator):
    bl_idname = "view3d.viewport_animation_port_b"
    bl_label = "Viewport Animation Port B"
    bl_description = "Render Viewport Animation on Port B"
    global percent_render_var
    def execute(self, context):
        global percent_render_var
        kpro_client = KeyframeProClient()
        if kpro_client.connect() and kpro_client.initialize():
            # bpy.ops.render.opengl(animation=True,  sequencer=False,  view_context=True)
            # filepath = bpy.context.scene.render.frame_path(frame=1) #pega endereco completo do render a partir do frame 1
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
                    # address=address + '\\'+'B'+'\\'
                    address=address + '\\'+'B'
            # filepath = address

            
            view_a_pre = kpro_client.get_active_in_viewer(0)


            original_folder = bpy.context.scene.render.filepath
            bpy.context.scene.render.filepath = address

            
            render_original = bpy.context.scene.render.resolution_percentage


            scene = context.scene
            # mytool = scene.my_tool
            percentage = scene.percentage
            percent_render_var = percentage.percentage

            bpy.context.scene.render.resolution_percentage = percent_render_var
            # print('render panel B percentage :',percent_render_var)

            bpy.ops.render.opengl(animation=True,  view_context=True)
            
            full = bpy.context.scene.render.frame_path(frame=1)
            filepath = full
            viewport_anim = kpro_client.import_file(filepath)

            
            # print('view_a antes :',view_a)
            kpro_client.set_viewer_layout(layout="vertical")

            if view_a_pre == {}:
                kpro_client.set_active_in_viewer(viewport_anim['id'], 1) #viewport B envia animacao
            else: #trecho para preencher View A pois estava apagando ao inserir View_b
                kpro_client.set_active_in_viewer(viewport_anim['id'], 1) #viewport B envia animacao

                view_a = kpro_client.get_active_in_viewer(0)
                print('view_a depois :',view_a)

                kpro_client.set_active_in_viewer(view_a_pre['id'], 0) # trecho para preencher viewer A, pois este apaga quando coloca o viewere B
                print('view_id compara:',view_a_pre['id']==viewport_anim['id'] )
            
            # kpro_client.set_active_in_viewer(viewport_anim['id'], 1) #viewport B
            
            bpy.context.scene.render.filepath = original_folder
            bpy.context.scene.render.resolution_percentage = render_original
        return{'FINISHED'}


# def check_sync(): #faz checagem para veryficar se sync ta ativo
#         checked_sync = bpy.app.timers.is_registered(frame_kfp_to_bl.frame_kfp_get)
#         return str(checked_sync)