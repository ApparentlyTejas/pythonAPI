from flask import jsonify


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(_):
        return jsonify({"error": "bad request"}), 400

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"error": "not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(_):
        return jsonify({"error": "method not allowed"}), 405

    @app.errorhandler(500)
    def internal_error(_):
        return jsonify({"error": "internal server error"}), 500
