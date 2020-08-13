from App import get_app

application = get_app()


if __name__ == "__main__":
    application.run(debug=True)