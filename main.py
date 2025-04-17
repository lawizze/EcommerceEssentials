from app import app
import auth
import admin
import shop
import cart

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
