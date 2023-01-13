__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
appserver.py
- creates an application instance and runs the dev server
"""

import os

if __name__ == "__main__":
    from statesman_discord.main import create_app

    app = create_app()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=True)
