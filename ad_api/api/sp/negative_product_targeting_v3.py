from ad_api.base import Client, sp_endpoint, fill_query_params, ApiResponse, Utils


class NegativeTargetsV3(Client):

    @sp_endpoint('/sp/negativeTargets/list', method='POST')
    def list_negative_product_targets(self, version: int = 3, **kwargs) -> ApiResponse:
        r"""
        Listing negative product targets.

        Request Body (optional)

        Returns
            ApiResponse
        """
        json_version = 'application/vnd.spTargetingClause.v' + str(version) + "+json"
        headers = {
            "Accept": json_version,
            "Content-Type": json_version
        }

        return self._request(kwargs.pop('path'), params=kwargs, headers=headers)

    @sp_endpoint('/sp/negativeTargets', method='POST')
    def create_negative_product_targets(self, version: int = 3, **kwargs) -> ApiResponse:
        r"""
        Creating negative product targets.

        Request Body (required)

        Returns
            ApiResponse
        """
        json_version = 'application/vnd.spTargetingClause.v' + str(version) + "+json"
        headers = {
            "Accept": json_version,
            "Content-Type": json_version
        }

        return self._request(kwargs.pop('path'), data=Utils.convert_body(kwargs.pop('body'), False), params=kwargs,
                             headers=headers)

    @sp_endpoint('/sp/negativeTargets', method='PUT')
    def edit_negative_product_targets(self, version: int = 3, **kwargs) -> ApiResponse:
        r"""
        Updating negative product targets.

        Request Body (required)

        Returns
            ApiResponse
        """
        json_version = 'application/vnd.spTargetingClause.v' + str(version) + "+json"
        headers = {
            "Accept": json_version,
            "Content-Type": json_version
        }

        return self._request(kwargs.pop('path'), data=Utils.convert_body(kwargs.pop('body'), False), params=kwargs,
                             headers=headers)

    @sp_endpoint('/sp/negativeTargets/delete', method='POST')
    def delete_negative_product_targets(self, version: int = 3, **kwargs) -> ApiResponse:
        r"""
        Deleting negative product targets.

        Request Body (required)

        Returns
            ApiResponse
        """
        json_version = 'application/vnd.spTargetingClause.v' + str(version) + "+json"
        headers = {
            "Accept": json_version,
            "Content-Type": json_version
        }

        return self._request(kwargs.pop('path'), data=Utils.convert_body(kwargs.pop('body'), False), params=kwargs,
                             headers=headers)

