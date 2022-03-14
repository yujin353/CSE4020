import glfw
from OpenGL.GL import *

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    if key == 1:
        glBegin(GL_POINTS)
    elif key == 2:
        glBegin(GL_LINES)
    elif key == 3:
        glBegin(GL_LINE_STRIP)
    elif key == 4:
        glBegin(GL_LINE_LOOP)
    elif key == 5:
        glBegin(GL_TRIANGLES)
    elif key == 6:
        glBegin(GL_TRIANGLE_STRIP)
    elif key == 7:
        glBegin(GL_TRIANGLE_FAN)
    elif key == 8:
        glBegin(GL_QUADS)
    elif key == 9:
        glBegin(GL_QUAD_STRIP)
    elif key == 10:
        glBegin(GL_POLYGON)
    glVertex2f(0.5, 0.5)
    glVertex2f(-0.5,0.5)
    glVertex2f(-0.5,-0.5)
    glVertex2f(0.5,-0.5)
    glEnd()
    
def main():
    if not glfw.init():
        return
    
    print('enter key')
    global key
    key = int(input())
    
    window = glfw.create_window(480, 480, "2020056353", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()
