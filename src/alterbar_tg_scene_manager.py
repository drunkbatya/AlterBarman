class Scene:
    def __init__(self, name):
        self.menu = None
        self.name = name

    def onEnter(self, msg):
        pass

    def onEvent(self, msg, scene_manager):
        pass

    def onExit(self):
        pass


class SceneManager:
    def __init__(self):
        self.scene_stack = []
        self.scenes = {}
        self.init_msg = None

    def addScene(self, scene):
        self.scenes[scene.name] = scene

    def nextScene(self, name, msg):
        scene = self.scenes[name]
        if len(self.scene_stack):
            old_scene = self.scene_stack[-1]
            print(f"Leaving scene {old_scene.name}")
            old_scene.onExit(msg)
        else:
            self.init_msg = msg
        print(f"Entering scene {scene.name}")
        self.scene_stack.append(scene)
        scene.onEnter(self.init_msg)

    def previousScene(self, msg):
        scene = self.scene_stack.pop()
        print(f"Leaving scene {scene.name}")
        scene.onExit(msg)
        if len(self.scene_stack):
            old_scene = self.scene_stack[-1]
            old_scene.onEnter(self.init_msg)

    def sendEventToScene(self, event, msg):
        if len(self.scene_stack):
            if event == "back":
                return self.previousScene(msg)
            scene = self.scene_stack[-1]
            print(f"Sending event to scene {scene.name}")
            scene.onEvent(event, msg, self)
