"""Study Habit Tracker — Flask application entry point.

Run with:  python app.py
"""

import os

from flask import Flask

import db


def create_app(test_config=None):
    """Create and configure the Flask application.

    test_config is used by the test suite to point at a temporary database.
    """
    app = Flask(__name__)

    if test_config is None:
        app.config["DATABASE"] = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "study_tracker.db"
        )
    else:
        app.config.update(test_config)

    # Create the table if it does not exist yet.
    with app.app_context():
        db.init_db()

    app.teardown_appcontext(db.close_db)

    from routes import bp

    app.register_blueprint(bp)

    return app


if __name__ == "__main__":
    from log import logged

    @logged
    def main():
        port = int(os.environ.get("PORT", "3000"))
        # Bind to 0.0.0.0 so the app is reachable via the Codio public URL.
        app = create_app()
        app.run(host="0.0.0.0", port=port)

    main()