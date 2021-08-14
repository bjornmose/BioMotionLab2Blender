# This script defines functions to be used directly in drivers expressions to
# extend the builtin set of python functions.
#
# This can be executed on manually or set to 'Register' to
# initialize thefunctions on file load.

import bpy
import math
from math import sin, cos, radians
import mathutils
import bmesh
import numpy as np

#donot rename with BML data
#nControlRoot = "[Osz]"
#nCSin        = "[1]Sin(1t)"
#nCCos        = "[1]Cos(1t)" 
#nCSin2       = "[2]Sin(2t)"
#nCCos2       = "[2]Cos(2t)" 

nControlRoot = "ControlRoot"
nCSin        = "CSin"
nCCos        = "CCos" 
nCSin2       = "CSin2"
nCCos2       = "CCos2" 


nLissajousScale = "LisScale"
nLissajousSin1x = "LisSin1x"
nLissajousSin1y = "LisSin1y"
nLissajousSin1z = "LisSin1z"

nLissajousCos1x = "LisCos1x"
nLissajousCos1y = "LisCos1y"
nLissajousCos1z = "LisCos1z"

nLissajousSin2x = "LisSin2x"
nLissajousSin2y = "LisSin2y"
nLissajousSin2z = "LisSin2z"

nLissajousCos2x = "LisCos2x"
nLissajousCos2y = "LisCos2y"
nLissajousCos2z = "LisCos2z"



nFrames      = "Osz_Frames"
nShift       = "Osz_Shift"
nAmplitude   = "Osz_Amplitude"
nStickyOrg   = "Osz_StickyOrg"
nCopyFrom    = "Osz_CopyFrom"
nCopyTo      = "Osz_CopyTo"

nDefaultPeriod =2*2*3*5*7

nControlDefaultDefaultShape = "SPHERE"


def oszUniqueName(namein):
        name = namein
        pp=name.partition(nControlRoot)
        if (len(pp[1])>0):
            name = pp[0] + 'I'+nControlRoot
        return(name)   

    

def oscAxisID(t,axis,ID):
    obj = bpy.data.objects.get(ID+nControlRoot)
    if (not obj):
        return 0
#        GenControl(ID)
    try:
     frames =  obj[nFrames]
    except: 
     frames = nDefaultPeriod
    try:
     shift  =  obj[nShift] 
    except: 
     shift = 0.0
    try:
     amp = obj[nAmplitude] 
    except: 
     amp = 1.0
    try:
     fo = obj[nStickyOrg] 
    except: 
     fo = 1.0

    timebase = frames/(2*math.pi)
    f=(t+shift)/timebase 
        
    obj = bpy.data.objects.get(ID+nControlRoot)
    o = obj.location[axis]
    obj = bpy.data.objects.get(ID+nCSin)
    a = obj.location[axis]
    obj = bpy.data.objects.get(ID+nCCos)
    b = obj.location[axis]
    obj = bpy.data.objects.get(ID+nCSin2)
    c = obj.location[axis]
    obj = bpy.data.objects.get(ID+nCCos2)
    d = obj.location[axis]
    v = fo*o + amp * (a  * sin(f) + b * cos(f) + c * sin(2*f) + d * cos(2*f))
    return v

def oscAxisIDe(t,axis,ID):
    obj = bpy.data.objects.get(ID+nControlRoot)
    if (not obj):
        return 0
#        GenControl(ID)
    try:
     frames =  obj[nFrames]
    except: 
     frames = nDefaultPeriod 
    try:
     shift  =  obj[nShift] 
    except: 
     shift = 0.0
    try:
     amp = obj[nAmplitude] 
    except: 
     amp = 1.0

    timebase = frames/(2*math.pi)
    f=(t+shift)/timebase 
        
    #obj = bpy.data.objects.get(ID+nControlRoot)
    #o = obj.location[axis]
    obj = bpy.data.objects.get(ID+nCSin)
    a = obj.location[axis]
    obj = bpy.data.objects.get(ID+nCCos)
    b = obj.location[axis]
    obj = bpy.data.objects.get(ID+nCSin2)
    c = obj.location[axis]
    obj = bpy.data.objects.get(ID+nCCos2)
    d = obj.location[axis]
    v = amp * (a  * sin(f) + b * cos(f) + c * sin(2*f) + d * cos(2*f))
    return v





 
