import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import os
import ctypes

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

#obj
gVertexArrayIndexed = np.empty((0, 3))
gIndexArray = np.empty((0, 3))
gNormal = np.empty((0, 3))
gNormal2 = np.empty((0, 3))

newVertexArrayIndexed = np.empty((0, 3))
newIndexArray = np.empty((0, 3))
newNormal = np.empty((0, 3))
newNormal2 = np.empty((0, 3))

newVertexArrayIndexed2 = np.empty((0, 3))
newIndexArray2 = np.empty((0, 3))
newNormal2 = np.empty((0, 3))
newNormal22 = np.empty((0, 3))

newVertexArrayIndexed3 = np.empty((0, 3))
newIndexArray3 = np.empty((0, 3))
newNormal3 = np.empty((0, 3))
newNormal32 = np.empty((0, 3))

projection = True
hierarchical_mode = False
wireframe = False
smooth = False


def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    global wireframe
    if wireframe:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else: # solid
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    global projection
    if projection:
        gluPerspective(45, 1, 1, 100)
    else:
        glOrtho(-5,5, -5,5, -100,100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity() 

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

    # lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_NORMALIZE)


    # light 0
    glPushMatrix()
    lightPos0 = (3., 4., 5., 1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos0)
    glPopMatrix()

    #light 1
    glPushMatrix()
    lightPos1 = (-3., -4., 5., 0.)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos1)
    glPopMatrix()

    #light 2
    glPushMatrix()
    lightPos2 = (-3., 4., -5., 0.)
    glLightfv(GL_LIGHT2, GL_POSITION, lightPos2)
    glPopMatrix()

    ambientLightColor = (.1,.0,.0,1.)
    diffuseLightColor = (.5,.0,.0,1.)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLightColor)
    
    ambientLightColor1 = (.0,.1,.0,1.)
    diffuseLightColor1 = (.0,.5,.0,1.)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuseLightColor1)

    ambientLightColor2 = (.0,.0,.1,1.)
    diffuseLightColor2 = (.0,.0,.5,1.)
    glLightfv(GL_LIGHT2, GL_AMBIENT, ambientLightColor2)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, diffuseLightColor2)

    objectColor = (1., 1., 1., 1.)
    specularObjectColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glPushMatrix()

    global hierarchical_mode, gVertexArrayIndexed, gIndexArray, gNormal, gNormal2
    if hierarchical_mode:
        drawAnimatingModel()
    else:
        drawObj(gVertexArrayIndexed, gIndexArray, gNormal, gNormal2)
        
    glPopMatrix()
    
    glDisable(GL_LIGHTING)

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
    
def key_callback(window, key, scancode, action, mods):
    global projection, hierarchical_mode, wireframe, smooth
    if action==glfw.PRESS:
        if key==glfw.KEY_V:
            projection = not projection
        elif key==glfw.KEY_H:
            hierarchical_mode = True
            createHierarchicalModelObject()
        elif key==glfw.KEY_Z:
            wireframe = not wireframe
        elif key==glfw.KEY_S:
            smooth = not smooth 

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
    distance -= yoffset * 0.6

def drop_callback(window, paths):
    global gVertexArrayIndexed, gIndexArray, gNormal, gNormal2, hierarchical_mode

    hierarchical_mode = False
    paths = ''.join(paths)
    gVertexArrayIndexed, gIndexArray, gNormal, gNormal2 = createVertexAndIndexArrayIndexed(paths)
    drawObj(gVertexArrayIndexed, gIndexArray, gNormal, gNormal2)

def createVertexAndIndexArrayIndexed(file):
    v_coords = []
    n_coords = []

    v_index = []
    n_index = []

    tmp_v = []
    tmp_n = []

    gFace = [0, 0, 0]

    for line in open(file, 'r'):
        if line.startswith('#'):
            continue

        values = line.split()
        valNum = values[1:]
        
        if not values:
            continue

        if values[0]=='v':
            tmp = [float(values[1]), float(values[2]), float(values[3])]
            v_coords.append(tmp)
        elif values[0]=='vn':
            tmp = [float(values[1]), float(values[2]), float(values[3])]
            n_coords.append(tmp)
        elif values[0]=='f':

            if len(valNum) == 3:
                gFace[0] += 1
            elif len(valNum) == 4:
                gFace[1] += 1
            else:
                gFace[2] += 1

            for i in range(1, len(valNum)-1):
                face_i = []
                norm_i = []

                for v in values[i:i+2]:
                    w = v.split('/')
                    face_i.append(int(w[0])-1)
                    norm_i.append(int(w[2])-1)
                v = values[len(valNum)]
                w = v.split('/')
                face_i.append(int(w[0])-1)
                norm_i.append(int(w[2])-1)

                if i != 1: # n-polygon
                    tmp_v.append(face_i)
                    tmp_n.append(norm_i)
                else:
                    v_index.append(face_i)
                    n_index.append(norm_i)

    # n-polygon
    for i in range(len(tmp_v)-1, -1, -1):
        v_index.insert(len(n_coords), tmp_v[i])
        n_index.insert(len(n_coords), tmp_n[i])

    narr = [[0.]*3]*len(v_coords)
    narr2 = [[0.]*3]*len(v_coords)
    for i in range(len(v_index)):
        t1 = np.subtract(v_coords[v_index[i][1]], v_coords[v_index[i][0]])
        t2 = np.subtract(v_coords[v_index[i][2]], v_coords[v_index[i][0]])

        nv = np.cross(t1, t2)
        nv = nv / np.sqrt(np.dot(nv, nv))

        for j in range(3):
            narr[v_index[i][j]] = n_coords[n_index[i][j]]
            narr2[v_index[i][j]] += nv

    for i in range(len(v_coords)):
        if np.sqrt(np.dot(narr2[i], narr2[i])) == 0:
            continue
        narr2[i] = narr2[i] / np.sqrt(np.dot(narr2[i], narr2[i]))
    
    varr = np.array(v_coords, 'float32')
    iarr = np.array(v_index)
    narr = np.array(narr)
    narr2 = np.array(narr2)

    if not hierarchical_mode:
        print("File name: ", file.split('\\')[-1])
        print("Total number of faces: " + str(gFace[0] + gFace[1] + gFace[2]))
        print("Number of faces with 3 vertices: " + str(gFace[0]))
        print("Number of faces with 4 vertices: " + str(gFace[1]))
        print("Number of faces more than 4 vertices: " + str(gFace[2]))
    
    return varr, iarr, narr, narr2

