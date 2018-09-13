import app

app = app.create_app()

if __name__ == '__main__':
    # for rule in app.url_map.iter_rules():
    #     print(rule)
    app.run(host='0.0.0.0', port=8081, debug=True)