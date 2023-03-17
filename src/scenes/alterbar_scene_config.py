import alterbar_tg
from . import alterbar_scene_new_order
from . import alterbar_scene_test


def scenesInit():
    alterbar_tg.scene_manager.addScene(alterbar_scene_new_order.scene)
    alterbar_tg.scene_manager.addScene(alterbar_scene_test.scene)
