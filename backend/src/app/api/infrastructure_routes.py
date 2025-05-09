# routes.py
from flask import Blueprint, jsonify, request
from .infrastructure_api import InfrastructurePlanner
from ..graph.networks import TransportationNetwork

planner_bp = Blueprint("planner", __name__)

def load_planner(period: str = "morning"):
    tn = TransportationNetwork.from_json_folder("data")
    return InfrastructurePlanner(tn, period=period)

@planner_bp.route("/", methods=["GET"])
def default_morning():
    planner = load_planner("morning")
    return jsonify(planner.get_mst_edges())

@planner_bp.route("/period/<period>", methods=["GET"])
def mst_by_period(period):
    planner = load_planner(period)
    return jsonify(planner.get_mst_edges())

@planner_bp.route("/analysis", methods=["GET"])
def cost_analysis():
    period = request.args.get("period", "morning")
    planner = load_planner(period)
    return jsonify(planner.analyze_cost_effectiveness())
