from typing import DefaultDict


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
        self.scene_stack = DefaultDict(list)
        self.scenes = {}

    def addScene(self, scene):
        self.scenes[scene.name] = scene

    def nextScene(self, name, userID, messageID):
        scene = self.scenes[name]
        if len(self.scene_stack[userID]):
            old_scene = self.scene_stack[userID][-1]
            print(f"Leaving scene {old_scene.name}")
            old_scene.onExit(userID, messageID)
        print(f"Entering scene {scene.name}")
        self.scene_stack[userID].append(scene)
        scene.onEnter(userID)

    def previousScene(self, userID, messageID):
        scene = self.scene_stack[userID].pop()
        print(f"Leaving scene {scene.name}")
        scene.onExit(userID, messageID)
        if len(self.scene_stack[userID]):
            old_scene = self.scene_stack[userID][-1]
            old_scene.onEnter(userID)

    def inlineCallback(self, query):
        userID = query.from_user.id
        messageID = query.message.id
        if not len(self.scene_stack[userID]):
            return
        callback_data_parsed = query.data.split("_")
        callback_btn_menu_id = callback_data_parsed[0]
        event = callback_data_parsed[1]
        scene = self.scene_stack[userID][-1]
        if not scene.menu:
            return
        if not scene.menu.checkInlineButtonLink(callback_btn_menu_id, query.id):
            return
        print(f"Sending event to scene {scene.name}")
        if event == "back":
            self.previousScene(userID, messageID)
        else:
            scene.onEvent(event, userID, messageID, self)

    def clearUserSceneStack(self, userID):
        print(f"Clearing scene stack for user {userID}")
        self.scene_stack[userID] = []
