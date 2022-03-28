import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

key_input = []

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    # draw cooridnates
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    
    glColor3ub(255, 255, 255)
    
    ###########################
    for k in key_input:
        if k == 'Q':
            glTranslatef(-0.1, 0., 0.)
        elif k == 'E':
            glTranslatef(0.1, 0., 0.)
        elif k == 'A':
            glRotatef(10., 0., 0., 1.)
        elif k == 'D':
            glRotatef(-10., 0., 0., 1.)
        elif k == '1':
            key_input.clear()
            glLoadIdentity()
    ###########################
    
    drawTriangle()
    
def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0.,.5]))
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([.5,0.]))
    glEnd()
   
def key_callback(window, key, scancode, action, mods):
    global key_input
    
    if action==glfw.PRESS or action==glfw.REPEAT:
        #translate -0.1 x
        if key == glfw.KEY_Q:
            key_input.insert(0,'Q')
        #translate 0.1 x
        elif key == glfw.KEY_E:
            key_input.insert(0,'E')
        #rotate 10
        elif key == glfw.KEY_A:
            key_input.insert(0,'A')
        #rotate 10
        elif key == glfw.KEY_D:
            key_input.insert(0,'D')
        #reset
        elif key == glfw.KEY_1:
            key_input.insert(0, '1')
        
def main():
    global key_input
    if not glfw.init():
        return    
    window = glfw.create_window(480, 480, "2020056353", None, None)
    if not window:
        glfw.terminate()
        return
    
    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
