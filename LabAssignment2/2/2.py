import glfw
from OpenGL.GL import *

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_LINE_LOOP)
    glVertex2f(0.5, 0.5)
    glVertex2f(-0.5,0.5)
    glVertex2f(-0.5,-0.5)
    glVertex2f(0.5,-0.5)
    glEnd()
    
def main():
    if not glfw.init():
        return
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