def OszCopyFromNamedRoot(ID,name):
    obj1 = bpy.data.objects.get(ID+name)
    obj2 = bpy.data.objects.get(name)
    obj1.location = obj2.location

    
def OszCopyFromRoot(context,ID):
    OszCopyFromNamedRoot(ID,nControlRoot)
    OszCopyFromNamedRoot(ID,nCSin)
    OszCopyFromNamedRoot(ID,nCCos)
    OszCopyFromNamedRoot(ID,nCSin2)
    OszCopyFromNamedRoot(ID,nCCos2)

def OszCopyLocation(ID_me,ID_other,name):
    obj1 = bpy.data.objects.get(ID_me+name)
    obj2 = bpy.data.objects.get(ID_other+name)
    obj1.location = obj2.location
  
def OszCopyProps(ID_me,ID_other,name):
    obj1 = bpy.data.objects.get(ID_me+name)
    obj2 = bpy.data.objects.get(ID_other+name)
    obj1[nFrames]  = obj2[nFrames] 
    obj1[nShift]   = obj2[nShift] 
    obj1[nAmplitude]   = obj2[nAmplitude] 


def OszCopyFromOther(ID_me,ID_other):
    OszCopyLocation(ID_me,ID_other,nControlRoot)
    OszCopyProps(ID_me,ID_other,nControlRoot)
    OszCopyLocation(ID_me,ID_other,nCSin)
    OszCopyLocation(ID_me,ID_other,nCCos)
    OszCopyLocation(ID_me,ID_other,nCSin2)
    OszCopyLocation(ID_me,ID_other,nCCos2)
    
def createEmpty(OName,draw_size,draw_type):
    print('Create {:}'.format(OName))
    Cobj = bpy.data.objects.new( OName, None )
    ver = bpy.app.version[1]
    print(ver)
    if (ver < 80):
        bpy.context.scene.objects.link( Cobj )
        Cobj.empty_draw_size = draw_size
        Cobj.empty_draw_type = draw_type
    
    if (ver > 79):
        bpy.context.scene.collection.objects.link( Cobj )
        Cobj.empty_display_size = draw_size
        Cobj.empty_display_type = draw_type  

    return Cobj   

class OszControl():

    def objIsOsz(obj):
        to_name = obj.name + nControlRoot
        print('is OscC')
        print(to_name)
        Cobj = bpy.data.objects.get(to_name)
        if (Cobj is not None ):
            return True
        else:
            return False
    
    
