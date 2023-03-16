class Scene:
    def __init__(self, name):
        self.menu = None
        self.name = name

    def onEnter():
        pass

    def onEvent():
        pass

    def onExit():
        pass


class SceneManager:
    def __init__(self):
        self.scene_stack = []
        self.scenes = {}

    def addScene(self, scene):
        self.scenes[scene.name] = scene

    def nextScene(self, name, msg):
        scene = self.scenes[name]
        print(f"Entering scene {scene.name}")
        self.scene_stack.append(scene)
        scene.onEnter(msg)

    def previousScene(self, msg):
        scene = self.scene_stack.pop()
        print(f"Leaving scene {scene.name}")
        scene.onExit(msg)
        if len(self.scene_stack):
            self.scene_stack[-1].onEnter()

    def sendEventToScene(self, event, msg):
        if len(self.scene_stack):
            if event == "back":
                return self.previousScene(msg)
            scene = self.scene_stack[-1]
            print(f"Sending event to scene {scene.name}")
            scene.onEvent(event, msg)
