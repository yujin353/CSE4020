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

def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
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

    drawFrame()
    drawGrid()
    drawCubeArray()

def drawUnitCube():
    glBegin(GL_QUADS)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)

    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)

    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)

    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)

    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, 0.5)

    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glEnd()

def drawCubeArray():
    glColor3ub(255, 255, 255)
    glPushMatrix()
    drawUnitCube()
    glPopMatrix()

# draw coordinate system: x in red,y in green, z in blue
def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([1., 0., 0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([0., 1., 0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([0., 0., 1.]))
    glEnd()

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
    global projection
    if key==glfw.KEY_V:
        if action==glfw.PRESS:
            projection = not projection

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

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(720, 720, "ClassAssignment1", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)  

    glfw.make_context_current(window)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
