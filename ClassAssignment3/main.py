import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

projection = True
button_left = False
button_right = False
cur_xpos = 0
cur_ypos = 0
azimuth = np.radians(45)
elevation = np.radians(35.264)
distance = 5
u = np.array([1,0,0])
v = np.array([0,1,0])
w = np.array([0,0,1])
p_ref = np.array([0.,0.,0.])

gVertexArrayIndexed = None
gIndexArray = None
global path,anim
isDrag = False
isBox = False
isAnimate = False
motion = []
fileName = ''

def createVertexArraySeparate():
    varr = np.array([
            (-0.5773502691896258,0.5773502691896258,0.5773502691896258),         # v0 normal
            ( -0.02 ,  0 ,  0.02 ), # v0 position
            (0.8164965809277261,0.4082482904638631,0.4082482904638631),         # v2 normal
            (  0.02 , 0 ,  0.02 ), # v2 position
            (0.4082482904638631,-0.4082482904638631,0.8164965809277261),         # v1 normal
            (  0.02 ,  -1 ,  0.02 ), # v1 position

            (-0.4082482904638631,-0.8164965809277261,0.4082482904638631),         # v0 normal
            ( -0.02 ,  -1 ,  0.02 ), # v0 position
            (-0.4082482904638631,0.4082482904638631,-0.8164965809277261),         # v3 normal
            ( -0.02 , 0 ,  -0.02 ), # v3 position
            (0.4082482904638631,0.8164965809277261,-0.4082482904638631),         # v2 normal
            (  0.02 , 0 ,  -0.02 ), # v2 position

            (0.5773502691896258,-0.5773502691896258,-0.5773502691896258),
            ( 0.02 ,  -1 , -0.02 ), # v4
            (-0.8164965809277261,-0.4082482904638631,-0.4082482904638631),
            (  -0.02 ,  -1 , -0.02 ), # v5
          
            ], 'float32')

            
    iarr = np.array([
            (0,2,1),
            (0,3,2),
            (4,5,6),
            (4,6,7),
            (0,1,5),
            (0,5,4),
            (3,6,2),
            (3,7,6),
            (1,2,6),
            (1,6,5),
            (0,7,3),
            (0,4,7)
            ], dtype = 'int32')
    return varr,iarr


def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    
    glVertexArrayIndexed,glIndexArray = createVertexArraySeparate()

    varr = glVertexArrayIndexed
    iarr = glIndexArray
    
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    
    glNormalPointer(GL_FLOAT,6*iarr.itemsize,varr)
    glVertexPointer(3,GL_FLOAT,6*iarr.itemsize,ctypes.c_void_p(varr.ctypes.data+3*iarr.itemsize))
    glDrawElements(GL_TRIANGLES,iarr.size,GL_UNSIGNED_INT,iarr)
    


def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glLoadIdentity()

    global projection
    if projection:
        gluPerspective(45, 1, 1, 50)
    else:
        glOrtho(-5,5, -5,5, -15,15)

    global azimuth, elevation, distance, u,v,w, p_ref
    w = np.array([np.cos(elevation) * np.sin(azimuth), np.sin(elevation),np.cos(elevation)*np.cos(azimuth)])
    w = w/np.sqrt(w@w)
    u = np.cross(v, w)
    u = u/np.sqrt(u@u)
    v = np.cross(w,u)

    if distance < 0:
        distance = 0
    p_eye = np.array([distance*w[0]+p_ref[0],distance*w[1]+p_ref[1],distance*w[2]+p_ref[2]])
    gluLookAt(p_eye[0],p_eye[1],p_eye[2], p_ref[0],p_ref[1],p_ref[2], v[0],v[1],v[2])

    drawGrid()

    glColor3ub(60, 0, 255)

    if(isDrag == True and isAnimate == False):
        anim.drawSkeleton()
    
    if(isAnimate == True):
        anim.animateMotion()

def drawGrid():
    glColor3ub(150,150,150)
    for i in range(-15, 16):
        for j in range(-15, 16):
            glBegin(GL_LINE_LOOP)
            glVertex3fv(np.array([i,0,j]))
            glVertex3fv(np.array([i+1,0,j]))
            glVertex3fv(np.array([i+1,0,j+1]))
            glVertex3fv(np.array([i,0,j+1]))
            glEnd()

def l2norm(v):
    return np.sqrt(np.dot(v, v))

def normalized(v):
    l = l2norm(v)
    if l == 0:
        l = 1
    return 1 / l * np.array(v)

