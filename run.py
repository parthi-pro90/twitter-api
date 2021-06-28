from app import app


if __name__ == '__main__':
    # from gevent import monkey
    # monkey.patch_all(ssl=False)
    app.run(host='127.0.0.1', port=7010)
    # app.run(host=app.config['SERVER_HOST'], debug=True,port=app.config['PORT'],threaded=True)
