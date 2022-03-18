import glfw
from OpenGL.GL import *

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_input)
    glVertex2f(0.5, 0.5)
    glVertex2f(-0.5,0.5)
    glVertex2f(-0.5,-0.5)
    glVertex2f(0.5,-0.5)
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global GL_input
    
    if key == glfw.KEY_0:
        GL_input = GL_POLYGON
    elif key == glfw.KEY_1:
        GL_input = GL_POINTS
    elif key == glfw.KEY_2:
        GL_input = GL_LINES
    elif key == glfw.KEY_3:
        GL_input = GL_LINE_STRIP
    elif key == glfw.KEY_4:
        GL_input = GL_LINE_LOOP
    elif key == glfw.KEY_5:
        GL_input = GL_TRIANGLES
    elif key == glfw.KEY_6:
        GL_input = GL_TRIANGLE_STRIP
    elif key == glfw.KEY_7:
        GL_input = GL_TRIANGLE_FAN
    elif key == glfw.KEY_8:
        GL_input = GL_QUADS
    elif key == glfw.KEY_9:
        GL_input = GL_QUAD_STRIP
        
def main():
    global GL_input
    GL_input = GL_LINE_LOOP

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