def GenControl(ID):
     w_empty_draw_size = 1
     OName =ID+nControlRoot
     Cobj = bpy.data.objects.get(OName)
     if (not Cobj):
         Cobj = createEmpty(OName,w_empty_draw_size,nControlDefaultDefaultShape )
         Cobj[nFrames] = nDefaultPeriod 
         Cobj[nShift] = 0.0
         Cobj[nAmplitude] = 1.0
         Cobj[nCopyFrom] = 'void'
         Cobj[nCopyTo] = 'void'
         
         Cobj[nLissajousScale] = 0.5
         
         Cobj[nLissajousSin1x] = 1         
         Cobj[nLissajousSin1y] = 0         
         Cobj[nLissajousSin1z] = 0         
         
         Cobj[nLissajousCos1x] = 0         
         Cobj[nLissajousCos1y] = 1         
         Cobj[nLissajousCos1z] = 0         
         
         Cobj[nLissajousSin2x] = 1         
         Cobj[nLissajousSin2y] = 0         
         Cobj[nLissajousSin2z] = 0         
         
         Cobj[nLissajousCos2x] = 0         
         Cobj[nLissajousCos2y] = 1         
         Cobj[nLissajousCos2z] = 0         
  
 
           
     OName =ID+nCSin
     obj = bpy.data.objects.get(OName)
     if (not obj):
         obj = createEmpty(OName,w_empty_draw_size,'ARROWS')
         obj.parent = Cobj

     OName =ID+nCCos
     obj = bpy.data.objects.get(OName)
     if (not obj):
         obj = createEmpty(OName,w_empty_draw_size,'ARROWS')
         obj.parent = Cobj

     OName =ID+nCSin2
     obj = bpy.data.objects.get(OName)
     if (not obj):
         obj = createEmpty(OName,w_empty_draw_size,'ARROWS')
         obj.parent = Cobj

     OName =ID+nCCos2
     obj = bpy.data.objects.get(OName)
     if (not obj):
         obj = createEmpty(OName,w_empty_draw_size,'ARROWS')
         obj.parent = Cobj
     print(ID+"GenControl Done")
     return(Cobj)
     
def add_driverOsc(source, index ,ID):
    d = source.driver_add( 'location', index ).driver
    d.expression = "oscAxisID(frame,"+str(index)+",'"+ID+"')" 
    

def AddOszDriver(obj,ID):
    add_driverOsc(obj, 0, ID)    
    add_driverOsc(obj, 1, ID)
    add_driverOsc(obj, 2, ID)



def add_driverOsce(source, index ,ID):
    d = source.driver_add( 'location', index ).driver
    d.expression = "oscAxisIDe(frame,"+str(index)+",'"+ID+"')" 
    

def AddOszDrivere(obj,ID):
    add_driverOsce(obj, 0, ID)    
    add_driverOsce(obj, 1, ID)
    add_driverOsce(obj, 2, ID)

    
     
class CopyOszRootOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.copyoszroot_operator"
    bl_label = "CopyFromControlRoot"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        obj = context.object
        pp=obj.name.partition(nControlRoot)
        if (len(pp[1]) > 0):
         OszCopyFromRoot(context,pp[0])
         print("Transfer-->"+pp[0]+pp[1])
        return {'FINISHED'}
     

class AddOszDriverOperator(bpy.types.Operator):
    #bl_idname no upper Case allowed!
    bl_idname = "object.addoszdriveroperator"
    bl_label = "AddOszDriver"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        obj = context.object
        name = obj.name
        """
        pp=obj.name.partition(nControlRoot)
        if (len(pp[1])>0):
            name = pp[0] + 'I'+nControlRoot
        """
        GenControl(name)
        AddOszDriver(obj,name)
        return {'FINISHED'}

class EmbedInOszOperator(bpy.types.Operator):
    #bl_idname no upper Case allowed!
    bl_idname = "object.embedinoszoperator"
    bl_label = "MakeOszParent"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        obj = context.object
        name = obj.name
        """
        pp=obj.name.partition(nControlRoot)
        if (len(pp[1])>0):
            name = pp[0] + 'I'+nControlRoot
        """
        pobj = GenControl(name)
        pobj.location = obj.location
        obj.parent = pobj
        AddOszDrivere(obj,name)
        return {'FINISHED'}




class duposzoperator(bpy.types.Operator):
    #bl_idname no upper Case allowed!
    bl_idname = "object.duposzoperator"
    bl_label  = "DupOszDriver"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        obj = context.object
        name = obj.name
        pp=obj.name.partition(nControlRoot)
        if (len(pp[1])>0):
            for i in range(1,10):
             nname = pp[0] +'_' +str(i)
             testobj = bpy.data.objects.get(nname+nControlRoot)
             if (testobj is None):
              GenControl(nname)
              OszCopyFromOther(nname,pp[0])
              obj[nCopyFrom]=nname  
              obj[nCopyTo]=nname  
              break
             else:
              print(testobj.name + ' exists')
            
        return {'FINISHED'}