class BvhJoint:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.offset = np.zeros(3)
        self.channelOrder = []
        self.channelIdx = []
        self.children = []
        self.rotationMatrix = list()
        self.position = list()
        self.channels = list()
        
    def addChild(self, child):
        self.children.append(child)

    def draw(self):
        global isBox, fileName
        
        glPushMatrix()
        glTranslatef(self.offset[0], self.offset[1], self.offset[2])

        if(isBox == True):
            if self.parent:
                offset = np.sqrt(self.offset[0]**2+self.offset[1]**2+self.offset[2]**2)
                                
                degree = np.cross(normalized(self.offset),np.array([0,1,0]))
                degreeSize = np.rad2deg(np.arcsin(np.sqrt(degree[0]**2+degree[1]**2+degree[2]**2)))
                if np.dot(self.offset, np.array([0,1,0])) > 0:
                    degreeSize = 180 - degreeSize
                glPushMatrix()
                glRotatef(degreeSize,degree[0],degree[1],degree[2])

                if fileName == '0007_Cartwheel001.bvh':
                    glScalef(30,-offset, 30)
                else:
                    glScalef(1,-offset, 1)
                drawCube_glDrawElements()
                glPopMatrix()
        else :
            if self.parent:
                glBegin(GL_LINES)
                glVertex3fv(-self.offset)
                glVertex3fv(np.array([0.,0.,0.]))
                glEnd()
        
        for child in self.children:
            child.draw()
        glPopMatrix()

    def animate(self, frameNumber):
        global motion, isBox
        
        glPushMatrix()
        glTranslatef(self.offset[0], self.offset[1], self.offset[2])
        
        if(isBox == True):
            if self.parent:
                offset = np.sqrt(self.offset[0]**2+self.offset[1]**2+self.offset[2]**2)
                
                degree = np.cross(normalized(self.offset),np.array([0,1,0]))
                degreeSize = np.rad2deg(np.arcsin(np.sqrt(degree[0]**2+degree[1]**2+degree[2]**2)))
                if np.dot(self.offset, np.array([0,1,0])) > 0:
                    degreeSize = 180 - degreeSize
                glPushMatrix()
                glRotatef(degreeSize,degree[0],degree[1],degree[2])
                
                if fileName == '0007_Cartwheel001.bvh':
                    glScalef(30,-offset, 30)
                else:
                    glScalef(1,-offset, 1)
                drawCube_glDrawElements()
                glPopMatrix()
        else :
            if self.parent:
                glBegin(GL_LINES)
                glVertex3fv(-self.offset)
                glVertex3fv(np.array([0.,0.,0.]))
                glEnd()
                
        for motion_idx, motion_type in zip(self.channelIdx, self.channelOrder):
            if motion_type.lower() == 'xrotation':
                glRotatef(motion[frameNumber][motion_idx], 1, 0, 0)
            elif motion_type.lower() == 'yrotation':
                glRotatef(motion[frameNumber][motion_idx], 0, 1, 0)
            elif motion_type.lower() == 'zrotation':
                glRotatef(motion[frameNumber][motion_idx], 0, 0, 1)
            elif motion_type.lower() == 'xposition':
                glTranslatef(motion[frameNumber][motion_idx], 0, 0)
            elif motion_type.lower() == 'yposition':
                glTranslatef(0, motion[frameNumber][motion_idx], 0)
            elif motion_type.lower() == 'zposition':
                glTranslatef(0, 0, motion[frameNumber][motion_idx])
            
        for child in self.children:
            child.animate(frameNumber)
        glPopMatrix()

