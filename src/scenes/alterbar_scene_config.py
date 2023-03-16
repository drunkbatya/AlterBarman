import alterbar_tg
from . import alterbar_scene_new_order


def scenesInit():
    alterbar_tg.scene_manager.addScene("new_order", alterbar_scene_new_order.scene)