class copyoszoperator(bpy.types.Operator):
    #bl_idname no upper Case allowed!
    bl_idname = "object.copyoszoperator"
    bl_label  = "Pull"

    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            obj = context.object
            pp=obj.name.partition(nControlRoot)
            if (len(pp[1])>0):
                othername = obj[nCopyFrom]
                testobj = bpy.data.objects.get(othername+nControlRoot)
                if (testobj is not None):
                    return(1) 
        return(0)
            


    def execute(self, context):
        obj = context.object
        name = obj.name
        pp=obj.name.partition(nControlRoot)
        if (len(pp[1])>0): # am osz at all
          othername = obj[nCopyFrom]     
          testobj = bpy.data.objects.get(othername+nControlRoot)
          if (testobj is not None):
               OszCopyFromOther(pp[0],othername)
               print('copy ' + pp[0] + ' <--' +  othername)    
          else:
               print('OOPS?' + othername)     
                
        return {'FINISHED'}
    
    
class copyoszoperatorto(bpy.types.Operator):
    #bl_idname no upper Case allowed!
    bl_idname = "object.copytooszoperator"
    bl_label  = "Push"

    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            obj = context.object
            pp=obj.name.partition(nControlRoot)
            if (len(pp[1])>0):
                othername = obj[nCopyTo]
                testobj = bpy.data.objects.get(othername+nControlRoot)
                if (testobj is not None):
                    return(1) 
        return(0)



    def execute(self, context):
        obj = context.object
        name = obj.name
        pp=obj.name.partition(nControlRoot)
        if (len(pp[1])>0): # am osz at all
          othername = obj[nCopyTo]     
          testobj = bpy.data.objects.get(othername+nControlRoot)
          if (testobj is not None):
               OszCopyFromOther(othername,pp[0])
               print('copy ' + pp[0] + ' --> ' +  othername)    
          else:
               print('OOPS?' + othername)     
                
        return {'FINISHED'}




class SetAmpAll(bpy.types.Operator):
    #bl_idname no upper Case allowed!
    bl_idname = "object.setampall"
    bl_label  = "SetAmpAll"
    
    @classmethod
    def poll(self, context):
        has_amp = 0
        ao = context.active_object
        try:
            amp= ao[nAmplitude]
            has_amp=1
        except:  
            has_amp=0            
        return (has_amp!=0)


    def execute(self, context):
        ao = context.active_object
        amp = 1.0
        amp= ao[nAmplitude] 
        print(amp)        
        for ob in context.selected_objects:
            name = ob.name
            pp=ob.name.partition(nControlRoot)
            if (len(pp[1])>0):
                print(name)
                ob[nAmplitude]=amp
        return {'FINISHED'}

class SetFramesAll(bpy.types.Operator):
    #bl_idname no upper Case allowed!
    bl_idname = "object.setframesall"
    bl_label  = "SetFramesAll"

    @classmethod
    def poll(self, context):
        has_f = 0
        ao = context.active_object
        try:
            amp= ao[nFrames]
            has_f=1
        except:  
            has_f=0            
        return (has_f!=0)
    
    def execute(self, context):
        ao = context.active_object
        fr = 40
        fr= ao[nFrames] 
        print(fr)        
        for ob in context.selected_objects:
            name = ob.name
            pp=ob.name.partition(nControlRoot)
            if (len(pp[1])>0):
                print(name)
                ob[nFrames]=fr
        return {'FINISHED'}

class SetShiftAll(bpy.types.Operator):
    #bl_idname no upper Case allowed!
    bl_idname = "object.setshiftall"
    bl_label  = "SetShiftAll"

    @classmethod
    def poll(self, context):
        has_f = 0
        ao = context.active_object
        try:
            shift= ao[nShift]
            has_s=1
        except:  
            has_s=0            
        return (has_s!=0)
    
    def execute(self, context):
        ao = context.active_object
        sh = 0
        sh= ao[nShift] 
        print(sh)        
        for ob in context.selected_objects:
            name = ob.name
            pp=ob.name.partition(nControlRoot)
            if (len(pp[1])>0):
                print(name)
                ob[nShift]=sh
        return {'FINISHED'}
    
