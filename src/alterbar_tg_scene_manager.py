class Scene:
    def __init__(self, onEnter, onEvent, onExit):
        self.onEnter = onEnter
        self.onEvent = onEvent
        self.onExit = onExit


class SceneManager:
    def __init__(self):
        self.scene_stack = []
        self.scenes = {}

    def addScene(self, name, scene):
        self.scenes[name] = scene

    def nextScene(self, name, msg):
        scene = self.scenes[name]
        self.scene_stack.append(scene)
        scene.onEnter(msg)

    def previousScene(slef):
        scene = self.scene_stack.pop()
        scene.enExit()
        if len(self.scene_stack):
            self.scene_stack[-1].onEnter()

    def sendEventToScene(self, event):
        if len(self.scene_stack):
            self.scene_stack[-1].onEvent(event)
