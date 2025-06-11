from app import create_app, logging

app = create_app()

if __name__ == '__main__':
    logging.info('Starting application at http://localhost:5000')
    app.run(debug=True)