class SetLissajous(bpy.types.Operator):
    #bl_idname no upper Case allowed!
    bl_idname = "object.setlissajous"
    bl_label  = "SetLissajous"

    @classmethod
    def poll(self, context):
        has_l = 0
        ao = context.active_object
        try:
            dummy = ao[nLissajousCos1x]
            has_l=1
        except:  
            has_l=0            
        return (has_l!=0)
    
    def execute(self, context):
        scale = 1.0
        ao = context.active_object
        try:
            scale = ao[nLissajousScale] 

        except: 
            ao[nLissajousScale] = 1.0

        frames=bpy.context.scene.frame_end
        
        for ob in context.selected_objects:
            name = ob.name
            pp=ob.name.partition(nControlRoot)
            if (len(pp[1])>0):
                print('to do->SetLissajous')
                truncname =(pp[0])
                print(truncname)
                targetobj = bpy.data.objects.get(truncname+nCSin)
                if (targetobj is not None):
                    targetobj.location[0] = scale * ao[nLissajousSin1x]
                    targetobj.location[1] = scale * ao[nLissajousSin1y]
                    targetobj.location[2] = scale * ao[nLissajousSin1z]
                targetobj = bpy.data.objects.get(truncname+nCCos)
                if (targetobj is not None):
                    targetobj.location[0] = scale * ao[nLissajousCos1x]
                    targetobj.location[1] = scale * ao[nLissajousCos1y]
                    targetobj.location[2] = scale * ao[nLissajousCos1z]

                targetobj = bpy.data.objects.get(truncname+nCSin2)
                if (targetobj is not None):
                    targetobj.location[0] = scale * ao[nLissajousSin2x]
                    targetobj.location[1] = scale * ao[nLissajousSin2y]
                    targetobj.location[2] = scale * ao[nLissajousSin2z]
                    
                targetobj = bpy.data.objects.get(truncname+nCCos2)
                if (targetobj is not None):
                    targetobj.location[0] = scale * ao[nLissajousCos2x]
                    targetobj.location[1] = scale * ao[nLissajousCos2y]
                    targetobj.location[2] = scale * ao[nLissajousCos2z]
                bpy.ops.object.paths_calculate(start_frame=1,end_frame=frames)
                    
                #Doit here
        return {'FINISHED'}
    



class OpUpdateOszDriverProps(bpy.types.Operator):
    #bl_idname no upper Case allowed!
    bl_idname = "object.updateoszdriverprops"
    bl_label = "ExpandOszDriverProps"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        obj = context.object
        name = obj.name
        pp=obj.name.partition(nControlRoot)
        if (len(pp[1])>0):
            try:
             frames =  obj[nFrames]
            except: 
             obj[nFrames] = 40
            try:
             shift  =  obj[nShift ] 
            except: 
             obj[nShift ] = 0.0         
            try:
             amp = obj[nAmplitude] 
            except: 
             obj[nAmplitude] = 1.0
             
            try:
             fo = obj[nStickyOrg] 
            except: 
             obj[nStickyOrg] = 1.0

            try:
             on = obj[nCopyFrom] 
            except: 
             obj[nCopyFrom] = ""
            try:
             on = obj[nCopyTo] 
            except: 
             obj[nCopyTo] = ""

            print(name + "Update done")
        else:
            print("nothing to update")
        return {'FINISHED'}



class LissajousPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "LissajousPanel"
    bl_idname = "OBJECT_PT_LISSAJOUSGP"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
         obj = context.object
         layout = self.layout
         pp=obj.name.partition(nControlRoot)
         if (len(pp[1])>0):

            row = layout.row()
            row.prop(obj, '["%s"]' % (nLissajousSin1x),text="XSin(t)") 
            row.prop(obj, '["%s"]' % (nLissajousSin1y),text="YSin(t)") 
            row.prop(obj, '["%s"]' % (nLissajousSin1z),text="ZSin(t)") 

            row.prop(obj, '["%s"]' % (nLissajousCos2x),text="XCos(2t)") 
            row.prop(obj, '["%s"]' % (nLissajousCos2y),text="YCos(2t)") 
            row.prop(obj, '["%s"]' % (nLissajousCos2z),text="ZCos(2t)") 
            
            row = layout.row()

            
            row.prop(obj, '["%s"]' % (nLissajousCos1x),text="XCos(1)") 
            row.prop(obj, '["%s"]' % (nLissajousCos1y),text="YCos(1)") 
            row.prop(obj, '["%s"]' % (nLissajousCos1z),text="ZCos(1)") 
            
            
            row.prop(obj, '["%s"]' % (nLissajousSin2x),text="XSin(2t)") 
            row.prop(obj, '["%s"]' % (nLissajousSin2y),text="YSin(2t)") 
            row.prop(obj, '["%s"]' % (nLissajousSin2z),text="ZSin(2t)") 

            

            
            row = layout.row()
            row.prop(obj, '["%s"]' % (nLissajousScale),text="Scale") 
            row.operator("object.setlissajous")
         
class CycleGenPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "OscGenPanel"
    bl_idname = "OBJECT_PT_CGP"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
         obj = context.object
         layout = self.layout
         pp=obj.name.partition(nControlRoot)
         if (len(pp[1])>0):
            row = layout.row()
            row.prop(obj, '["%s"]' % (nCopyFrom),text="Source") 
            row.operator("object.copyoszoperator")
            row = layout.row()
            row.prop(obj, '["%s"]' % (nCopyTo),text="Target") 
            row.operator("object.copytooszoperator")
            row = layout.row()
            row.operator("object.duposzoperator")

            row = layout.row()
            row.prop(obj, '["%s"]' % (nAmplitude),text="Amp") 
            row.prop(obj, '["%s"]' % (nFrames),text="Frames") 
            row.prop(obj, '["%s"]' % (nShift),text="Shift") 
            row = layout.row()
            row.operator("object.setampall")
            row.operator("object.setframesall")
            row.operator("object.setshiftall")
        
            row = layout.row()
            row.operator("object.updateoszdriverprops")
                
            if (bpy.data.objects.get(nControlRoot) is not None):
                row.operator("object.copyoszroot_operator")
         row = layout.row()
         c_test = OszControl
         b_result = c_test.objIsOsz(obj)
         if (not b_result):
             row.operator("object.embedinoszoperator")
             row.operator("object.addoszdriveroperator")
         else:
             row.label(text=(" Attached to " + obj.name + nControlRoot))
             row = layout.row()
             row.label(text=(" ToDo : Update Display Path"))
         
   

# Put Classes to publish here 
_myclasses = (
              CopyOszRootOperator,
              CycleGenPanel,
              LissajousPanel,
              SetLissajous,
              EmbedInOszOperator,
              AddOszDriverOperator,
              OpUpdateOszDriverProps,
              duposzoperator,
              copyoszoperator,
              copyoszoperatorto,
              SetAmpAll,
              SetFramesAll,
              SetShiftAll
              ) 
                

def register():
    bpy.app.driver_namespace["oscAxisID"] = oscAxisID
    bpy.app.driver_namespace["oscAxisIDe"] = oscAxisIDe
    for cls in _myclasses :
        bpy.utils.register_class(cls)


def unregister():
    for cls in _myclasses :
        bpy.utils.unregister_class(cls)
    print("Unregistered OszAxis .. ")

#run from run
if __name__ == "__main__":
#    GenControl('')
    register()
    print('register is done')
else:
    register()
    GenControl('')
    print('Osz Avis V xxx register done')
