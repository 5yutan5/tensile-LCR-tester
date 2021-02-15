from enum import Enum

import AutoLab.icons.resource_icons
from PySide6.QtGui import QIcon


class IconNames(Enum):
    ADD_BEHAVIOR = ":AddBehavior_16x.svg"
    ADD_CONNECTION = ":AddConnection_16x.svg"
    CHECK_MARK = ":Checkmark_16x.svg"
    COLLAPSE_LEFT = ":CollapseLeft_16x.svg"
    COLLAPSE_UP = ":CollapseUp_16x.svg"
    CONNECT = ":Connect_16x.svg"
    CONNECT_PLUGGED = ":ConnectPlugged_16x.svg"
    CONNECT_UNPLUGGED = ":ConnectUnplugged_16x.svg"
    CONTINUE = ":DebugContinue_16x.svg"
    DISCONNECT = ":Disconnect_16x.svg"
    DYNAMIC = ":Dynamic_16x.svg"
    DYNAMIC_GROUP = ":DynamicGroup_16x.svg"
    EXPAND_ARROW = ":ExpandArrow_16x.svg"
    EXPAND_DOWN = ":ExpandDown_16x.svg"
    EXPAND_RIGHT = ":ExpandRight_16x.svg"
    FOLDER_OPENED = ":FolderOpened_16x.svg"
    LOADING = ":Loading_16x.svg"
    OPEN_FOLDER = ":OpenFolder_16x.svg"
    RUN = ":Run_16x.svg"
    STATUS_OK = ":StatusOK_16x.svg"
    STATUS_PAUSE = ":StatusPause_16x.svg"
    STATUS_RUN = ":StatusRun_16x.svg"
    STATUS_SEALED = ":StatusSealed_16x.svg"
    STOP = ":Stop_16x.svg"


def create_qicon(name: IconNames) -> QIcon:
    return QIcon(name.value)
