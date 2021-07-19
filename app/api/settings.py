from flask import (
    g, request, session, jsonify
)

from .api import Setting
from . import setting_bp

setting = Setting()

@setting_bp.route("/sync")
def sync():
    res = setting.sync()
    return jsonify(res)

@setting_bp.route("/offsync")
def offsync():
    res = setting.offsync()
    return jsonify(res)

@setting_bp.route('/privacy')
def privacy():
    res = setting.toggleprivacy()
    return jsonify(res)

@setting_bp.route('/reset')
def reset():
    res = setting.reset()
    return jsonify(res)
    fg