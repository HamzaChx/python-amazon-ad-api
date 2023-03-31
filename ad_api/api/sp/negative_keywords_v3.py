from ad_api.base import Client, sp_endpoint, ApiResponse, Utils


class NegativeKeywordsV3(Client):

    @sp_endpoint('/sp/negativeKeywords/list', method='POST')
    def list_negative_keywords(self, version: int = 3, **kwargs) -> ApiResponse:
        r"""
        Listing negative product keywords.

        Request Body (optional)

        Returns
            ApiResponse
        """
        json_version = 'application/vnd.spKeyword.v' + str(version) + "+json"
        headers = {
            "Accept": json_version,
            "Content-Type": json_version
        }

        return self._request(kwargs.pop('path'), params=kwargs, headers=headers)

    @sp_endpoint('/sp/negativeKeywords/', method='POST')
    def create_negative_keyword(self, version: int = 3, **kwargs) -> ApiResponse:
        r"""
        Creating negative product keywords.

        Request Body (required)

        Returns
            ApiResponse
        """
        json_version = 'application/vnd.spKeyword.v' + str(version) + "+json"
        headers = {
            "Accept": json_version,
            "Content-Type": json_version
        }

        return self._request(kwargs.pop('path'), data=Utils.convert_body(kwargs.pop('body'), False), params=kwargs,
                             headers=headers)

    @sp_endpoint('/sp/negativeKeywords/', method='PUT')
    def edit_negative_keyword(self, version: int = 3, **kwargs) -> ApiResponse:
        r"""
        Updating negative product keywords.

        Request Body (required)

        Returns
            ApiResponse
        """
        json_version = 'application/vnd.spKeyword.v' + str(version) + "+json"
        headers = {
            "Accept": json_version,
            "Content-Type": json_version
        }

        return self._request(kwargs.pop('path'), data=Utils.convert_body(kwargs.pop('body'), False), params=kwargs,
                             headers=headers)

    @sp_endpoint('/sp/negativeKeywords/delete', method='POST')
    def delete_negative_keywords(self, version: int = 3, **kwargs) -> ApiResponse:
        r"""
        Deleting negative product keywords.

        Request Body (required)

        Returns
            ApiResponse
        """

        json_version = 'application/vnd.spKeyword.v' + str(version) + "+json"
        headers = {
            "Accept": json_version,
            "Content-Type": json_version
        }

        return self._request(kwargs.pop('path'), data=Utils.convert_body(kwargs.pop('body'), False), params=kwargs,
                             headers=headers)