class Bvh:
    def __init__(self):
        self.joints = {}
        self.root = None
        self.frames = 0
        self.fps = 0
      
    def parseFile(self, path):
        with open(path, 'r') as f:
            self.divideHierarchyAndMotion(f.read())
            
    def parseHierarchy(self, text):
        lines = text.split("\n")
        jointStack = []
        cidx = 0
        for line in lines:
            line =line.strip()
            words = line.split(" ")
            instruction = words[0]

            if instruction.upper() == "JOINT" or instruction.upper() == "ROOT":
                parent = jointStack[-1] if instruction.upper() == "JOINT" else None
                joint = BvhJoint(words[1], parent)
            
                self.joints[joint.name] = joint
               
                if parent:
                    parent.addChild(joint)
                jointStack.append(joint)
                
                if instruction.upper() == "ROOT":
                    self.root = joint
                    
            elif instruction.upper() == "CHANNELS":
                for i in range(2, len(words)):
                    jointStack[-1].channelIdx.append(cidx)
                    cidx+=1
                    jointStack[-1].channelOrder.append(words[i])
               
            elif instruction.upper() == "OFFSET":
                for i in range(1, len(words)):
                    jointStack[-1].offset[i - 1] = float(words[i])
                    
            elif instruction == "End":
                joint = BvhJoint(jointStack[-1].name + "_end", jointStack[-1])
                jointStack[-1].addChild(joint)
                jointStack.append(joint)
                       
            elif instruction == '}':
                jointStack.pop()


    def parseMotion(self, text):
        global  motion
        motion.clear()
    
        lines = text.split("\n")

        for line in lines:
            if line == '':
                continue

            line = line.replace("\n", "")
            line = line.strip()
            line = line.replace("\t"," ")
           
            if line.startswith("Frame Time: "):
                self.fps = round(1 / float(line.split(" ")[2]))
                continue
            if line.startswith("Frames:"):
                self.frames = int(line.split(" ")[1])
                continue
            
            line = line.split()
            line = list(map(float, line))
            motion.append(line)
           
    def divideHierarchyAndMotion(self, text):
        hierarchy, motion = text.split("MOTION")
        self.parseHierarchy(hierarchy)
        self.parseMotion(motion)

    def drawSkeleton(self):
        glPushMatrix()
        if fileName == '0007_Cartwheel001.bvh':
            glScalef(.03,.03,.03)
        self.root.draw()
        glPopMatrix()
        
    def animateMotion(self):
        global pressTime,anim,positionMatrixf, fileName
        time = glfw.get_time()-pressTime
        frameNumber = int(time* (self.fps))% self.frames
        
        glPushMatrix()
        if fileName == '0007_Cartwheel001.bvh':
            glScalef(.03,.03,.03)
        self.root.animate(frameNumber)
        glPopMatrix()
            
    def printBvhInformation(self):
        global path, fileName
        fileName = (path[0].split('\\'))[-1]
        print("File name : " + str(fileName))
        print("Number of frames :"+ str(self.frames)+" frames")
        print("FPS : "+str(self.fps))
        print("Number of joints : "+str(len(self.joints.keys()))+" joints")
        print("List of all joint names : ")
        for i in self.joints.keys():
            print("\t\t\t"+ i)

    
def BvhRendering():
    global path,anim
    anim = Bvh()
    anim.parseFile(path[0])
    anim.printBvhInformation()

    
def key_callback(window, key, scancode, action, mods):
    global projection, isBox, isAnimate, pressTime
    if action==glfw.PRESS:
        if key==glfw.KEY_V:
            projection = not projection
        elif key==glfw.KEY_1:
            isBox = False
        elif key==glfw.KEY_2:
            isBox = True
        elif key==glfw.KEY_SPACE:
            isAnimate = not isAnimate
            pressTime = glfw.get_time()

def cursor_callback(window, xpos, ypos):
    global button_left, button_right, cur_xpos, cur_ypos, azimuth, elevation, u,v, p_ref
    if button_left:
        azimuth += np.radians(cur_xpos - xpos) * 0.1
        elevation += np.radians(ypos - cur_ypos) * 0.1

        if np.cos(elevation) >= 0:
            v = np.array([0,1,0])
        else:
            v = np.array([0,-1,0])

    elif button_right:
        p_ref += (cur_xpos - xpos) * u * 0.005
        p_ref += (ypos - cur_ypos) * v * 0.005

    cur_xpos = xpos
    cur_ypos = ypos

def button_callback(window, button, action, mod):
    global button_left, button_right
    #orbit
    if button==glfw.MOUSE_BUTTON_LEFT:
        if action==glfw.PRESS:
            button_left = True
        elif action==glfw.RELEASE:
            button_left = False
    #pan
    elif button==glfw.MOUSE_BUTTON_RIGHT:
        if action==glfw.PRESS:
            button_right = True
        elif action==glfw.RELEASE:
            button_right = False

#zoom        
def scroll_callback(window, xoffset, yoffset):
    global distance
    distance -= yoffset * 0.2

def drop_callback(window, paths):
    global isDrag,path,isAnimate
    path = paths
    BvhRendering()
    isDrag = True
    isAnimate = False

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(720, 720, "ClassAssignment3", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_drop_callback(window, drop_callback)

    glfw.make_context_current(window)
    glfw.swap_interval(1)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
