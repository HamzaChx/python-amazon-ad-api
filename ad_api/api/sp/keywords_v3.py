from ad_api.base import Client, sp_endpoint, fill_query_params, ApiResponse, Utils


class KeywordsV3(Client):

    @sp_endpoint('/sp/keywords/list', method='POST')
    def list_keywords(self, version: int = 3, **kwargs) -> ApiResponse:
        r"""
        Listing product keywords.

        Request Body (optional)

        Returns
            ApiResponse
        """
        json_version = 'application/vnd.spKeyword.v3+json' + str(version) + "+json"

        headers = {
            "Accept": json_version,
            "Content-Type": json_version
        }

        return self._request(kwargs.pop('path'), params=kwargs, headers=headers)

    @sp_endpoint('/sp/keywords', method='POST')
    def create_keyword(self, version: int = 3, **kwargs) -> ApiResponse:
        r"""
        Creating product keywords.

        Request Body (required)

        Returns
            ApiResponse
        """
        json_version = 'application/vnd.spKeyword.v3+json' + str(version) + "+json"

        headers = {
            "Accept": json_version,
            "Content-Type": json_version
        }

        return self._request(kwargs.pop('path'), data=Utils.convert_body(kwargs.pop('body'), False), params=kwargs,
                             headers=headers)

    @sp_endpoint('/sp/keywords', method='PUT')
    def edit_keyword(self, version: int = 3, **kwargs) -> ApiResponse:
        r"""
        Updating product keywords.

        Request Body (required)

        Returns
            ApiResponse
        """

        json_version = 'application/vnd.spKeyword.v3+json' + str(version) + "+json"
        headers = {
            "Accept": json_version,
            "Content-Type": json_version
        }

        return self._request(kwargs.pop('path'), data=Utils.convert_body(kwargs.pop('body'), False), params=kwargs,
                             headers=headers)

    @sp_endpoint('/sp/keywords/delete', method='POST')
    def delete_keywords(self, version: int = 3, **kwargs) -> ApiResponse:
        r"""
        Deleting product keywords.

        Request Body (required)

        Returns
            ApiResponse
        """

        json_version = 'application/vnd.spKeyword.v3+json' + str(version) + "+json"
        headers = {
            "Accept": json_version,
            "Content-Type": json_version
        }

        return self._request(kwargs.pop('path'), data=Utils.convert_body(kwargs.pop('body'), False), params=kwargs,
                             headers=headers)
