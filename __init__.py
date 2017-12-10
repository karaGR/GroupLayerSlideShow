# -*- coding: utf-8 -*-

#===================================
#レイヤースライドショープラグイン
#
#===================================

def classFactory(iface):
    from .main import main
    return main(iface) 