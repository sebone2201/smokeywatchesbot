from smokey_database_version import *
if __name__ == "__main__":
    import threading
    from flask import Flask

    # Start Flask just to bind a port for Render
    def start_flask():
        app = Flask(__name__)

        @app.route("/")
        def index():
            return "Bot is running!"

        app.run(host="0.0.0.0", port=8000)

    # Run your bot in the main thread
    threading.Thread(target=start_flask).start()
    main()