# Animating hierarchical model rendering mode
def createHierarchicalModelObject():
    global newVertexArrayIndexed,newIndexArray,newNormal,newNormal2, newVertexArrayIndexed2,newIndexArray2,newNormal2,newNormal22, newVertexArrayIndexed3,newIndexArray3,newNormal3,newNormal32

    i_path = os.path.join(os.getcwd(), './island.obj')
    l_path = os.path.join(os.getcwd(), './Lowpoly_tree_sample.obj')
    s_path = os.path.join(os.getcwd(), './Sting_sword.obj')
    
    newVertexArrayIndexed,newIndexArray,newNormal,newNormal2 = createVertexAndIndexArrayIndexed(i_path)#'./island.obj')
    newVertexArrayIndexed2,newIndexArray2,newNormal2,newNormal22 = createVertexAndIndexArrayIndexed(l_path)#'./Lowpoly_tree_sample.obj')
    newVertexArrayIndexed3,newIndexArray3,newNormal3,newNormal32 = createVertexAndIndexArrayIndexed(s_path)#'./Sting-Sword-lowpoly.obj')
    
def drawAnimatingModel():
    global newVertexArrayIndexed,newIndexArray,newNormal,newNormal2, newVertexArrayIndexed2,newIndexArray2,newNormal2,newNormal22, newVertexArrayIndexed3,newIndexArray3,newNormal3,newNormal32

    t = glfw.get_time()

    # Island drawing    
    glPushMatrix()
    glTranslate(3*np.sin(t), 2 + 2*np.cos(t), np.sin(t))

    glPushMatrix()
    objectColor = (0, 1, 0, 1.)
    specularObjectColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    
    glScalef(4.5, 4.5, 4.5)
    drawObj(newVertexArrayIndexed,newIndexArray,newNormal,newNormal2)
    glPopMatrix()

    # tree drawing
    glPushMatrix()
    glRotatef(t*(180/np.pi), 0, 1, 0)
    glTranslatef(-2., 1.8, -2.)
    glRotatef(-t*(180/np.pi), 0 ,1, 0)

    glPushMatrix()
    objectColor = (1, .5, .0, 1.)
    specularObjectColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glScalef(.2, .2, .2)
    drawObj(newVertexArrayIndexed2,newIndexArray2,newNormal2,newNormal22)
    glPopMatrix()

    glPopMatrix()


    # tree drawing
    glPushMatrix()
    glRotatef(t*(180/np.pi), 0, 1, 0)
    glTranslatef(2., 1.8, 2.)
    glRotatef(t*(180/np.pi), 0 ,1, 0)

    glPushMatrix() 
    objectColor = (1, 1, 0, 1.)
    specularObjectColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glScalef(.13, .13, .13)
    drawObj(newVertexArrayIndexed2,newIndexArray2,newNormal2,newNormal22)
    glPopMatrix()

    
    # sword drawing
    glPushMatrix()
    glTranslatef(2*np.sin(t), 2, 0.)
    glRotatef(5*t*(180/np.pi), 0, 1, 0)

    glPushMatrix()
    objectColor = (0, 0, 1, 1.)
    specularObjectColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
   
    glScale(0.05, 0.05, 0.05)
    drawObj(newVertexArrayIndexed3,newIndexArray3,newNormal3,newNormal32)
    glPopMatrix()
    
    glPopMatrix()

    # sword drawing
    glPushMatrix()
    glTranslatef(2*np.sin(t), 3, 0.)
    glRotatef(5*t*(180/np.pi), 0, 0, 1)

    glPushMatrix()
    objectColor = (1, 0, 0, 1.)
    specularObjectColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glScale(0.05, 0.05, 0.05)
    drawObj(newVertexArrayIndexed3,newIndexArray3,newNormal3,newNormal32)
    glPopMatrix()

    glPopMatrix()
    glPopMatrix()
    glPopMatrix()

def drawObj(vertexArrayIndexed, indexArray, normal, normal2):
    global smooth
    
    varr = vertexArrayIndexed
    iarr = indexArray
    narr = normal
    narr2 = normal2

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    
    if smooth:
        glNormalPointer(GL_FLOAT, 3*varr.itemsize, narr2)
    else:
        glNormalPointer(GL_FLOAT, 3*varr.itemsize, narr)

    glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(960, 960, "ClassAssignment2", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_drop_callback(window, drop_callback)

    glfw.make_context_current(window)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
