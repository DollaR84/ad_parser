from config import Config

import google_auth_httplib2
from google.oauth2 import service_account

from googleapiclient import http
from googleapiclient import discovery


class Client:

    def __init__(self, config: Config):
        self.cfg = config

    @property
    def credentials(self):
        return service_account.Credentials.from_service_account_file(
            self.cfg.creds_file_path,
            scopes=[self.cfg.scope],
        )

    def get(self):
        auth = google_auth_httplib2.AuthorizedHttp(
            self.credentials, http=http.set_user_agent(
                http.build_http(), self.cfg.application_name
            )
        )

        return discovery.build(
            self.cfg.service_name, self.cfg.service_version, http=auth
        )
