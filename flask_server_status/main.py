import pkg_resources
from typing import List, Optional
from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import sessionmaker

from .utils.cache import cache
from .db import get_routes as _get_routes_
from .db.engine import get_engine, create_tables
from .utils.cron import background_log, get_logs

class FlaskStatus:
    def __init__(self,
                 app: Flask = None, 
                 routes: Optional[List[str]] = None,  
                 url_prefix: Optional[str] = None):
        """
        FlaskStatus

        :param app: Flask app
        :param routes: List of routes to be monitored
        :param timeout: Time in seconds to update the logs. Default is 5 minutes
        :param url_prefix: URL prefix to access the logs. Default is '/status'
        """
        self.app = app
        if app is not None:
            self.init_app(app, routes, url_prefix)

    def init_app(self,
                 app: Flask, 
                 routes: Optional[List[str]] = None, 
                 url_prefix: Optional[str] = None):
        self.app = app

        if not app.config.get('SQLALCHEMY_DATABASE_URI'):
            app.logger.warning('SQLALCHEMY_DATABASE_URI is not set in app.config. Using default sqlite:///tmp/status.db')
        
        cache['SQLALCHEMY_DATABASE_URI'] = app.config.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///tmp/status.db')

        if isinstance(app.config.get('API_ENABLED'), bool) and app.config.get('API_ENABLED') is True and app.config.get('API_SECRET'):
            from .routes.configure import route as configure
            
            if app.config.get('API_SECRET').startswith('Bearer ') is False:
                cache['API_SECRET'] = 'Bearer ' + app.config
            else:
                cache['API_SECRET'] = app.config.get('API_SECRET')
            
            app.register_blueprint(configure, url_prefix='/flask-status')
        
        if not url_prefix:
            url_prefix = '/status'
        
        if url_prefix.startswith('/') is False:
            self.url_prefix = '/' + url_prefix
        
        app.template_folder = pkg_resources.resource_filename('flask_server_status', 'statsig/templates')
        app.static_folder   = pkg_resources.resource_filename('flask_server_status', 'statsig/static')

        engine = get_engine(cache['SQLALCHEMY_DATABASE_URI'])
        create_tables(engine)
        session = sessionmaker(bind=engine)()

        scheduler = BackgroundScheduler()
        scheduler.add_job(get_logs, 'interval', seconds=2)
        scheduler.add_job(background_log, 'cron', args=[app, session, routes], minute='*')
        scheduler.start()

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['flask-status'] = self

        @app.route(url_prefix)
        def flask_logs():
            """
            # Status Page

            This page shows all routes in the app and the logs
            """
            response = _get_routes_(session, routes) if not cache.get('routes') else cache['routes']
            return render_template('index.html', response=response)
        return app