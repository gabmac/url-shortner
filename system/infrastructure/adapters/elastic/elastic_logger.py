from datetime import datetime
from typing import Any, Dict, Optional, Union

import boto3
from fastapi import Request
from opensearchpy import AWSV4SignerAuth, OpenSearch, RequestsHttpConnection


class AWSSigner:
    session = boto3.Session()
    credentials = session.get_credentials()
    region = session.region_name

    @classmethod
    def signer(cls) -> Optional[AWSV4SignerAuth]:
        if cls.credentials and cls.region:
            return AWSV4SignerAuth(cls.credentials, cls.region)
        else:
            return None


class ElasticsearchLogger(AWSSigner):
    """
    Class describing how to connect to ES ou Amazon Elasticsearch Service
    """

    RESOURCE_ALREADY_EXISTS = "resource_already_exists_exception"

    client = None

    def __init__(self, host: str, port: str, service_name: str, simulate: bool = True):
        if not ElasticsearchLogger.client:
            self.auth = None if simulate else ElasticsearchLogger.signer()
            self.security = False if simulate else True
            ElasticsearchLogger.client = OpenSearch(
                hosts=[
                    {
                        "host": host,
                        "port": port,
                    },
                ],
                use_ssl=self.security,
                verify_certs=self.security,
                http_auth=self.auth,
                connection_class=RequestsHttpConnection,
            )
        self.index_name = "{service_name}-{month}-{year}".format(
            service_name=service_name,
            month=datetime.now().month,
            year=datetime.now().year,
        )
        self.index = self._create_index()

    def _create_index(self) -> Any:
        """
        Tries to create the index
        """
        if self.client is not None and not self.client.indices.exists(
            index=self.index_name,
        ):
            self.client.indices.create(index=self.index_name, body={})
        return True

    def create_document(self, document_dict: Dict[str, Any]) -> None:
        if self.client is not None:
            self.client.index(
                index=self.index_name,
                body=document_dict,
                refresh=True,
            )

    @staticmethod
    async def set_body(request: Request, body: bytes) -> None:
        """Set body from RequestArgs:
        request (Request)
        body (bytes)
        """

        async def receive() -> Dict[str, Union[str, bytes]]:
            return {"type": "http.request", "body": body}

        request._receive = receive

    @staticmethod
    async def get_body(request: Request) -> bytes:
        """Get body from request
        Args:
            request (Request)
        Returns:
            bytes
        """
        body = await request.body()
        await ElasticsearchLogger.set_body(request, body)
        return body
